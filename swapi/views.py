import csv
import os
from datetime import datetime

import petl as etl
import requests
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Dataset


class DataDownloader:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        results = []
        with requests.Session() as session:
            while self.url:
                response = session.get(self.url)
                response.raise_for_status()
                data = response.json()
                results.extend(data["results"])
                self.url = data["next"]
        return results

    def resolve_homeworld(self, results):
        for result in results:
            result["homeworld"] = self.resolve_homeworld_helper(result["homeworld"])
        return results

    def resolve_homeworld_helper(self, url):
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()
        return data["name"]

    def transform_data(self, results, fields_to_drop):
        table = etl.fromdicts(results)
        table = etl.cutout(table, *fields_to_drop)
        table = etl.addfield(
            table,
            "date",
            lambda row: datetime.strptime(
                row["edited"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).strftime("%Y-%m-%d"),
        )
        return table

    def create_filename(self):
        return f'characters_{timezone.now().strftime("%Y%m%d%H%M%S")}.csv'

    def save_data_as_csv(self, table, filename):
        file_path = f"swapi/{filename}"
        with default_storage.open(file_path, "wb") as f:
            etl.tocsv(table, f)

    def save_metadata_to_database(self, results, filename):
        num_characters = len(results)
        Dataset.objects.create(file_name=filename, num_characters=num_characters)

    def download_data(self):
        results = self.fetch_data()
        filename = self.create_filename()
        fields_to_drop = {"birth_year", "edited"} - set(results[0].keys())
        results = self.resolve_homeworld(results)
        table = self.transform_data(results, fields_to_drop)
        self.save_data_as_csv(table, filename)
        self.save_metadata_to_database(results, filename)


def download_data_view(request):
    if request.method == "POST":
        try:
            downloader = DataDownloader(os.getenv("SWAPI_BASE_URL"))
            downloader.download_data()
            messages.success(request, "Data downloaded successfully!")
        except Exception as e:
            messages.error(request, f"Failed to download data. Error message: {str(e)}")
            return HttpResponseServerError()

        return redirect(reverse("download_data"))

    datasets = Dataset.objects.all()
    return render(request, "index.html", {"datasets": datasets})


def preview_dataset(request, *args, **kwargs):
    # Load CSV data
    filename = kwargs.get("filename")
    file_path = f"swapi/{filename}"
    with default_storage.open(file_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Set up paginator
    paginator = Paginator(rows, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "csv.html", {"page_obj": page_obj, "csv_file": file_path})


def compare_fields(request, *args, **kwargs):
    # Load CSV data
    filename = kwargs.get("filename")
    file_path = f"swapi/{filename}"
    with default_storage.open(file_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if request.method != "POST":
        return render(request, "example.html", {"rows": rows, "filename": filename})

    selected_columns = request.POST.get("selected_columns")
    selected_columns = selected_columns.split(",") if selected_columns else []

    # Filter rows to selected columns
    filtered_rows = []
    for row in rows:
        filtered_row = {column: row[column] for column in selected_columns}
        filtered_rows.append(filtered_row)

    # Count occurrences of values for selected columns
    value_counts = {}
    for row in filtered_rows:
        key = tuple(row.values())
        value_counts[key] = value_counts.get(key, 0) + 1

    # Create table rows with value counts
    table_rows = []
    for key, count in value_counts.items():
        row_dict = {column: key[i] for i, column in enumerate(selected_columns)}
        row_dict["count"] = count
        table_rows.append(row_dict)

    # Sort table rows by count in descending order
    table_rows = sorted(table_rows, key=lambda row: row["count"], reverse=True)

    return JsonResponse({"rows": table_rows, "filename": filename})

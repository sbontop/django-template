import os

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .models import Dataset
from .util.data_downloader import DataDownloader
from .util.data_preview import DataPreview


class DownloadDataView(View):
    def get(self, request):
        datasets = Dataset.objects.all()
        return render(request, "index.html", {"datasets": datasets})

    def post(self, request):
        try:
            downloader = DataDownloader(os.getenv("SWAPI_BASE_URL"))
            downloader.download_data()
            messages.success(request, "Data downloaded successfully!")
        except Exception as e:
            messages.error(request, f"Failed to download data. Error message: {str(e)}")
            return HttpResponseServerError()

        return redirect(reverse("download_data"))


class PreviewDatasetView(View):
    def get(self, request, *args, **kwargs):
        # Load CSV data
        filename = kwargs.get("filename")
        file_path = f"swapi/{filename}"
        rows = DataPreview(file_path).load_csv_data()

        # Set up paginator
        paginator = Paginator(rows, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request, "csv.html", {"page_obj": page_obj, "csv_file": file_path}
        )


class CompareFieldsView(View):
    def get(self, request, *args, **kwargs):
        # Load CSV data
        filename = kwargs.get("filename")
        file_path = f"swapi/{filename}"
        rows = DataPreview(file_path).load_csv_data()

        return render(
            request, "compare_fields.html", {"rows": rows, "filename": filename}
        )

    def post(self, request, *args, **kwargs):
        # Load CSV data
        filename = kwargs.get("filename")
        file_path = f"swapi/{filename}"
        rows = DataPreview(file_path).load_csv_data()

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


class GetColumnOptionsView(View):
    def get(self, request, *args, **kwargs):
        # Load CSV data
        filename = kwargs.get("filename")
        file_path = f"swapi/{filename}"
        rows = DataPreview(file_path).load_csv_data()
        return JsonResponse({"columns": list(rows[0].keys())})

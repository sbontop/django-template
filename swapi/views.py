# swapi/views.py

import os
from datetime import datetime

import petl as etl
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from api.settings import MEDIA_ROOT

from .models import Person

SWAPI_ENDPOINT = "https://swapi.co/api/people/"
TRANSFORMATIONS = [
    (
        "edited",
        lambda d: datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d"),
    ),
    ("homeworld", lambda url: requests.get(url).json()["name"]),
]


@require_http_methods(["GET", "POST"])
def download_swapi_data(request):
    """Download data from the SWAPI endpoint and save it to a CSV file."""
    if request.method != "POST":
        return render(request, "download_swapi_data.html")
    # Fetch the data from the SWAPI endpoint
    response = requests.get(os.getenv("SWAPI_BASE_URL"))
    data = response.json()["results"]

    # Apply transformations to the data
    data = etl.fromdicts(data)
    for field, transform_fn in TRANSFORMATIONS:
        data = etl.fieldmap(transform_fn, field, data)

    # Save the transformed data to a CSV file in the file system
    filename = f'swapi_data_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
    file_path = os.path.join(MEDIA_ROOT, filename)
    etl.tocsv(data, file_path)

    # Save the metadata for the downloaded dataset to the database
    Person.objects.create(filename=filename)

    # Return a download response for the CSV file
    with open(file_path, "r") as f:
        file_data = f.read()
    response = HttpResponse(file_data, content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

# swapi/views.py

import os

import requests
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView

from data_outputter.swapi.swapi_data_outputter import SwapiDataOuputter
from data_transformer.swapi.swapi_data_transformer import SwapiDataTransformer

from .models import Person


class SwapiETL(TemplateView):
    template_name = "swapi.html"

    def get(self, request):
        # Retrieve the data
        url = os.getenv("SWAPI_URL")
        data = []
        while url:
            response = requests.get(url)
            json_data = response.json()
            data += json_data["results"]
            url = json_data["next"]
        for d in data:
            # Transform the data
            dt = SwapiDataTransformer(d)
            table = dt.transform_data()

            # Output the data
            do = SwapiDataOuputter(table)
            do.to_csv()
            do.to_db()

        # Redirect to a new URL
        return redirect(reverse("swapi_list"))


class SwapiListView(ListView):
    model = Person
    template_name = "swapi_list.html"

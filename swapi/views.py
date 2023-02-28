# swapi/views.py

import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import SwapiModel
import os
import requests
from django.urls import reverse
from data_puller.swapi.swapi_data_puller import SwapiDataPuller
from data_transformer.swapi.swapi_data_transformer import SwapiDataTransformer
from data_outputter.swapi.swapi_data_outputter import SwapiDataOuputter

class SwapiETL(TemplateView):
    template_name = 'swapi.html'

    def post(self, request):
        # Retrieve the data
        data = []
        page_number = 1
        while True:
            response = requests.get(f"{os.getenv('SWAPI_URL')}?page={page_number}")
            if response.status_code != 200:
                break
            data += response.json()['results']
            page_number += 1

        # Transform the data
        dt = SwapiDataTransformer(data)
        table = dt.transform_data()

        # Output the data
        do = SwapiDataOuputter(table)
        do.to_csv()
        do.to_db()

        # Redirect to a new URL
        return redirect(reverse('swapi_list'))

class SwapiListView(ListView):
    model = SwapiModel
    template_name = 'swapi_list.html'

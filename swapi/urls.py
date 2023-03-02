# swap/urls.py
from django.urls import path

from . import views

urlpatterns = [
    # path("etl/", views.SwapiETL.as_view(), name="swapi_etl"),
    # path("list/", views.SwapiListView.as_view(), name="swapi_list"),
    path("download_data/", views.download_swapi_data, name="swapi_download"),
]

from django.urls import path

from .views import download_data_view, view_csv

urlpatterns = [
    path("download_data/", download_data_view, name="download_data"),
    path("view_csv/<str:filename>", view_csv, name="view_csv"),
]

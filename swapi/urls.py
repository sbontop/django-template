from django.urls import path

from .views import compare_fields, download_data_view, preview_dataset

urlpatterns = [
    path("download_data/", download_data_view, name="download_data"),
    path("preview_dataset/<str:filename>", preview_dataset, name="preview_dataset"),
    path("compare_fields/<str:filename>", compare_fields, name="compare_fields"),
]

from django.urls import path

from .views import (
    CompareFieldsView,
    DownloadDataView,
    GetColumnOptionsView,
    PreviewDatasetView,
)

urlpatterns = [
    path("download_data/", DownloadDataView.as_view(), name="download_data"),
    path(
        "preview_dataset/<str:filename>/",
        PreviewDatasetView.as_view(),
        name="preview_dataset",
    ),
    path(
        "compare_fields/<str:filename>/",
        CompareFieldsView.as_view(),
        name="compare_fields",
    ),
    path(
        "get_column_options/<str:filename>/",
        GetColumnOptionsView.as_view(),
        name="get_column_options",
    ),
]

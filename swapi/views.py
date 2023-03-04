import os

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Dataset
from .util.compare_field import CompareField
from .util.data_downloader import DataDownloader
from .util.data_preview import DataPreview


class DownloadDataView(TemplateView):
    template_name = "datasets.html"

    def get_context_data(self, **kwargs):
        datasets = Dataset.objects.all()
        return {"datasets": datasets}

    def post(self, request):
        downloader = DataDownloader(os.getenv("SWAPI_BASE_URL"))
        downloader.download_data()
        return redirect(reverse("download_data"))


class PreviewDatasetView(TemplateView):
    template_name = "preview_csv.html"

    def get_context_data(self, **kwargs):
        filename = kwargs.get("filename")
        data = DataPreview(filename).load_csv_data()
        # Paginate data
        paginator = Paginator(data, 10)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return {"page_obj": page_obj, "filename": filename}


class CompareFieldsView(TemplateView):
    template_name = "compare_fields.html"

    def get_context_data(self, **kwargs):
        filename = kwargs.get("filename")
        data = DataPreview(filename).load_csv_data()
        return {"data": data, "filename": filename}

    def post(self, request, *args, **kwargs):
        filename = kwargs.get("filename")
        data = DataPreview(filename).load_csv_data()
        selected_columns = request.POST.get("selected_columns")

        table_data = CompareField(data, selected_columns).compare()

        return JsonResponse({"data": table_data, "filename": filename})


class GetColumnOptionsView(TemplateView):
    def get(self, request, *args, **kwargs):
        filename = kwargs.get("filename")
        data = DataPreview(filename).load_csv_data()
        return JsonResponse({"columns": list(data[0].keys())})

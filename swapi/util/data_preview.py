import csv

from django.core.files.storage import default_storage


class DataPreview:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv_data(self):
        with default_storage.open(self.file_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

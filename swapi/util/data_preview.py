import csv

from django.core.files.storage import default_storage


class DataPreview:
    def __init__(self, filename):
        self.filename = filename

    def get_filepath(self):
        return f"swapi/{self.filename}"

    def load_csv_data(self):
        with default_storage.open(self.get_filepath(), "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows

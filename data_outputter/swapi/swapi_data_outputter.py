# swapi_data_outputter.py
import os
from datetime import datetime

import petl as etl

from swapi.models import Person


class SwapiDataOuputter:
    def __init__(self, data):
        self.data = data
        self.filename = self._get_filename()
        self.filepath = self._get_filepath()
        self._create_root_dir()

    def _create_root_dir(self):
        if not os.path.exists(os.getenv("DATA_OUTPUT_PATH")):
            os.mkdir(os.getenv("DATA_OUTPUT_PATH"))

    def _get_filename(self):
        return f"swapi_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    def _get_filepath(self):
        return f"{os.getenv('DATA_OUTPUT_PATH')}/{self._get_filename()}"

    def to_csv(self):
        etl.tocsv(self.data, self.filepath)

    def to_db(self):
        swapi_data = Person(filename=self.filename)
        swapi_data.save()

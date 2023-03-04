
# swapi_data_outputter.py
import petl as etl
from swapi.models import SwapiModel
from datetime import datetime
import os

class SwapiDataOuputter:
    def __init__(self, data):
        self.data = data
        self.filename = self.create_filename()
        self.filepath = self.create_filepath()
    
    def create_filename(self):
        return f"swapi_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    def create_filepath(self):
        return f"{os.getenv('DATA_OUTPUT_PATH')}/{self.create_filename()}"

    def to_csv(self):
        etl.tocsv(self.data, self.filepath)
    
    def to_db(self):
        swapi_data = SwapiModel(filename=self.filename)
        swapi_data.save()

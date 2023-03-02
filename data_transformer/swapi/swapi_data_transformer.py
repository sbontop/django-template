# swapi_data_transformer.py
from datetime import datetime

import petl as etl


class SwapiDataTransformer:
    def __init__(self, data):
        self.data = data

    def transform_data(self):
        table = etl.fromdicts(self.data)
        table = table.convert(
            "edited",
            lambda d: datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )
        table = table.rename({"homeworld": "homeworld_url"})
        table = table.joinlookup(
            etl.fromjson("https://swapi.dev/api/planets/", "results"),
            "homeworld_url",
            "url",
            "name",
        )
        table = table.cutout(
            "films", "species", "vehicles", "starships", "created", "edited", "url"
        )

        return table

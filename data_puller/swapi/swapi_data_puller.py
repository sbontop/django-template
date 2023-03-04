# swapi_data_puller.py
import requests

class SwapiDataPuller:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        return requests.get(self.url)
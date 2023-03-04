# swapi_data_transformer.py
import petl as etl


class SwapiDataTransformer:
    def __init__(self, data):
        self.data = data
        
    
    
    
    def transform_data(self):
        table = etl.fromdicts(self.data)
        table = etl.addfield(table, 'date', lambda row: row['edited'][:10])
        table = etl.cutout(table, 'edited', 'url', 'films', 'species', 'vehicles', 'starships')
        table = etl.join(table, 'homeworld', 'https://swapi.co/api/planets/{id}/', key='id', lookup='name')
        return table

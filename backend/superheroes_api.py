import requests
import json
from django.conf import settings


class SuperheroesAPI():
    API_KEY = settings.SUPERHERO_KEY
    BASE_URI = settings.SUPERHERO_URI

    def get_character_data(self, id):
        uri = f'{self.BASE_URI}{self.API_KEY}/{id}'
        response = requests.get(uri)
        return json.loads(response.text)

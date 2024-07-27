import grequests
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

    def get_characters_data(self, ids):
        urls = [f'{self.BASE_URI}{self.API_KEY}/{id}' for id in ids]
        rs = (grequests.get(u) for u in urls)
        responses = grequests.map(rs)
        json_responses = list(
            map(lambda response: json.loads(response.text) if response else None, responses))
        return json_responses

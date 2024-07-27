import grequests
import requests
import json
from settings.settings import *


class SuperheroesAPI():
    API_KEY = SUPERHERO_KEY
    BASE_URI = SUPERHERO_URI

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

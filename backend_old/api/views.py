from django.views import View
from django.http import JsonResponse
from utilities import generate_teams, random_attack
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create your views here.


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


class Battle():
    def __init__(self, a_team, b_team):
        self.a_team = a_team
        self.b_team = b_team

    def run_battle(self):
        winner = ''
        while self.a_team['characters'] and self.b_team['characters']:
            a_character = self.a_team['characters'][0]
            b_character = self.b_team['characters'][0]
            logger.info(
                '------------------------------ FIGHT ----------------------------------')
            logger.info(
                f'Character: {a_character["name"]}, Initial HP: {a_character["health_points"]}')
            logger.info(
                f'Character: {b_character["name"]}, Initial HP: {b_character["health_points"]}')

            a_attack = random_attack(a_character['intelligence'],
                                     a_character['speed'],
                                     a_character['combat'],
                                     a_character['strength'],
                                     a_character['durability'],
                                     a_character['power'],
                                     a_character['fb']
                                     )
            b_attack = random_attack(b_character['intelligence'],
                                     b_character['speed'],
                                     b_character['combat'],
                                     b_character['strength'],
                                     b_character['durability'],
                                     b_character['power'],
                                     b_character['fb']
                                     )

            a_character['health_points'] -= b_attack['value']
            b_character['health_points'] -= a_attack['value']

            logger.info(
                f'Character: {a_character["name"]}, Type Attack: {a_attack["type"]}, Attack Value: {a_attack["value"]}')
            logger.info(
                f'Character: {b_character["name"]}, Type Attack: {b_attack["type"]}, Attack Value: {b_attack["value"]}')

            logger.info(
                '-----------------------------------------------------------------------')

            if a_character['health_points'] <= 0:
                self.a_team['characters'].pop(0)
                if not self.a_team['characters']:
                    winner = 'b_team'
            if b_character['health_points'] <= 0:
                self.b_team['characters'].pop(0)
                if not self.b_team['characters']:
                    winner = 'a_team'

        return self.a_team, self.b_team, winner


class SimulateBattle(View):
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        battle = Battle(body['a_team'], body['b_team'])
        a_team, b_team, winner = battle.run_battle()
        return JsonResponse({
            'a_team': a_team,
            'b_team': b_team,
            'winner': winner
        })


class BattleSimulatorTest(View):
    def get(self, request, *args, **kwargs):
        logger.info('Generating teams')
        a_team, b_team = generate_teams()
        logger.info('Teams generated')
        battle = Battle(a_team, b_team)
        a_team, b_team, winner = battle.run_battle()

        return JsonResponse({
            'a_team': a_team,
            'b_team': b_team,
            'winner': winner
        })


class GenerateTeams(View):
    def get(self, request, *args, **kwargs):
        logger.info('Generating teams')
        a_team, b_team = generate_teams()
        logger.info('Teams generated')
        return JsonResponse({
            'a_team': a_team,
            'b_team': b_team,
        })

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from utilities import generate_teams, random_attack
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create your views here.


class BattleSimulator(View):
    def get(self, request, *args, **kwargs):
        logger.info('Generating teams')
        a_team, b_team = generate_teams()
        logger.info('Teams generated')
        winner = ''

        while a_team['characters'] and b_team['characters']:
            a_character = a_team['characters'][0]
            b_character = b_team['characters'][0]
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
                a_team['characters'].pop(0)
                if not a_team['characters']:
                    winner = 'b_team'
            if b_character['health_points'] <= 0:
                b_team['characters'].pop(0)
                if not b_team['characters']:
                    winner = 'a_team'

        return JsonResponse({
            'a_team': a_team,
            'b_team': b_team,
            'winner': winner
        })

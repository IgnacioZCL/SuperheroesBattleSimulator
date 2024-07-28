import logging
from utilities.utilities import random_attack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Create your views here.


class Battle():
    def __init__(self, a_team, b_team):
        self.a_team = a_team
        self.b_team = b_team

    def run_battle(self):
        logger.info('Simulating battle')
        winner = ''
        battle_logs = []
        while self.a_team['characters'] and self.b_team['characters']:
            a_character = self.a_team['characters'][0]
            b_character = self.b_team['characters'][0]

            battle_log = {
                'a_character_name': a_character['name'],
                'a_character_hp': a_character['health_points'],
                'b_character_name': b_character['name'],
                'b_character_hp':  b_character['health_points']
            }

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

            battle_log.update({
                'a_attack_type': a_attack["type"],
                'a_attack_points': a_attack["value"],
                'b_attack_type': b_attack["type"],
                'b_attack_points': b_attack["value"],
            })
            battle_logs.append(battle_log)

            if a_character['health_points'] <= 0:
                self.a_team['characters'].pop(0)
                if not self.a_team['characters']:
                    winner = 'b_team'
            if b_character['health_points'] <= 0:
                self.b_team['characters'].pop(0)
                if not self.b_team['characters']:
                    winner = 'a_team'

        return self.a_team, self.b_team, winner, battle_logs

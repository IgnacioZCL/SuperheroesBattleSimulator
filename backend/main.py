from fastapi import FastAPI, Request
from utilities.utilities import generate_teams, random_attack
from fastapi.middleware.cors import CORSMiddleware
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate_teams/")
async def generate_teams_endpoint():
    logger.info('Generating teams')
    a_team, b_team = generate_teams()
    logger.info('Teams generated')

    return {
        "a_team": a_team,
        "b_team": b_team
    }


@app.post("/simulate_battle/")
async def simulate_battle_endpoint(request: Request):
    body = await request.json()
    battle = Battle(body['a_team'], body['b_team'])
    a_team, b_team, winner = battle.run_battle()
    return {
        'a_team': a_team,
        'b_team': b_team,
        'winner': winner
    }


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

from fastapi import FastAPI, Request
from utilities.utilities import generate_teams, random_attack
from fastapi.middleware.cors import CORSMiddleware
import logging
import requests

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
    a_team, b_team, winner, battle_logs = battle.run_battle()
    return {
        'a_team': a_team,
        'b_team': b_team,
        'winner': winner,
        'battle_logs': battle_logs
    }


@app.post("/send_battle/")
async def send_battle_email(request: Request):
    body = await request.json()

    response = requests.post(
        "https://api.mailgun.net/v3/sandboxae28c4bcd41b4411993ab4b53e2caa61.mailgun.org/messages",
        auth=("api", "d1bd7548c4f61829bb3f1dea4e3b07e0-0f1db83d-aa94cad1"),
        data={"from": "Excited User <ignacio.f.zuniga@gmail.com>",
                      "to": [body['receiver']],
                      "subject": "Resumen de la pelea de personajes",
              "html": body['battle_summary']})
    return {'message': 'success'}


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

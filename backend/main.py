from fastapi import FastAPI, Request
from utilities.utilities import generate_teams
from utilities.battle import Battle
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

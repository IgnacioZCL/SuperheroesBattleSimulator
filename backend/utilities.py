from random import randint, sample
from superheroes_api import SuperheroesAPI


def get_hp(strength, durability, power, stamina):
    return (((strength * 0.8 + durability * 0.7 + power) / 2) * (1 + (stamina/10))) + 100


def get_stats(base, stamina, fb):
    return ((2 * base + stamina) / 1.1) * fb


def generate_stamina():
    return randint(0, 10)


# Filiation Coefficient
def get_fb(alignment_team, alignment_character):
    return 1 + randint(0, 9) if alignment_team == alignment_character else (1 + randint(0, 9)) ** -1


def mental_attack(intelligence, speed, combat, fb):
    return (intelligence * 0.7 + speed * 0.2 + combat * 0.1) * fb


def strong_attack(strength, power, combat, fb):
    return (strength * 0.6 + power * 0.2 + combat * 0.2) * fb


def fast_attack(speed, durability, strength, fb):
    return (speed * 0.55 + durability * 0.5 + strength * 0.2) * fb


def random_attack(intelligence, speed, combat, strength, durability, power, fb):
    attack_type = randint(1, 3)

    if attack_type == 1:
        return {
            'type': 'Mental Attack',
            'value': round(mental_attack(intelligence, speed, combat, fb))
        }
    if attack_type == 2:
        return {
            'type': 'Strong Attack',
            'value': round(strong_attack(strength, power, combat, fb))
        }
    if attack_type == 3:
        return {
            'type': 'Fast Attack',
            'value': round(fast_attack(speed, durability, strength, fb))
        }


def stats_configuration(team):
    individual_alignment = [character['alignment'] for character in team]
    team_data = {
        'characters': team,
        'alignment': max(set(individual_alignment), key=individual_alignment.count)
    }
    for character in team:
        stamina = generate_stamina()
        fb = get_fb(team_data['alignment'], character['alignment'])
        character['intelligence'] = round(
            get_stats(character['intelligence'], stamina, fb))
        character['strength'] = round(
            get_stats(character['strength'], stamina, fb))
        character['speed'] = round(get_stats(character['speed'], stamina, fb))
        character['combat'] = round(
            get_stats(character['combat'], stamina, fb))
        character['power'] = round(get_stats(character['power'], stamina, fb))
        character['durability'] = round(get_stats(
            character['durability'], stamina, fb))
        character['health_points'] = round(get_hp(
            character['strength'], character['durability'], character['power'], stamina))
        character['fb'] = fb
    return team_data


def generate_teams():
    shapi = SuperheroesAPI()
    teams = []

    for character_id in sample(range(1, 732), 10):
        character_data = shapi.get_character_data(character_id)
        character = {
            'id': character_id,
            'name': character_data['name'],
            'intelligence': int(character_data['powerstats']['intelligence']) if character_data['powerstats']['intelligence'] != 'null' else 0,
            'strength': int(character_data['powerstats']['strength']) if character_data['powerstats']['strength'] != 'null' else 0,
            'speed': int(character_data['powerstats']['speed']) if character_data['powerstats']['speed'] != 'null' else 0,
            'combat': int(character_data['powerstats']['combat']) if character_data['powerstats']['combat'] != 'null' else 0,
            'power': int(character_data['powerstats']['power']) if character_data['powerstats']['power'] != 'null' else 0,
            'durability': int(character_data['powerstats']['durability']) if character_data['powerstats']['durability'] != 'null' else 0,
            'alignment': character_data['biography']['alignment'],
            'image': character_data['image']['url']
        }
        teams.append(character)

    a_team = teams[:5]
    b_team = teams[5:]
    a_team = stats_configuration(a_team)
    b_team = stats_configuration(b_team)
    return a_team, b_team

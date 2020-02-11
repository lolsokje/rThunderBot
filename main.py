#! /usr/local/bin/python3

import pytz
import requests
from Client import Client
from datetime import datetime

BASE_API_URL = 'https://data.nba.net/prod/v1/'

client = None
subs = {}


def init():
    global client
    nicknames_to_sub_links()
    url = BASE_API_URL + 'today.json'
    json_result = parse_json(url)
    season_details = json_result['teamSitesOnly']
    client = Client(season_details, 'lolsokje')


def get_conference_standings(conference):
    url = BASE_API_URL + 'current/standings_conference.json'
    result = parse_json(url)
    conference = result['league']['standard']['conference'][conference]

    standings_string = """|#|TEAM|W|L|PCT|GB
|-|-|-|-|-|-|
    """

    for team in conference:
        rank = team['confRank']
        nick_name = team['teamSitesOnly']['teamNickname']
        wins = team['win']
        losses = team['loss']
        pct = team['winPct']
        gb = team['gamesBehind']
        sub = subs[nick_name]

        if nick_name == 'Thunder':
            string = f"**{rank}** | {sub} **{nick_name}** | **{wins}** | **{losses}** | **{pct}** | **{gb}**\n"
        else:
            string = f"{rank} | {sub} {nick_name} | {wins} | {losses} | {pct} | {gb}\n"
        standings_string = standings_string + string

    return standings_string


def get_roster():
    url = f"{BASE_API_URL}{client.season_year}/players.json"
    players = parse_json(url)
    players = players['league']['standard']

    output = [x for x in players if x['teamId'] == client.team_id]

    roster_dict = {}

    for player in output:
        first_name = player['firstName']
        last_name = player['lastName']
        jersey_number = player['jersey']
        pos = player['pos']
        college = player['collegeName']
        country = player['country']

        roster_dict[int(jersey_number)] = {
            'name': f"{first_name} {last_name}",
            'pos': pos,
            'college': college,
            'country': country
        }

    roster_string = """No | Name | Pos. | College
        -|-|-|-
        """

    for key in sorted(roster_dict):
        player = roster_dict[key]
        affiliation = f"{player['college']}"

        if player['college'] == ' ':
            affiliation = f"*{player['country']}*"

        roster_string = roster_string + f"{key} | {player['name']} | {player['pos']} | {affiliation}\n"

    return roster_string


def parse_json(url):
    return requests.get(url).json()


def nicknames_to_sub_links():
    global subs
    nicknames = ['76ers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat', 'Hornets',
                 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers', 'Pelicans',
                 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Timberwolves', 'Trail Blazers',
                 'Warriors', 'Wizards']

    subs = ['[](/r/sixers)', '[](/r/mkebucks)', '[](/r/chicagobulls)', '[](/r/clevelandcavs)', '[](/r/bostonceltics)',
            '[](/r/laclippers)', '[](/r/memphisgrizzlies)', '[](/r/atlantahawks)', '[](/r/heat)',
            '[](/r/charlottehornets)', '[](/r/utahjazz)', '[](/r/kings)', '[](/r/nyknicks)', '[](/r/lakers)',
            '[](/r/orlandomagic)', '[](/r/mavericks)', '[](/r/gonets)', '[](/r/denvernuggets)', '[](/r/pacers)',
            '[](/r/nolapelicans)', '[](/r/detroitpistons)', '[](/r/torontoraptors)', '[](/r/rockets)',
            '[](/r/nbaspurs)', '[](/r/suns)', '[](/r/thunder)', '[](/r/timberwolves)', '[](/r/ripcity)',
            '[](/r/warriors)', '[](/r/washingtonwizards)']

    ret = {}

    for nickname, sub in zip(nicknames, subs):
        ret[nickname] = sub

    subs = ret


if __name__ == '__main__':
    init()
    roster = get_roster()
    standings = get_conference_standings('west')
    client.update_sidebar(standings, roster)

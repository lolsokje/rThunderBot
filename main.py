#! /usr/local/bin/python3

import pytz
import sys
import requests
import time
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

    standings = """|#|TEAM|W|L|PCT|GB
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
        standings = standings + string

    return standings


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
    standings = get_conference_standings('west')
    client.update_sidebar(standings)

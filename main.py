#! /usr/local/bin/python3

import pytz
import requests
from Client import Client
from datetime import datetime

BASE_API_URL = 'https://data.nba.net/prod/v1/'

client = None
subs = {}
teams = {}


def init() -> None:
    global client
    nicknames_to_sub_links()
    url = BASE_API_URL + 'today.json'
    json_result = parse_json(url)
    season_details = json_result['teamSitesOnly']
    client = Client(season_details, 'lolsokje')
    team_ids_to_nicknames()


def get_conference_standings(conference: str) -> str:
    url = BASE_API_URL + 'current/standings_conference.json'
    result = parse_json(url)
    conference = result['league']['standard']['conference'][conference]

    standings_string = """###WESTERN CONFERENCE STANDINGS
    # | TEAM | WIN | LOSS | PCT | GB
        -|-|-|-|-|-
        """

    for team in conference:
        rank = team['confRank']
        nick_name = team['teamSitesOnly']['teamNickname']
        wins = team['win']
        losses = team['loss']
        pct = team['winPct']
        gb = team['gamesBehind']
        sub = subs[nick_name]

        if nick_name == client.team_nick_name:
            string = f"**{rank}** | {sub} **{nick_name}** | **{wins}** | **{losses}** | **{pct}** | **{gb}**\n"
        else:
            string = f"{rank} | {sub} {nick_name} | {wins} | {losses} | {pct} | {gb}\n"
        standings_string = standings_string + string

    return standings_string


def get_roster() -> str:
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

    roster_string = """###THUNDER ROSTER
    NO | NAME | POS | COLLEGE
        -|-|-|-
        """

    for key in sorted(roster_dict):
        player = roster_dict[key]
        affiliation = f"{player['college']}"

        if player['college'] == ' ':
            affiliation = f"*{player['country']}*"

        roster_string = roster_string + f"{key} | {player['name']} | {player['pos']} | {affiliation}\n"

    return roster_string


def get_schedule() -> str:
    url = f"{BASE_API_URL}{client.season_year}/teams/{client.team_id}/schedule.json"
    res = parse_json(url)
    games = res['league']['standard']
    current_month = datetime.strftime(datetime.today(), '%b')
    current_month_long = datetime.strftime(datetime.today(), '%B')

    central = pytz.timezone('US/Central')
    utc = pytz.utc

    schedule_string = f"""###THUNDER {current_month_long.upper()} SCHEDULE
    DATE | TEAM | LOCATION | RESULT
    -|-|-|-|-
    """

    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    for game in games:
        if game['seasonStageId'] == client.season_stage:
            start_utc = datetime.strptime(game['startTimeUTC'], fmt).replace(tzinfo=utc)
            start_central = start_utc.astimezone(central)
            start_date = start_central.strftime('%b %d')

            if current_month == start_central.strftime('%b'):
                if game['statusNum'] == 3:
                    home_score = int(game['hTeam']['score'])
                    away_score = int(game['vTeam']['score'])

                    if game['isHomeTeam']:
                        win_loss = 'W' if home_score > away_score else 'L'
                        score = f"{away_score} - **{home_score}**"
                    else:
                        win_loss = 'L' if home_score > away_score else 'W'
                        score = f"**{away_score}** - {home_score}"
                    result = f"[**{win_loss}** {score}](https://stats.nba.com/game/{game['gameId']})"
                else:
                    result = start_central.strftime('%-I:%M %p')

                location = "HOME" if game['isHomeTeam'] else "AWAY"
                opponent_id = game['vTeam']['teamId'] if game['isHomeTeam'] else game['hTeam']['teamId']
                nickname = teams[opponent_id]
                sub = subs[nickname]

                string = f"{start_date} | {sub} {nickname} | {location} | {result}\n"

                schedule_string = schedule_string + string

    return schedule_string


def parse_json(url: str):
    return requests.get(url).json()


def nicknames_to_sub_links() -> None:
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


def team_ids_to_nicknames() -> None:
    global teams
    url = f"{BASE_API_URL}/{client.season_year}/teams.json"
    teams_json = parse_json(url)
    teams = teams_json['league']['standard']

    ret = {}

    for team in teams:
        if team['isNBAFranchise']:
            team_id = team['teamId']
            ret[team_id] = team['nickname']

    teams = ret


if __name__ == '__main__':
    init()
    schedule = get_schedule()
    roster = get_roster()
    standings = get_conference_standings('west')
    client.update_sidebar(schedule, standings, roster)

import requests
from nba_api.stats.endpoints import leaguestandingsv3
from nickname_converter import NicknameConverter
import json

TEAM_ID = 1610612760

TEAM_INDEX = 3
TEAM_NAME_INDEX = 4
CONFERENCE_INDEX = 6
RANK_INDEX = 8
WIN_INDEX = 13
LOSS_INDEX = 14
PCT_INDEX = 15
GB_INDEX = 88


class StandingsBuilder:
    def __init__(self, nickname_converter):
        self.standings_string = """###WESTERN CONFERENCE STANDINGS
 # | TEAM | WIN | LOSS | PCT | GB
-|-|-|-|-|-
"""
        self.nickname_converter = nickname_converter

    def build_standings(self):
        standings = json.loads(leaguestandingsv3.LeagueStandingsV3().get_json())
        teams = standings['resultSets'][0]['rowSet']

        for team in teams:
            if team[CONFERENCE_INDEX] != 'West':
                continue

            team_name = team[TEAM_NAME_INDEX]
            sub = self.nickname_converter.convert_name(team_name)

            if TEAM_ID == team[TEAM_INDEX]:
                row =f"{team[RANK_INDEX]} | {sub} {team_name} | {team[WIN_INDEX]} | {team[LOSS_INDEX]} | {team[PCT_INDEX]} | {team[GB_INDEX]}\n"
            else:
                row = f"{team[RANK_INDEX]} | {sub} {team_name} | {team[WIN_INDEX]} | {team[LOSS_INDEX]} | {team[PCT_INDEX]} | {team[GB_INDEX]}\n"

            self.standings_string = self.standings_string + row

        return self.standings_string

from nba_api.stats.endpoints import commonteamroster
import json

NAME = 3
NUMBER = 6
POSITION = 7


class RosterBuilder:
    def __init__(self):
        self.roster_string = """###THUNDER ROSTER
 # | NAME | POS
    -|-|-|-
    """

    def build_roster(self):
        roster = json.loads(commonteamroster.CommonTeamRoster(team_id='1610612760').get_json())

        players = roster['resultSets'][0]['rowSet']

        for player in players:
            self.roster_string = self.roster_string + f"{player[NUMBER]} | {player[NAME]} | {player[POSITION]}\n"

        return self.roster_string

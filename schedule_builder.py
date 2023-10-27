import requests
from datetime import datetime
import calendar
from nickname_converter import NicknameConverter


TEAM_ID = 1610612760
TODAY = datetime.today()
MONTH_NUMBER = TODAY.month
MONTH_NAME = calendar.month_name[MONTH_NUMBER]


def get_schedule():
    response = requests.get('https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json')
    json_data = response.json()

    return json_data['leagueSchedule']['gameDates']


class ScheduleBuilder:
    def __init__(self, nickname_converter):
        self.schedule_string = f"""###THUNDER {MONTH_NAME.upper()} SCHEDULE
        DATE | TEAM | LOCATION | RESULT
        -|-|-|-|-
        """
        self.nickname_converter = nickname_converter

    def build_schedule(self):
        schedule = get_schedule()

        for gameDate in schedule:
            date = datetime.strptime(gameDate['gameDate'], '%m/%d/%Y %H:%M:%S')

            if date.month != MONTH_NUMBER:
                continue

            for game in gameDate['games']:
                if game['homeTeam']['teamId'] != TEAM_ID and game['awayTeam']['teamId'] != TEAM_ID:
                    continue

                game_date = date.strftime('%b %-d')

                home_team = game['homeTeam']
                away_team = game['awayTeam']

                is_home_team = home_team['teamId'] == TEAM_ID

                opponent = away_team['teamName'] if is_home_team else home_team['teamName']
                sub = self.nickname_converter.convert_name(opponent)

                location = 'HOME' if is_home_team else 'AWAY'

                if game['gameStatus'] == 3:
                    away_score = int(away_team['score'])
                    home_score = int(home_team['score'])

                    if is_home_team:
                        win_loss = 'W' if home_score > away_score else 'L'
                        score = f"{away_score} - **{home_score}**"
                    else:
                        win_loss = 'L' if home_score > away_score else 'W'
                        score = f"**{away_score}** - {home_score}"

                    result = f"[**{win_loss}** {score}](https://nba.com/game/{game['gameId']})"
                else:
                    time = game['homeTeamTime'] if is_home_team else game['awayTeamTime']
                    time = datetime.fromisoformat(time)
                    result = time.time().strftime('%-I:%M %p')

                self.schedule_string = self.schedule_string + f"{game_date} | {sub} {opponent} | {location} | {result}\n"

        return self.schedule_string


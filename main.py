from roster_builder import RosterBuilder
from schedule_builder import ScheduleBuilder
from standings_builder import StandingsBuilder
from nickname_converter import NicknameConverter
import praw
import conf

IMPORTANT_LINKS = """### **Important links**
* [Rules](https://www.reddit.com/r/Thunder/wiki/rules)
* [Message the mods](https://www.reddit.com/message/compose?to=%2Fr%2FThunder)
* [Thunder Twitter](https://twitter.com/okcthunder)
* [Thunder Facebook](https://www.facebook.com/OKCThunder)
    \n"""


class ThunderBot:
    def __init__(self):
        converter = NicknameConverter()
        self.roster_builder = RosterBuilder()
        self.schedule_builder = ScheduleBuilder(converter)
        self.standings_builder = StandingsBuilder(converter)

        subreddit_name = 'thunder'
        self.reddit = praw.Reddit(client_id=conf.settings['client_id'],
                                  client_secret=conf.settings['client_secret'],
                                  password=conf.settings['password'],
                                  user_agent=conf.settings['user_agent'],
                                  username=conf.settings['username'])

        sub = self.reddit.subreddit(subreddit_name)
        self.mod = sub.mod
        self.settings = self.mod.settings()
        self.description = self.settings['description']

    def build_sidebar(self):
        roster = self.roster_builder.build_roster()
        schedule = self.schedule_builder.build_schedule()
        standings = self.standings_builder.build_standings()

        return f"{IMPORTANT_LINKS}\n{schedule}\n{standings}\n{roster}"

    def update_sidebar(self, sidebar_content: str):
        first_line = self.description.partition('\n')[0]
        sidebar_text = f"{first_line}\n" if first_line.startswith('####') else ''
        sidebar_text = f"{sidebar_text}{sidebar_content}"

        self.mod.update(description=sidebar_text)


if __name__ == '__main__':
    thunderBot = ThunderBot()

    sidebar = thunderBot.build_sidebar()
    thunderBot.update_sidebar(sidebar)

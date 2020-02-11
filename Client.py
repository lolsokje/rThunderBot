import requests
import praw
import conf


class Client(object):
    def __init__(self, season_details, sub):
        self.team_id = '1610612760'
        self.team_name = 'Oklahoma City'
        self.team_nick_name = 'Thunder'
        self.season_stage = season_details['seasonStage']
        self.season_year = season_details['seasonYear']
        self.reddit = praw.Reddit(client_id=conf.settings['client_id'],
                                  client_secret=conf.settings['client_secret'],
                                  password=conf.settings['password'],
                                  user_agent=conf.settings['user_agent'],
                                  username=conf.settings['username'])

        sub = self.reddit.subreddit(sub)
        self.mod = sub.mod

    def update_sidebar(self, standings):
        print(standings)
        self.mod.update(description=standings)

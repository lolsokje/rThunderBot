class NicknameConverter:
    def __init__(self):
        names = ['76ers', 'Bucks', 'Bulls', 'Cavaliers', 'Celtics', 'Clippers', 'Grizzlies', 'Hawks', 'Heat',
                     'Hornets', 'Jazz', 'Kings', 'Knicks', 'Lakers', 'Magic', 'Mavericks', 'Nets', 'Nuggets', 'Pacers',
                     'Pelicans', 'Pistons', 'Raptors', 'Rockets', 'Spurs', 'Suns', 'Thunder', 'Timberwolves',
                     'Trail Blazers', 'Warriors', 'Wizards']

        subs = ['[](/r/sixers)', '[](/r/mkebucks)', '[](/r/chicagobulls)', '[](/r/clevelandcavs)',
                '[](/r/bostonceltics)',
                '[](/r/laclippers)', '[](/r/memphisgrizzlies)', '[](/r/atlantahawks)', '[](/r/heat)',
                '[](/r/charlottehornets)', '[](/r/utahjazz)', '[](/r/kings)', '[](/r/nyknicks)', '[](/r/lakers)',
                '[](/r/orlandomagic)', '[](/r/mavericks)', '[](/r/gonets)', '[](/r/denvernuggets)', '[](/r/pacers)',
                '[](/r/nolapelicans)', '[](/r/detroitpistons)', '[](/r/torontoraptors)', '[](/r/rockets)',
                '[](/r/nbaspurs)', '[](/r/suns)', '[](/r/thunder)', '[](/r/timberwolves)', '[](/r/ripcity)',
                '[](/r/warriors)', '[](/r/washingtonwizards)']

        self.nicknames = {}

        for nickname, sub in zip(names, subs):
            self.nicknames[nickname] = sub

    def convert_name(self, name):
        return self.nicknames[name]

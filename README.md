# rThunderBot
A bot for the /r/Thunder subreddit

## Requirements
The bot is written with Python 3 in mind, so make sure you've got that version installed.

Other dependencies are;
- praw
- pytz

If you don't have these packages installed, install them with `pip3 install [package]`

## Setup
In order to use the bot, you need to add a `conf.py` file in the same directory as `main.py`, with this structure;

```
settings = dict(
    client_id='',
    client_secret='',
    password='',
    username='',
    user_agent=''
)
```

If you're unsure about what to enter where, please refer to the [PRAW](https://praw.readthedocs.io/en/latest/getting_started/authentication.html) documentation. 

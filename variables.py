import os
from dotenv import load_dotenv

import instaloader
from instaloader import *

import re
import requests
import traceback # to print error traceback
import telebot

import json
import urllib.parse

# we use dotenv to use os.getenv() instead of os.environ[]
# and read from '.env' in current folder instead of '/etc/environment'
# more guide:
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
load_dotenv()

# env variables
bot_token = os.getenv('BEST_INSTAGRAM_DOWNLOADER_BOT_API')
log_channel_id = os.getenv('INSTAGRAM_DOWNLOADER_LOG_CHANNEL_ID') # set to False if not needed

# initialize bot
bot = telebot.TeleBot(bot_token)

# settings
bot_username = "@Best_Instagram_Downloader_Bot"
caption_trail = "\n\n\n" + bot_username
session_file_name = "session" # any name change should apply to .gitignore too

# warp socks proxy
warp_proxies = os.environ["WARP_PROXIES"]
warp_proxies = json.loads(warp_proxies)

# regex
insta_post_or_reel_reg = r'(?:https?://www\.)?instagram\.com\S*?/(p|reel)/([a-zA-Z0-9_-]{11})/?'
spotify_link_reg = r'(?:https?://)?open\.spotify\.com/(track|album|playlist|artist)/[a-zA-Z0-9]+'

# messages
start_msg = '''Hi😃👋
Send an instagram link to download.

It can be a post link like this:
https://www.instagram.com/p/DFx\_jLuACs3

Or it can be a reel link like this:
https://www.instagram.com/reel/C59DWpvOpgF'''

help_msg = '''This bot is open source and you are welcome to contribute and improve it.
https://github.com/arashnm80/best-instagram-downloader

You can give me energy by giving a star in github'''

privacy_msg = '''This bot doesn't gather any info from the users.

Also it's whole open source and available here:
https://github.com/arashnm80/best-instagram-downloader'''

end_msg = '''If you liked the bot you can support me by giving a star [here](https://github.com/arashnm80/best-instagram-downloader)⭐ (it's free)

You can also check out my *Music Downloader* too: @SpotSeekBot'''

fail_msg = '''Sorry, my process wasn't successful.
But you can try again another time or with another link.'''

wrong_pattern_msg = '''wrong pattern.
You should send an instagram post or reel link.'''

reel_msg = '''reel links are not supported at the moment.
You can send post links instead.

Motivate me to add support of reels and stories by subscribing to [my youtube](https://www.youtube.com/@Arashnm80)'''

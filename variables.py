import os
from dotenv import load_dotenv

# we use dotenv to use os.getenv() instead of os.environ[]
# and read from '.env' in current folder instead of '/etc/environment'
# more guide:
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
load_dotenv()

# instagram user for instaloader
USER = os.getenv('INSTAGRAM_USER_1') # to read from .env file
PASS = os.getenv('INSTAGRAM_PASS_1')

# env variables
bot_token = os.getenv('BEST_INSTAGRAM_DOWNLOADER_BOT_API')
log_channel_id = os.getenv('LOG_CHANNEL_ID') # set to False if not needed

# settings
session_file_name = "session" # any name change should apply to .gitignore too

# regex
# insta_post_reg = r'(?:https?://www\.)?instagram\.com\S*?/p/(\w{11})/?'
insta_post_reg = r'(?:https?://www\.)?instagram\.com\S*?/p/([a-zA-Z0-9-]{11})/?'
insta_correct_link_reg = insta_post_reg # story can be added later
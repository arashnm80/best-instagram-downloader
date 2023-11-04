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
bot_username = "@Best_Instagram_Downloader_Bot"
caption_trail = "\n\n\n" + bot_username
session_file_name = "session" # any name change should apply to .gitignore too

# regex
insta_post_reg = r'(?:https?://www\.)?instagram\.com\S*?/p/([a-zA-Z0-9_-]{11})/?'
insta_story_reg = r'(?:https?://www\.)?instagram\.com\S*?/p/([a-zA-Z0-9_-]{11})/?'
insta_correct_link_reg = insta_post_reg # story can be added later

# messages
start_msg = '''Welcome :)
Send a post link to download.'''

help_msg = '''This bot is open source and you are welcome to contribute and improve it.
https://github.com/arashnm80/best-instagram-downloader

You can give me energy by giving a star in github :)'''

end_msg = '''You can check out my spotify downloader bot too: @SpotSeekBot

Subscribe to [my youtube](https://www.youtube.com/@Arashnm80) for more...'''

fail_msg = '''Sorry, my process wasn't successful.
But you can try again another time or with another link.'''

wrong_pattern_msg = '''wrong pattern.
Currently only post links are supported.

Motivate me to add support of reels and stories by subscribing to [my youtube](https://www.youtube.com/@Arashnm80)'''
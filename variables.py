import os

# instagram user for instaloader
USER = os.environ['INSTAGRAM_USER_1']
PASS = os.environ['INSTAGRAM_PASS_1']

# env variables
bot_token = os.environ['BEST_INSTAGRAM_DOWNLOADER_BOT_API']
log_channel_id = os.environ['LOG_CHANNEL_ID']


# settings
session_file_name = "session" # any name change should apply to .gitignore too

# regex
insta_post_reg = r'(?:https?://www\.)?instagram\.com\S*?/p/(\w{11})/?'
insta_correct_link_reg = insta_post_reg # story can be added later
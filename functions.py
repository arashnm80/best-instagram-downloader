from variables import *

import instaloader
from instaloader import *

import re
import requests

import telebot
# from telebot import types

def log(log_message):
    if not log_channel_id:
        return # set to False log channel means it is not needed

    log_bot_url = "https://api.telegram.org/bot" + bot_token + "/"

    log = requests.post(log_bot_url + "sendMessage", data={
        "chat_id": log_channel_id,
        "text": log_message
    })
    
    # Check if the log was sent successfully
    if log.status_code == 200:
        print('log registered')
    else:
        print('Error in registering log:', log.status_code)

def try_to_delete_message(chat_id, message_id):
    # initialize bot
    bot = telebot.TeleBot(bot_token)

    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass # ignore errors if user has already deleted the message

def get_ready_to_work_insta_instance():
    # create instance
    L = instaloader.Instaloader()

    # prepare session
    try:
        L.load_session_from_file(USER, session_file_name) # (load session created w/
                                    #  `instaloader -l USERNAME`)
    except:
        L.login(USER, PASS)
        print("new login")
        L.save_session_to_file(session_file_name)
        print("save to a new session")
    
    return L

def download_post_to_folder(post_shortcode, folder):
    L = get_ready_to_work_insta_instance()
    post = Post.from_shortcode(L.context, post_shortcode)
    L.download_post(post, target=folder)

def get_post_shortcode_from_link(link):
    match = re.search(insta_post_reg, link)
    if match:
        return match.group(1)
    else:
        return False
from variables import *

import instaloader
from instaloader import *

import re
import requests
import telebot

def log(log_message):
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

def get_ready_to_work_insta_instance():
    # create instance
    L = instaloader.Instaloader()

    # prepare session
    try:
        print("restore session")
        L.load_session_from_file(USER, session_file_name) # (load session created w/
                                    #  `instaloader -l USERNAME`)
    except:
        print("new login")
        L.login(USER, PASS)
        L.save_session_to_file(session_file_name)
    
    return L

def download_post_to_folder(post_id, folder):
    L = get_ready_to_work_insta_instance
    post = Post.from_shortcode(L.context, post_id)
    L.download_post(post, target=folder)

def get_post_id_from_link(link):
    match = re.search(insta_post_reg, link)
    if match:
        print(match.group(1))
    else:
        return False
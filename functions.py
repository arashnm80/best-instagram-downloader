from variables import *



# # classes (for rate limiting - might delete them)

# class MyCustomException(Exception):
#     def __init__(self, message="Custom rate limit exceeded"):
#         self.message = message
#         super().__init__(self.message)

# class MyRateController(instaloader.RateController):
#     def sleep(self, secs):
#         raise MyCustomException("Custom rate limit exceeded")


# functions

def log(log_message):
    if not log_channel_id:
        return # set to False log channel means it is not needed

    log_bot_url = "https://api.telegram.org/bot" + bot_token + "/"

    log = requests.post(log_bot_url + "sendMessage", data={
        "chat_id": log_channel_id,
        "text": log_message
    }, proxies=warp_proxies)
    
    # Check if the log was sent successfully
    if log.status_code == 200:
        print('log registered')
    else:
        print('Error in registering log:', log.status_code)

def try_to_delete_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass # ignore errors if user has already deleted the message

# def get_ready_to_work_insta_instance():
#     # #  (for rate limiting - might delete it)
#     # L = instaloader.Instaloader(rate_controller=lambda ctx: MyRateController(ctx))
    
#     # create instance
#     L = instaloader.Instaloader()

#     # prepare session
#     try:
#         L.load_session_from_file(USER, session_file_name) # gives error if file doesn't exist
#         print(L.test_login()) # gives error if session is expired
#         print("using old session")
#     except:
#         log("session failed")
#         print("session failed")
#         #### commented for debug
#         # if os.path.exists(session_file_name):
#         #     os.remove(session_file_name) # delete older session if it file exists
#         # L.login(USER, PASS)
#         # log("new login with instagram bot")
#         # L.save_session_to_file(session_file_name)
#         # print("save to a new session")
#         ####
    

#     return L

# def download_post_to_folder(post_shortcode, folder):
#     L = get_ready_to_work_insta_instance()
#     post = Post.from_shortcode(L.context, post_shortcode)
#     L.download_post(post, target=folder)

def get_post_or_reel_shortcode_from_link(link):
    match = re.search(insta_post_or_reel_reg, link)
    if match:
        return match.group(2)
    return False

def get_post_or_reel_info_from_link(link):
    match = re.search(insta_post_or_reel_reg, link)
    if match:
        return match.group(2), match.group(1)
    return False, False

def download_media_bytes(url, retries=3):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.instagram.com/",
    }
    last_error = None
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                stream=True,
                proxies=warp_proxies,
                headers=headers,
                timeout=45,
            )
            if response.status_code == 200:
                return response.content
            last_error = f"status {response.status_code}"
        except requests.RequestException as exc:
            last_error = str(exc)
    raise RuntimeError(f"download failed after {retries} attempts: {last_error}")

from functions import *

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, start_msg, parse_mode="Markdown", disable_web_page_preview=True)
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nstart command")

@bot.message_handler(commands=['help'])
def help_command_handler(message):
    bot.send_message(message.chat.id, help_msg, parse_mode="Markdown", disable_web_page_preview=True)
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nhelp command")

@bot.message_handler(regexp = insta_post_or_reel_reg)
def post_or_reel_link_handler(message):
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\npost link: {message.text}")
    try:
        guide_msg_1 = bot.send_message(message.chat.id, "Ok wait a few moments...")
        post_shortcode = get_post_or_reel_shortcode_from_link(message.text)
        print(post_shortcode)

        if not post_shortcode:
            log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nerror in getting post_shortcode")
            return # post shortcode not found

        L = get_ready_to_work_insta_instance()        
        post = Post.from_shortcode(L.context, post_shortcode)

        # caption handling
        new_caption = post.caption
        while len(new_caption) + len(caption_trail) > 1024:
            new_caption = new_caption[:-1] # remove last character
        new_caption = new_caption + caption_trail

        # handle post with single media
        if post.mediacount == 1:
            if post.is_video:
                bot.send_video(message.chat.id, post.video_url, caption=new_caption)
            else:
                bot.send_photo(message.chat.id, post.url, caption=new_caption)
            bot.send_message(message.chat.id, end_msg, parse_mode="Markdown", disable_web_page_preview=True)
            try_to_delete_message(message.chat.id, guide_msg_1.message_id)
            ### debug
            if os.path.exists(session_file_name):
                os.remove(session_file_name) # delete older session if it file exists
            L.save_session_to_file(session_file_name)
            print("save to a new session")
            ###
            return

        # handle post with multiple media
        media_list = []
        sidecars = post.get_sidecar_nodes()
        for s in sidecars:
            if s.is_video: # it's a video
                url = s.video_url
                media = telebot.types.InputMediaVideo(url)
                if not media_list: # first media of post
                    media = telebot.types.InputMediaVideo(url, caption=new_caption)
            else: # it's an image
                url = s.display_url
                media = telebot.types.InputMediaPhoto(url)
                if not media_list: # first media of post
                    media = telebot.types.InputMediaPhoto(url, caption=new_caption)
            media_list.append(media)
        bot.send_media_group(message.chat.id, media_list)
        bot.send_message(message.chat.id, end_msg, parse_mode="Markdown", disable_web_page_preview=True)
        try_to_delete_message(message.chat.id, guide_msg_1.message_id)
        ### debug
        if os.path.exists(session_file_name):
            os.remove(session_file_name) # delete older session if it file exists
        L.save_session_to_file(session_file_name)
        print("save to a new session")
        ###
        return
    except Exception as e:
        try_to_delete_message(message.chat.id, guide_msg_1.message_id)
        log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nerror in main body: {str(e)}")
        bot.send_message(message.chat.id, fail_msg, parse_mode="Markdown", disable_web_page_preview=True)
        traceback.print_exc() # print error traceback
        ### debug
        if os.path.exists(session_file_name):
            os.remove(session_file_name) # delete older session if it file exists
        L.save_session_to_file(session_file_name)
        print("save to a new session")
        ###


# @bot.message_handler(regexp = insta_reel_reg)
# def reel_link_handler(message):
#     log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nreel link: {message.text}")
#     bot.send_message(message.chat.id, reel_msg, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(func=lambda message: True)
def wrong_pattern_handler(message):
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nwrong pattern: {message.text}")
    bot.send_message(message.chat.id, wrong_pattern_msg, parse_mode="Markdown", disable_web_page_preview=True)

bot.infinity_polling()


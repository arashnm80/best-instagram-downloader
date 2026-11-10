from functions import *
from riad_azz import get_instagram_media_links

@bot.message_handler(commands=['start'])
def start_command_handler(message):
    bot.send_message(message.chat.id, start_msg, parse_mode="Markdown", disable_web_page_preview=True)
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nstart command")

@bot.message_handler(commands=['help'])
def help_command_handler(message):
    bot.send_message(message.chat.id, help_msg, parse_mode="Markdown", disable_web_page_preview=True)
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nhelp command")

@bot.message_handler(commands = ['privacy'])
def privacy_message_handler(message):
    bot.send_message(message.chat.id, privacy_msg, parse_mode="Markdown", disable_web_page_preview=True)
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\nprivacy command")

@bot.message_handler(regexp = spotify_link_reg)
def spotify_link_handler(message):
    bot.send_message(message.chat.id, "This bot only supports Instagram links. Please send an Instagram post or reel link.\n\nIf you want to download from Spotify you can check out my other bot: @SpotSeekBot")

@bot.message_handler(regexp = insta_post_or_reel_reg)
def post_or_reel_link_handler(message):
    try:
        log(f"{bot_username} log:\n\nuser:\n{message.chat.id}\n\n✅ message text:\n{message.text}")
        guide_msg_1 = bot.send_message(message.chat.id, "Ok wait a few moments...")
        post_shortcode, content_type = get_post_or_reel_info_from_link(message.text)
        print(post_shortcode, content_type)

        if not post_shortcode:
            log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\n🛑 error in getting post_shortcode")
            return # post shortcode not found

        media_links, caption = get_instagram_media_links(post_shortcode, content_type)
        
        # todo: fix later if possible and don't let it to happen in the first place
        # if they are both empty and the riad_azz returned this error:
        # "Error extracting media info: 'NoneType' object has no attribute 'get'"
        if (not media_links) and (not caption):
            raise Exception("riad_azz returned nothing")

        # caption handling
        if caption is None:
            caption = ''
        while len(caption) + len(caption_trail) > 1024:
            caption = caption[:-1]
        caption = caption + caption_trail

        media_list = []
        for idx, item in enumerate(media_links):
            url = item['url']
            try:
                file_content = download_media_bytes(url)
            except Exception as exc:
                log(f"a not ok file between files ({url[:80]}...): {exc}")
                continue

            is_video = item['type'] == 'video'
            file_bytes = io.BytesIO(file_content)
            file_bytes.name = f"file_{idx}.mp4" if is_video else f"file_{idx}.jpg"

            if is_video:
                if idx == 0:
                    media = telebot.types.InputMediaVideo(media=telebot.types.InputFile(file_bytes), caption=caption)
                else:
                    media = telebot.types.InputMediaVideo(media=telebot.types.InputFile(file_bytes))
            else:
                if idx == 0:
                    media = telebot.types.InputMediaPhoto(media=telebot.types.InputFile(file_bytes), caption=caption)
                else:
                    media = telebot.types.InputMediaPhoto(media=telebot.types.InputFile(file_bytes))

            media_list.append(media)

        if not media_list:
            raise Exception("all media downloads failed")

        def chunk_list(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        if len(media_list) == 1:
            media = media_list[0]
            if isinstance(media, telebot.types.InputMediaPhoto):
                bot.send_photo(message.chat.id, media.media, caption=media.caption)
            else:
                bot.send_video(message.chat.id, media.media, caption=media.caption)
        else:
            for chunk in chunk_list(media_list, 10):
                bot.send_media_group(message.chat.id, chunk)
        try_to_delete_message(message.chat.id, guide_msg_1.message_id)
        # # starpal promotion
        # if message.from_user.language_code == "fa":
        #     log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\n⭐️ starpal promotion for iranian user")
        #     bot.send_message(message.chat.id, starpal_promotion_msg, parse_mode="Markdown", disable_web_page_preview=False)
        #     return
        # normal end message
        bot.send_message(message.chat.id, end_msg, parse_mode="Markdown", disable_web_page_preview=True)
        return
    except Exception as e:
        try:
            try_to_delete_message(message.chat.id, guide_msg_1.message_id)
        except:
            pass
        log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\n🛑 error in main body: {str(e)}")
        bot.send_message(message.chat.id, fail_msg, parse_mode="Markdown", disable_web_page_preview=True)
        # import traceback
        # traceback.print_exc() # print error traceback

@bot.message_handler(func=lambda message: True)
def wrong_pattern_handler(message):
    log(f"{bot_username} log:\n\nuser: {message.chat.id}\n\n❌wrong pattern: {message.text}")
    bot.send_message(message.chat.id, wrong_pattern_msg, parse_mode="Markdown", disable_web_page_preview=True)

bot.infinity_polling()


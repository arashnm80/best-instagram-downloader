from functions import *

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "HI")

@bot.message_handler(regexp = insta_correct_link_reg)
def handle_correct_spotify_link(message):
    post_shortcode = get_post_shortcode_from_link(message.text)

    if not post_shortcode:
        return # post id not found

    L = get_ready_to_work_insta_instance()
    post = Post.from_shortcode(L.context, post_shortcode)
    sidecars = post.get_sidecar_nodes()
    first_media = False
    media_list = []
    for s in sidecars:
        if s.is_video: # it's a video
            url = s.video_url
            if not first_media:
                first_media = {"type": "video", "url": url}
            media = telebot.types.InputMediaVideo(url)
        else: # it's an image
            url = s.display_url
            if not first_media:
                first_media = {"type": "image", "url": url}
            media = telebot.types.InputMediaPhoto(url)

        media_list.append(media)

    if len(media_list) == 1:
        if first_media["type"] == "video":
            print("single video")
            bot.send_video(message.chat.id, first_media["url"], caption=post.caption)
        else:
            print("single image")
            bot.send_photo(message.chat.id, first_media["url"], caption=post.caption)
        return

    print("media group")
    bot.send_media_group(message.chat.id, media_list)
    return

    


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "wrong pattern")

bot.infinity_polling()


from functions import *


bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "HI")

@bot.message_handler(regexp = insta_correct_link_reg)
def handle_correct_spotify_link(message):
    # post_id = "CkyJVJvucbT" # bob
    # post_id = "Cy25C-ZIOgq" # girl with dress
    
    post_id = get_post_id_from_link()

    if not post_id:
        return # post id not found
    
    download_post_to_folder(post_id, "testFolder")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "wrong pattern")

bot.infinity_polling()


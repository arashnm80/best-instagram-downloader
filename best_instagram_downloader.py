from functions import *

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "HI")

@bot.message_handler(regexp = insta_correct_link_reg)
def handle_correct_spotify_link(message):
    # post_id = "CkyJVJvucbT" # bob
    # post_id = "Cy25C-ZIOgq" # girl with dress
    # post_id = "CyxWskeOMUo" # rock
    # post_id = "CzG8QcLoqHR" # sheida
    
    post_id = get_post_id_from_link(message.text)

    if not post_id:
        return # post id not found
    
    # download_post_to_folder(post_id, "testFolder")

    # # test stuff
    # L = get_ready_to_work_insta_instance()
    # post = Post.from_shortcode(L.context, post_id)
    # sidecars = post.get_sidecar_nodes()
    # for s in sidecars:
    #     print(s.display_url)

    


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "wrong pattern")

bot.infinity_polling()


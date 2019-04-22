from randomMovie import random_movie
import telebot
from telebot.types import Message
import re
import sqlite3
import os


TOKEN = os.getenv("TELEGRAM_TOKEN")
STICKER_ID = 'CAADAgADnQEAAjbsGwVbpgs1795URwI'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    bot.send_message(message.chat.id, text="Hey. I can choose you a random movie from your watchlist, but first give me a link to your watchlist \U0001F3AC /link")

@bot.message_handler(commands=['link'])
def command_link(message: Message):
    bot.send_message(message.chat.id, text='Give me your watchlist link')

    @bot.message_handler(content_types=['text'])
    def echo_movie(message: Message):
        text = message.text
        pattern = r'https:\/\/www\.imdb\.com\/user\/ur[0-9]+\/watchlist[\w\W]*'
        url = re.findall(pattern,text)
        if not url:
            bot.send_message(message.chat.id, text="That's not an imdb watchlist url...")
            bot.send_sticker(message.chat.id, data=STICKER_ID)
        else:
            user_id = message.from_user.id

            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            c.execute(f"SELECT user_id FROM users WHERE user_id={user_id}")
            check = c.fetchone()
            if check == None:
                c.execute(f"INSERT INTO users VALUES (?,?)",(user_id, url[0]))

                bot.send_message(message.chat.id, text="Your link has been saved. Thanks")
                bot.send_message(message.chat.id, text="Npw you can use /random_movie to get random movie from your watchlist \U0001F60B")
            else:
                bot.send_message(message.chat.id, text="You don't need to send your link twice. Geez...")
            
            conn.commit()
            conn.close()

@bot.message_handler(commands=['random_movie'])
def command_random_movie(message: Message):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    user_id = message.from_user.id

    c.execute(f"SELECT link FROM users WHERE user_id={user_id}")

    data = c.fetchone()

    if data == None:
        bot.send_message(message.chat.id, text="Give me your watchlist link first use /link command")
    else:
        movie_url = random_movie(data[0])
        if movie_url['link'] == '':
            bot.send_message(message.chat.id, text="I'm sorry, but you do not have films in your watchlist \U0001F622")
            bot.send_sticker(message.chat.id, data=STICKER_ID)
        else:
            bot.send_message(message.chat.id, text=movie_url['link'])

    conn.close()


bot.polling()
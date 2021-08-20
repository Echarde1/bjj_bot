import os

import telebot
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DB_URL = os.getenv('DB_CONN')
app.config['SQLALCHEMY_DATABSE_URI'] = SQLALCHEMY_DB_URL
db = SQLAlchemy(app)
bot = telebot.TeleBot('1975957600:AAEqP9V5rF60yrmUpP0f2H8DF9U_mjQYnZc')

counter = 0


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("Got message" + str(message))
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    elif message.text == "chlen":
        global counter
        counter += 1
        bot.send_message(message.from_user.id, str(counter))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


@bot.message_handler(commands=['stp'])
def stop_command(message):
    bot.send_message(message.from_user.id, "Ok")
    bot.stop_polling()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.before_first_request
def setup():
    db.create_all()


# if __name__ == "__main__":
#     app.run(debug=True)

bot.polling(none_stop=True, interval=0)

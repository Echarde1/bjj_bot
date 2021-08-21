import os
import threading

import telebot
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['JAWSDB_URL']
db = SQLAlchemy(app)
bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])
# bot = telebot.TeleBot(os.environ['FOO_TELEGRAM_BOT_TOKEN'])

counter = 0


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    message_cntr = db.Column(db.Integer)

    def __init__(self, user_name, first_name, message_cntr=1):
        self.user_name = user_name
        self.first_name = first_name
        self.message_cntr = message_cntr


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print("Got message " + str(message))
    username = str(message.from_user.username)
    first_name = str(message.from_user.first_name)
    print("username " + username)
    print("first_name " + first_name)
    update_if_needed(username, first_name)
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


# @app.before_first_request
# def setup():
#     threading.Thread(target=bot.polling(none_stop=True, interval=0), daemon=True)
# db.create_all()
# bot.polling(none_stop=True, interval=0)

# if __name__ == "__main__":
def update_if_needed(username, first_name):
    filtered = UserInfo.query.filter_by(user_name=username)
    result = filtered.first()
    if result is None:
        db.session.add(UserInfo(username, first_name))
    else:
        result.message_cntr = result.message_cntr + 1
    db.session.commit()

print(os.environ['JAWSDB_URL'])
print(os.environ['TELEGRAM_BOT_TOKEN'])
print(os.environ['TELEGRAM_BOT_TOKEN'])
bot.polling(none_stop=True, interval=0)

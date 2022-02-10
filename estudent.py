from telegram import Update

from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler
from telegram import *

import logging


updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)




def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# def login():
# 	context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")

def login(user_input):
    answer = "You have wrote me " + user_input
    return answer

def reply(update, context):
    user_input = update.message.text
    update.message.reply_text(do_something(user_input))


def main():
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


another_handler = CommandHandler('menu', login)
dispatcher.add_handler(start_handler)

# updater.start_polling()	

main()



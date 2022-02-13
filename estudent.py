import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram

import os
from dotenv import load_dotenv	


from estudent_bot import estudent_login, list_subjects, view_result

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

load_dotenv()


TELEGRAM_HTTP_API_TOKEN = os.getenv('token')
FIRST, SECOND, THIRD, FOURTH, FIVTH = range(5)

def start(update, bot):
    keyboard = [
        [InlineKeyboardButton(u"Login", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"Estudent Bot",
        reply_markup=reply_markup
    )
    return FIRST

def first(update, bot):
	print("I am first")
	query = update.callback_query
	query.message.reply_text(u"Enter Your ID")
	return SECOND

def second(update, bot):
	global user_id
	print("I am Second")
	query = update.message
	user_id = update.message.text
	print(user_id)
	query.reply_text(u"Enter Your Password")
	return THIRD

def third(update, bot):
	global user_password, user_id
	logged_in = False
	while  not logged_in:
		print("I am third")
		query = update.message
		user_password = query.text
		print(user_password)
		status = estudent_login(user_id, user_password)
		print(status)
		if status:
			keyboard = [
				[InlineKeyboardButton(u"View Result", callback_data=str(FOURTH))]]
			reply_markup = InlineKeyboardMarkup(keyboard)
		
			update.message.reply_text(
			    u"Logged in Successfully",
			    reply_markup=reply_markup
			)
			logged_in = True
			return FOURTH
		else:
			keyboard = [
				[InlineKeyboardButton(u"Login Agin", callback_data=str(FIRST))]]
			reply_markup = InlineKeyboardMarkup(keyboard)
			update.message.reply_text(u"Invalid ID or Password",
				reply_markup=reply_markup)
			logged_in = False
			return FIRST





def fourth(update, bot):
	print("I am fourth")
	query = update.callback_query
	global courses
	courses = list_subjects()
	keyboard = []
	for course in courses:
		keyboard.append([InlineKeyboardButton(course, callback_data=str(course))])
	reply_markup = InlineKeyboardMarkup(keyboard)
	query.message.reply_text(
	    u"Please Select a Course",
	    reply_markup=reply_markup)
	query.message.reply_text(u"Success")
	return FIVTH

def fivth(update, bot):
	print("I am fivth")
	query = update.callback_query
	query.answer()
	print(query.data)
	query.message.reply_text(view_result(query.data), parse_mode=telegram.ParseMode.HTML)	
	
    

updater = Updater(TELEGRAM_HTTP_API_TOKEN, use_context=True)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [CallbackQueryHandler(first)],
        SECOND: [MessageHandler(Filters.text, second)],
        THIRD: [MessageHandler(Filters.text, third)],
        FOURTH: [CallbackQueryHandler(fourth)],
        FIVTH: [CallbackQueryHandler(fivth)],
        
    },
    fallbacks=[CommandHandler('start', start)]
)

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()

updater.idle()
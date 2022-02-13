# Telegram
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import telegram
import os
from dotenv import load_dotenv	
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler

# Selenium


# Selenium Scrapper 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import time
from tabulate import tabulate

# Thread
import threading



# Telegram Stuff
load_dotenv()

TELEGRAM_HTTP_API_TOKEN = os.getenv('token')
FIRST, SECOND, THIRD, FOURTH, FIVTH = range(5)


# Selenium Stuff



options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
delay = 2 # seconds


	

def start(update, bot):
	user = update.message.from_user
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
		

		# Selenium Scrapper starts here 1st Stage
		global thread
		treadHandler = threading.Thread(driver.get("http://10.240.1.89"))
		treadHandler.start()
		

		user_ids = driver.find_element(By.ID,"user_name")
		passwords = driver.find_element(By.ID, "password")
		sign = driver.find_element(By.TAG_NAME, "button")
		status = False
		while not status:
			user_ids.clear()
			passwords.clear()
			user_ids.send_keys(user_id)
			passwords.send_keys(user_password)
			print("\n\nThis message is from Selenium: ",user_ids.get_attribute('value'), passwords.get_attribute('value'))
			sign.click()
			time.sleep(delay)

			try:
				# Selenium Error
				error = driver.find_element (By.XPATH, "//div[contains( text(), 'Invalid login credentials. Please try again.')]")
				keyboard = [
					[InlineKeyboardButton(u"Login Agin", callback_data=str(FIRST))]]
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text(u"Invalid ID or Password",
					reply_markup=reply_markup)
				logged_in = False
				return FIRST

			except:
				status = True
				keyboard = [
					[InlineKeyboardButton(u"View Result", callback_data=str(FOURTH))]]
				reply_markup = InlineKeyboardMarkup(keyboard)
			
				update.message.reply_text(
				    u"Logged in Successfully",
				    reply_markup=reply_markup
				)
				logged_in = True
				return FOURTH

		print(status)





def fourth(update, bot):
	print("I am fourth")
	query = update.callback_query
	global courses
	
	try:
		ac_his = driver.find_element(By.XPATH, "//a[@href='/academic_history']")
		ac_his.click()
		#Academic History
		time.sleep(delay)
		

		assessment_result = driver.find_element(By.XPATH, "//a[@href='#assessment_result']")
		assessment_result.click()

		time.sleep(delay)

		#Scroll course
		scroll = driver.find_element(By.ID, 'course_enrollment_id')
		options = [x.text for x in scroll.find_elements(By.TAG_NAME,"option")]
		options_a = [x.get_attribute("value") for x in scroll.find_elements(By.TAG_NAME,"option")]

		courses = {}

		for i in range(len(options)):
			courses[options[i]] = options_a[i]

	except:
		return "Error has Occured!"	


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

	# Selenium Stuff
	global courses
	try:
		value = courses[query.data]
		driver.find_element(By.XPATH,f"//option[@value='{value}']").click() 

		result_table = driver.find_element(By.XPATH, '/html/body/div/div/div/section/div/div/div[2]/div/div[4]/div/div/div/div/div/div[2]/table')
		t_head = driver.find_element(By.CLASS_NAME, 'thead-light')
		th = t_head.find_elements(By.TAG_NAME, 'th')
		thead = []
		for i in th:
			thead.append(i.text)
		
		tbody = result_table.find_elements(By.TAG_NAME, 'td')
		data = []
		d = []
		for i in tbody:
			if i.text == "":
				data.append(d)
				d = []
			else:
				d.append(i.text)

		print(tabulate(data,headers=thead))
		query.message.reply_text(tabulate(data,headers=thead), parse_mode=telegram.ParseMode.HTML)
	except:
		print("Exiting...")
		return False

		
	
    

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
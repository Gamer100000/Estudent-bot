from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import time
from tabulate import tabulate



options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

driver.get("http://10.240.1.89")

user_id = driver.find_element(By.ID,"user_name")
password = driver.find_element(By.ID, "password")
sign = driver.find_element(By.TAG_NAME, "button")
delay = 2 # seconds

def estudent_login(u_id,u_password):

	# --------------
	
	user_id.send_keys(u_id)
	password.send_keys(u_password)
	sign.click()
	try:
		error = driver.find_element (By.XPATH, "//div[contains( text(), 'Invalid login credentials. Please try again.')]")
		user_id.clear()
		password.clear()
		return False
		
	except:
		return True

	# After loged in successfully
	
	time.sleep(delay)


def list_subjects():
	global courses
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

	# for i,c in enumerate(options):
	# 	print(i,c)
	return courses


	

def view_result(value):
	global courses
	try:
		value = courses[value]
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
		return tabulate(data,headers=thead)
	except:
		print("Exiting...")
		return False
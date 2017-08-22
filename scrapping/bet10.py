from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from sqlalchemy import create_engine
import psycopg2, time
import os


def bet10_scrapping():
	display = Display(visible=0, size=(1200, 900))
	display.start()
	try:		
		bet10 = webdriver.Chrome(executable_path=os.path.abspath("/usr/bin/chromedriver"))
		bet10.get("http://partners.10bet.com/")
		bet10.find_element_by_id("username").send_keys("betfyuk")
		bet10.find_element_by_id("password").send_keys("dontfuckwithme")
		pwd = bet10.find_element_by_id("password")
		pwd.send_keys(Keys.RETURN)
		bet10.implicitly_wait(10)
		mtd_valArr = []
		table = bet10.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			mtd_valArr.append(mtd_val.text)
		bet10.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[2]').click()
		time.sleep(60)
		table = bet10.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		bet10.find_element_by_xpath('//*[@id="dashboard"]/div[1]/div[1]/div/div[1]/div/div/select[1]/option[4]').click()
		time.sleep(61)
		table = bet10.find_element(by=By.ID, value = "dashboard_quick_stats")
		mtds_val = table.find_element(by=By.CLASS_NAME, value = "row_light_color")
		for mtd_val in mtds_val.find_elements_by_tag_name("td"):
			if mtd_val.text != 'Total -':
				mtd_valArr.append(mtd_val.text)
		print(mtd_valArr)
		return mtd_valArr
	finally:
		bet10.quit()
		display.stop()

data = bet10_scrapping()

merchant = str(data[0])
impression = int(data[1])
click = int(data[2])
registration = int(data[3])
new_deposit = int(data[4])
commission = float(data[5])
impreytd = int(data[6])
cliytd = int(data[7])
regytd = int(data[8])
ndytd = int(data[9])
commiytd = float(data[10])
impreto = int(data[11])
clito = int(data[12])
regto = int(data[13])
ndto = int(data[14])
commito = float(data[15])

engine = create_engine('postgresql://postgres:root@localhost/kyan')
result = engine.execute("INSERT INTO bet10s (merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito)

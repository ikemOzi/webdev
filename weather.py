from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import mysql.connector
import openpyxl
from openpyxl import Workbook, load_workbook
import os
import sys



# Prepare script for executable conversion
application_path = os.path.dirname(os.path.abspath(__file__))

# fahrenheit to celsius converter


def fahrenheit_to_celsius(x):
    conversion = (x - 32) * (5/9)
    return round(conversion)

def lengthOFday(sunrise, sunset):
    hr,min = sunrise.split(':')
    hr2,min2 = sunset.split(':')
    len_sunrise = (int(hr) * 60) + int(min[0:2])
    len_sunset = ((int(hr2) + 12) * 60) + int(min2[0:2])
    difference = (len_sunset - len_sunrise)/60
    length_of_day = round(difference)
    return length_of_day



# Headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
# make connection
chromedriver_path = 'C:\\Users\\IKEMBUCHUKWU\\PycharmProjects\\automating\\chromedriver.exe'
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://weather.com/weather/monthly/l/54c05dba526194559ce1f72a53a7551cbde7db0b2e1b49ac96868cff81ade6fa")


# get date
now = datetime.now()
month_day_year = now.strftime("%A-%B-%d-%Y")
day_week, month, day, year = month_day_year.split('-')

#get weather type with beautiful soup
baseurl = 'https://weather.com/weather/today/l/214a966fa550aef8e13d7653a1ec2c76fbeeef54e67796211b077e76e2bdf897'
html_text = requests.get(baseurl).text
soup = BeautifulSoup(html_text, 'lxml')
weather = soup.find('div', class_='DailyWeatherCard--TableWrapper--2bB37').ul.li.a.find('div', class_='Column--icon--2TNHl Column--small--2Cczu Column--verticalStack--28b4K').svg.title.text
time.sleep(10)
# select today's weather on website
select_today = driver.find_element(By.XPATH, "//*[@class='ListItem--listItem--25ojW styles--listItem--2CkF3 Button--default--2gfm1'][1]")
select_today.click()
time.sleep(10)
# get night temperature
night_temp = driver.find_element(By.XPATH, "//*[@class='CurrentConditions--primary--2DOqs']/div[2]/span[2]").text
night_tempC = fahrenheit_to_celsius(int(night_temp[:-1]))
# get day temperature
day_temp = driver.find_element(By.XPATH, "//*[@class='CurrentConditions--primary--2DOqs']/div[2]/span[1]").text
day_tempC = fahrenheit_to_celsius(int(day_temp[:-1]))
# time of sunrise
sunrise = driver.find_element(By.XPATH, '//*[@data-testid="SunriseValue"]/p').text
# time of sunset
sunset = driver.find_element(By.XPATH, '//*[@data-testid="SunsetValue"]/p').text
# wind speed in mph
wind_speed = driver.find_element(By.XPATH, '//*[@class="Wind--windWrapper--3Ly7c undefined"]/span[2]').text # in mph
# percent humidity
humidity = driver.find_element(By.XPATH, '//*[@data-testid="PercentageValue"]').text[:-1]
# what weather feels like
feels_like = driver.find_element(By.XPATH,'//*[@class="TodayDetailsCard--feelsLikeTempValue--2icPt"]').text
feels_likeC = fahrenheit_to_celsius(int(feels_like[:-1]))
# the moon phase
moon_phase = driver.find_element(By.XPATH,'(//div[@class="ListItem--listItem--25ojW WeatherDetailsListItem--WeatherDetailsListItem--1CnRC"][8])/div[2]').text


######################################################################################
######################################################################################
# MAKE SQL TABLE

mydb = mysql.connector.connect(
    host='localhost',
    user = 'root',
    password = 'Silvergod10',
    port = '3306',
    database = 'weather'
)
mycursor = mydb.cursor()

# create table
mycursor.execute("CREATE TABLE IF NOT EXISTS weather_table (ID INT PRIMARY KEY AUTO_INCREMENT, "
                 "month VARCHAR(50), day INT, day_of_week VARCHAR(50), morning_temperature_C INT, "
                 "night_temperature_C INT, wind_chill_temp_C INT, wind_speed_mph INT, humidity_percent INT, "
                 "weather_type VARCHAR(50), sunrise VARCHAR(50), sunset VARCHAR(50), length_of_day INT,"
                 " moon_phase VARCHAR(50) )")

mycursor.execute("INSERT INTO weather_table (month, day, day_of_week, morning_temperature_C, "
                 "night_temperature_C, wind_chill_temp_C, wind_speed_mph, humidity_percent, "
                 "weather_type, sunrise, sunset, length_of_day, moon_phase)"
                 " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (month, day, day_week,
                                                                      day_tempC, night_tempC, feels_likeC, wind_speed,
                                                                      humidity, weather, sunrise, sunset,
                                                                      lengthOFday(sunrise, sunset), moon_phase ))

mydb.commit()

######################################################################################
######################################################################################
# MAKE EXCEL TABLE

# load workbook
wb = load_workbook('C:\\Users\\IKEMBUCHUKWU\\PycharmProjects\\automating\\google_weather.xlsx')

# set active worksheet
ws = wb.active

# set title of worksheet
ws.title = 'Weather Data'

# append data
ws.append([month, day, day_week,day_tempC, night_tempC, feels_likeC, wind_speed, humidity, weather, sunrise, sunset, lengthOFday(sunrise, sunset), moon_phase])

# save data
wb.save('C:\\Users\\IKEMBUCHUKWU\\PycharmProjects\\automating\\google_weather.xlsx')
driver.quit()

print('done')


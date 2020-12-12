#!/usr/bin/python3
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
from mysql.connector import Error
from mysql.connector import errorcode
import mysql.connector
import time
import pytz

time_th = pytz.timezone('Asia/Bangkok')
#new_update = html_soup.find('td', {'class':'aqiwgt-table-aqiinfo'}).find('span').text
def insert_todb(update, value1, value2, loca, polution_status):
    try:
        connection = mysql.connector.connect(host='',
                                             database='',
                                             user='',
                                             password='')
        query = """insert into bu_pm (last_update, pm25, pm10, location, polution_lv) VALUES (%s, %s, %s, %s, %s)"""
        attr = (update, value1, value2, loca, polution_status)
        cursor = connection.cursor()
        cursor.execute(query, attr)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into sub table")
        cursor.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into sub table {}".format(error))
    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL connection is closed")

url = 'https://aqicn.org/city/thailand/pathum-thani/bangkok-university-rangsit-campus/'
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')
value = html_soup.find_all('td', {'id':'cur_pm25'})                                 # Data of pm2.5 at bu
dt = str(datetime.now(time_th))                                                 # Last update 
address = html_soup.find('div', {'class':'aqiwgt-table-title'}).find('a').text      # Address
polution_status = html_soup.find('div',{'id':'aqiwgtinfo'}).text
pm1_0 = html_soup.find('td', {'id':'cur_pm10'}).text
pm2_5 = value[0].text
insert_todb(dt, pm2_5, pm1_0, address, polution_status)
#print(dt, pm2_5, pm1_0, address, polution_status)
print(pm1_0)
print(pm2_5)

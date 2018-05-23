import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from mysql.connector import Error, MySQLConnection
import json

dbconfig = {
    'host': 'localhost',
    'database': 'weather',
    'user': 'mustafa',
    'password': 'Passw0rd'
}

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.Wu7pEx6geUk")
soup = BeautifulSoup(page.content,"html.parser")

seven_day_fc = soup.find(id="seven-day-forecast-container")
forecast_item = seven_day_fc.find_all(class_="forecast-tombstone")

################# One day forecast ###################
#tonight = forecast_item[0]
#print(tonight.prettify())
#period = tonight.find(class_="period-name").get_text()
#short_desc = tonight.find(class_="short-desc").get_text()
#temp = tonight.find(class_="temp").get_text()

#get the title from img tag as a dictionary because there are many attributes within img tag
#img = tonight.find("img")
#desc = img['title']
#print(desc)

#getting all days forecast by iterating through the list
period_tags = seven_day_fc.select(".tombstone-container .period-name")
period = [pt.get_text() for pt in period_tags]
short_desc = [sd.get_text() for sd in seven_day_fc.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day_fc.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day_fc.select(".tombstone-container img")]

periodNew = period
print(period)

#putting the data into dataframes using pandas for analysis

#weather = pd.DataFrame({
#       "period": period,
#       "short_desc": short_desc,
#        "temps": temps,
#       "descs": descs
#  })

#print(weather)

#writing the results to excel
#writer = pd.ExcelWriter('weather_data.xlsx', engine = 'xlsxwriter')
#weather.to_excel(writer, sheet_name='Sheet 1')
#writer.save()

cnx = MySQLConnection(**dbconfig)
cursor = cnx.cursor()

insert_wData = 'INSERT INTO weather_data_scrape (period) VALUES(%s)' %(periodNew)

cursor.execute(insert_wData)

cnx.commit()

cnx.close()



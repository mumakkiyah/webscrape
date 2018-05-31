import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
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


my_list = [1,2,3,4,5,6,7,8,9]
df = pd.DataFrame(np.array(my_list).reshape(3,3), columns = list("abc"))
df = pd.DataFrame(np.array(my_list).reshape(3,-1), columns = list("abc"))

#getting all days forecast by iterating through the list
period_tags = seven_day_fc.select(".tombstone-container .period-name")
period = [pt.get_text() for pt in period_tags]
period_df = pd.DataFrame(np.array(period).reshape(-1,1), columns = list("P"))

short_desc = [sd.get_text() for sd in seven_day_fc.select(".tombstone-container .short-desc")]
short_desc_df = pd.DataFrame(np.array(short_desc).reshape(-1,1), columns = list("s"))

temps = [t.get_text() for t in seven_day_fc.select(".tombstone-container .temp")]
temps_df = pd.DataFrame(np.array(temps).reshape(-1,1), columns = list("t"))

descs = [d["title"] for d in seven_day_fc.select(".tombstone-container img")]
descs_df = pd.DataFrame(np.array(descs).reshape(-1,1), columns = list("d"))

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

insert_wData = 'INSERT INTO weather_data_scrape (period, temp) VALUES(%s, %s)' %(period_df,temps_df)

cursor.execute(insert_wData)

cnx.commit()

cnx.close()



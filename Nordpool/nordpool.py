from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import json
import paho.mqtt.client as mqtt

chromedriver = "D:/VGTU/3_Kursas/2/IIP/Nordpool/chromedriver-win32/chromedriver.exe"

options = webdriver.ChromeOptions()
service = Service(executable_path=chromedriver)
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.nordpoolgroup.com/en/market-data12/Dayahead/Area-Prices/LT/Hourly/?view=table"

def scrape_nordpool_data():
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Find the data table by ID "datatable"
    table = driver.find_element(By.ID, "datatable")

    # Inside the table in the <thead>, <tr class="column-headers"> find the 2nd <th> and save the date as a variable
    table_head = table.find_element(By.TAG_NAME, "thead")
    column_headers = table_head.find_elements(By.CLASS_NAME, "column-headers")
    second_header = column_headers[0].find_elements(By.TAG_NAME, "th")[1]
    date = second_header.text

    # Go back to <tbody> and in each row get and save the first two columns.
    table_body = table.find_element(By.TAG_NAME, "tbody")
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        first_column = cells[0].text
        second_column = cells[1].text
        data.append({"time": first_column, "price": second_column})

    # All of this data save into a JSON file
    with open("nordpool_data.json", "w") as outfile:
        json.dump({"date": date, "data": data}, outfile)
        
        return {"date": date, "data": data}  # Return scraped data

scraped_data = scrape_nordpool_data()



mqttBroker = "broker.mqttdashboard.com"
topic = "Lukas/Nordpool"

def send_to_mqtt(data):
    client = mqtt.Client()
    client.connect(mqttBroker)
    time.sleep(3)
        
    client.publish(topic, json.dumps(data))
    print("Published to MQTT")
    client.disconnect()

time.sleep(5)
send_to_mqtt(scraped_data)
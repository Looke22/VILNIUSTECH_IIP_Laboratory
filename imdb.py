from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
chromedriver = "C:/Users/lukas/Desktop/reactLab/chromedriver-win32/chromedriver.exe"

#os.environ["webdriver.chrome.driver"] = chromedriver
#chrome_options = Options()
#chrome_options.add_argument("--headless") 

options = webdriver.ChromeOptions()
service = Service(executable_path=chromedriver)
driver = webdriver.Chrome(service=service, options=options)

url="http://www.imdb.com"

def join_content(jc):
    return ','.join(jc)

def iterate_actors(iter_actors):
    m=[]
    for item in iter_actors:
        m.append(item['name'])
    return ','.join(m)
        

def prepare_content(json_content):
    d = {}
    d['image'] = json_content['image']
    d['name'] = json_content['name']
    d['url_content'] = url+json_content['url']
    d['genre'] = join_content(json_content['genre'])
    d['actors'] = iterate_actors(json_content['actor'])
    d['description'] = json_content['description']
    d['trailer'] = url+json_content['trailer']['embedUrl']
    return d
    
    
    

def imdb_searchbox(url, link):
    driver.get(url)
    searchbox = driver.find_element(By.ID, "suggestion-search")
    searchbox.click()
    searchbox.send_keys(link)
    time.sleep(1)
    try:
        driver.find_element(By.ID, "react-autowhatever-navSuggestionSearch--item-0").click()
    except NoSuchElementException:
        return None
    json_content = json.loads(driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]').get_attribute("innerText"))
    return prepare_content(json_content)
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # json_script = soup.find("script", type="application/ld+json")
    # if json_script:
    #     json_content = json.loads(json_script.string)
    #     return prepare_content(json_content)

def imdb_search(link):
    s=imdb_searchbox(url, link)
    driver.get_screenshot_as_file("capture.png")
    return s



    

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from utilities import get_news

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")

web_url = 'https://www.google.com/finance/'
service = Service(executable_path='./chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)
driver.get(web_url)
    
clickable_news = driver.find_elements(By.XPATH, '(//div[@role="tablist"])[2]//div')

df_list = []

for clickable in clickable_news:
    clickable.click()
    time.sleep(0.5)
    df_list.append(get_news(driver, clickable.text))

final_news: pd.DataFrame = pd.concat(df_list)
final_news.to_csv('./extracted_data/news.csv', index=False)
driver.quit()


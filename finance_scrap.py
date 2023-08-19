from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd
import time
from utilities import get_news, get_stocks

options = Options()
options.add_argument("--window-size=1920,1080")

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

driver.find_element(By.XPATH, '((//a[contains(@href,"/indexes")])[2]//span)[2]').click()

new_url = driver.window_handles[0]
driver.switch_to.window(new_url)

time.sleep(3)

clickable_stocks = driver.find_elements(By.XPATH, '//div[@role="navigation"]//div[@role="tablist"]//a')
categories = [el.text for el in driver.find_elements(By.XPATH, '//div[@role="navigation"]//div[@role="tablist"]//a')]

df_list = []
for i in range(len(categories)):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element_xpath = f'(//div[@role="navigation"]//div[@role="tablist"]//a)[{i+1}]'
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    element = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.XPATH, element_xpath)))
    driver.execute_script("arguments[0].click();", element)
    new_url = driver.window_handles[0]
    driver.switch_to.window(new_url)
    time.sleep(2)
    df_list.append(get_stocks(driver, categories[i]))
    


final_stocks: pd.DataFrame = pd.concat(df_list)
final_stocks.to_csv('./extracted_data/stocks.csv', index=False)

driver.quit()


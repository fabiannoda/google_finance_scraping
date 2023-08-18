from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

def get_news (driver: webdriver, category: str):
    news_cast = []
    headline = []
    link = []
    news = driver.find_elements(By.XPATH, '//section[@aria-labelledby="news-title"]/*//a[@rel="noopener noreferrer"]')
    for new in news:
        news_cast.append(new.find_element(By.XPATH, './div[1]/./div[1]/./div[1]').text)
        headline.append(new.find_element(By.XPATH, './div[1]/./div[2]').text)
        link.append(new.get_attribute('href'))
    df = pd.DataFrame({'news_cast': news_cast, 'headline': headline, 'link': link, 'category': category})
    return df
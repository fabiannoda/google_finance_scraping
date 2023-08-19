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

def get_stocks (driver: webdriver, category: str):
    stock_abreviation = []
    names = []
    price = []
    before_price_compare = []
    percentage = []
    stocks = driver.find_elements(By.XPATH, '//ul/li')

    for stock in stocks:
        stock_abreviation.append(stock.find_element(By.XPATH,'.//div[contains(@style,"background-color")]/div').text)
        names.append(stock.find_element(By.XPATH,'.//div[2]/./div').text)
        price.append(stock.find_element(By.XPATH,'.//span/./div/div').text)
        before_price_compare.append(stock.find_element(By.XPATH,'.//div[3]/.//span').text)
        percentage.append(stock.find_element(By.XPATH,'.//div[4]//span').get_attribute('aria-label'))
    stock_abreviation = list(filter(None, stock_abreviation))
    names = list(filter(None, names))
    price = list(filter(None, price))
    before_price_compare = list(filter(None, before_price_compare))
    percentage = percentage[-len(names):len(percentage)]
    df = pd.DataFrame({'stock_abreviation': stock_abreviation, 'names': names, 'price': price, 'before_price_compare': before_price_compare, 'percentage': percentage, 'category': category})
    return df
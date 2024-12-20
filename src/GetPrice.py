import os
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException
import DataBase
from time import sleep
import re


user_name = (os.path.basename(os.environ['USERPROFILE']))

def GetPrice(link, ID):
    chrome_options = Options()
    chrome_options.add_argument(f'user-data-dir=C:\\Users\\{user_name}\\AppData\\Local\\Google\\Chrome\\User Data')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Ẩn cửa sổ
    # chrome_options.add_argument('--headless')
    # invoke the webdriver
    service = Service("chromedriver-win64/chromedriver.exe")
    delay = 15 #seconds
    price = ""

    try:
        browser = webdriver.Chrome(options = chrome_options, service = service)
        browser.get(link)
        try:
            WebDriverWait(browser, delay)
            sleep(5)
            html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            soup = BeautifulSoup(html, "html.parser")

            # find the price of items

            if link.__contains__("shopee"):
                x = soup.find('div', class_='IZPeQz B67UQ0')
                if x: price = x.get_text()
            elif link.__contains__("sendo"):
                x = soup.find('span', class_='d7ed-ij7pjf d7ed-AHa8cD d7ed-giDKVr')
                if x: price = x.get_text()
            elif link.__contains__("lazada"):
                x = soup.find('span', class_='notranslate pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl')
                if x: price = x.get_text()

        except TimeoutException:
            print("Thử Lại")

        unwanted_chars = "[₫.đ,-]"
        price = re.sub(unwanted_chars, "", price)
        prices = list(map(str, price.split()))
        if prices:
            DataBase.UpdatePriceById(ID, prices[0])
        else:
            messagebox.showerror("có lỗi xảy ra khi lấy dữ liệu, kiểm tra lại trình duyệt.")
            return "error"
        browser.close()
    except SessionNotCreatedException as e:
        messagebox.showerror(title="Error", message=str(e))
        return "error"

    return ""

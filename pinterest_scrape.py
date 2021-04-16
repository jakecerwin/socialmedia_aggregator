#!/usr/bin/env python
# coding: utf-8

# need to install these first, and also download webdriver(chrome)
# pip install selenium
# pip install webdriver_manager

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

#instantiate the Chrome class web driver and pass the Chrome Driver Manager
driver = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
driver.maximize_window()

#go to Pinterest's Login page
driver.get("https://www.pinterest.com/login/")

user = 'jake.cerwin@yahoo.com'
password = 'datafocusedpythOn'

# login to account before starting to scrape
# email
driver.find_element_by_xpath('//*[@id="email"]').send_keys(user)

# password
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

# click login button
driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()


# scrape data!
#driver.get("https://www.pinterest.com/")

#raw_data = open("data/raw_pinterest.txt", "w")
images = []

# get five scrolls of data
for _ in range(1,5):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    with open('data/raw_pinterest.html', 'w', encoding='utf-8') as f_out:
        f_out.write(soup.prettify())


    # get the image from div with pinrep-image test-id
    for img in soup.find_all('div', {"data-test-id":"pinrep-image"}):


        target = img.find('img')
        if target is not None:
            str = target.get('src')
            images.append(f'{str}')

    # scroll down
    driver.execute_script("window.scrollTo(1,100000)")
    time.sleep(1)

print(images)

import pandas as pd

df = pd.DataFrame(images, columns=['pin_url'])
df['user'] = user
df['id'] = df.index
df['cat'] = 'pinterest'
df.head()

df.to_csv('data/cleaned_pinterest.csv', index=False)

driver.quit()


# write to file (ignore, the old way)
#with open ('pinterest_img.txt', 'w', encoding = 'utf-8') as pin_img:
#    pin_img.writelines(lines for lines in images)


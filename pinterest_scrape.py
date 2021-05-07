
#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import pandas as pd

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

images = []
content = []

# get five scrolls of data
for _ in range(1,5):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    

    # get the image from div with pinrep-image test-id
    for img in soup.find_all('div', {"data-test-id":"pinrep-image"}):


        target = img.find('img')
        if target is not None:
            str = target.get('src')
            images.append(f'{str}')
    
    # get the image from div with pinrep-image test-id
    for con in soup.find_all('div', {"class":"tBJ dyH iFc MF7 pBj DrD mWe"}):
        tar = con.get_text()
        content.append(tar)

    # scroll down
    driver.execute_script("window.scrollTo(1,100000)")
    time.sleep(1)

# print(content)

data = {'Image url': pd.Series(images),'Content':pd.Series(content)}
df = pd.DataFrame(data)
df.dropna(subset = ["Image url"], inplace=True)

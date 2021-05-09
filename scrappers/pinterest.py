# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:46:02 2021

@author: kriti and Jcerwin
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

debug = False

class PinterestScrapper:

    def __init__(self, username, password):
        options = webdriver.ChromeOptions()
        options.headless = not debug

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Maximize the Chrome window to full-screen
        # driver.minimize_window()

        # go to Pinterest's Login page
        self.driver.get("https://www.pinterest.com/login/")

        self.user = username
        self.password = password

        # login to account before starting to scrape
        # email
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.user)

        # password
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)

        # click login button
        self.driver.find_element_by_xpath(
            '//*[@id="__PWS_ROOT__"]/div[1]/div/div/div[3]/div/div/div[3]/form/div[5]/button').click()

        self.scraped = set()
        self.scraped_count = 0
        return None

    def scrape(self):
        # raw_data = open("data/raw_pinterest.txt", "w")
        images = []
        ids = []
        fmt = ""

        # get five scrolls of data
        for _ in range(1, 5):
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # get the image from div with pinrep-image test-id
            for img in soup.find_all('div', {"data-test-id": "pinrep-image"}):

                target = img.find('img')
                if target is not None:
                    image_str = target.get('src')

                    # prevent duplicates
                    if image_str in self.scraped:
                        continue
                    else:
                        self.scraped.add(image_str)

                    images.append(image_str)
                    self.scraped_count += 1
                    id = 'pt'+ str(self.scraped_count).zfill(8)
                    ids.append(id)

                    breakpoint()







            # scroll down
            self.driver.execute_script("window.scrollTo(1,100000)")
            time.sleep(1)

        data = {'images': pd.Series(images), 'ids': pd.Series(ids), }
        df = pd.DataFrame(data)

        # df.to_csv('data/cleaned_pinterest.csv', index=False)

        return df

    def refresh(self):
        self.driver.refresh()
        return None

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import simpledialog

    ROOT = tk.Tk()

    ROOT.withdraw()

    USERNAME = simpledialog.askstring(title="Login",
                                      prompt="Username")
    PASSWORD = simpledialog.askstring(title="Login",
                                      prompt="Password")

    pinterest = PinterestScrapper(USERNAME, PASSWORD)
    time.sleep(5)
    df = pinterest.scrape()
    pinterest.close()

    print(df.head())



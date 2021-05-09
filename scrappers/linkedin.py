#!/usr/bin/env python
# coding: utf-8

"""
@author: Gini and Jake Cerwin
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd


debug = True


class LinkedinScrapper:
    def __init__(self, username, password):
        options = webdriver.ChromeOptions()
        if not debug:
            options.headless = True
        # instantiate the Chrome class web driver and pass the Chrome Driver Manager
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        #Maximize the Chrome window to full-screen
        self.driver.maximize_window()

        self.driver.get('https://www.linkedin.com/login/')
        self.user = username
        self.password = password

        # login to account before starting to scrape
        elementID = self.driver.find_element_by_id('username')
        elementID.send_keys(username)
        elementID = self.driver.find_element_by_id('password')
        elementID.send_keys(password)
        elementID.submit()

        # account for remember me pop up
        try:
            elementID = self.driver.find_element_by_id('remember-me-prompt__form-primary')
            elementID.submit()
        except:
            pass

        return None

    def scrape(self):
        for _ in range(1, 20):
            src = self.driver.page_source
            soup = BeautifulSoup(src, "lxml")

            content = soup.findAll('span', attrs={'class': 'break-words'}) + soup.findAll('article', attrs={
                'class': 'feed-shared-announcement__description-container'})
            contents = []
            for i in content:
                c = i.get_text()
                contents.append({c})

            # Gini pls fix this
            personal_image = soup.findAll('img', attrs={'class':
                'lazy-image'})
            personal_images = []
            names = []


            for image in personal_image:
                breakpoint()
                # print(i['src'])
                src = image.attrs['src']
                e = image.attrs['title']
                personal_images.append({d})
                names.append({e})

            number_likes = []
            for i in soup.findAll('span',
                                  attrs={'class': 'v-align-middle social-details-social-counts__reactions-count'}):
                e = i.get_text()
                number_likes.append({e})
            self.driver.execute_script("window.scrollTo(1,100000)")
            time.sleep(2)

        data = {'User Image url': pd.Series(personal_images), 'Name': pd.Series(names),
                'Post Content': pd.Series(contents), 'Likes': pd.Series(number_likes)}
        df = pd.DataFrame(data)

        df.dropna(subset=["User Image url"], inplace=True)

        return df

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

    linkedin = LinkedinScrapper(USERNAME, PASSWORD)
    time.sleep(5)
    df = linkedin.scrape()
    linkedin.close()

    print(df.head())





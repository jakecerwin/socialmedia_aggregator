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
import numpy as np



class LinkedinScrapper:
    def __init__(self, username, password, debug=False):
        options = webdriver.ChromeOptions()
        if not debug:
            options.headless = True
        # instantiate the Chrome class web driver and pass the Chrome Driver Manager
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        # Maximize the Chrome window to full-screen
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
        images = []
        names = []
        postids = []
        contents = []
        number_likes = []

        for _ in range(1, 15):
            src = self.driver.page_source
            soup = BeautifulSoup(src, "lxml")

            # finding content
            try:
                content = soup.findAll('span', attrs={'class': 'break-words'})

                for i in content:
                    c = i.get_text()
                    contents.append({c})
            except:
                print('content')


            # finding image and name
            try:
                the_image = soup.findAll('div',
                                         attrs={'class': 'feed-shared-actor__avatar ivm-image-view-model ember-view'})

                for i in the_image:
                    if i is not None:

                        postid = 'lk' + i.attrs['id'][5:].zfill(8)
                        if postid in postids:
                            continue
                        image = i.img['src']
                        name = i.img['alt']
                        images.append(image)
                        names.append('linkedin@' + name)
                        postids.append(postid)


                    else:

                        continue
            except:
                print('image')

        # finding likes
        try:

            for i in soup.findAll('span',
                                  attrs={'class': 'v-align-middle social-details-social-counts__reactions-count'}):
                e = i.get_text()
                number_likes.append(e)

        except:
            print('likes')


        self.driver.execute_script("window.scrollTo(1,100000)")
        time.sleep(2)

        data = {
            'postid': np.array(postids),
            'likes': np.array(number_likes),
            'category': np.array(names),
            'link': np.array(images),
            'data': np.array(names)
        }
        #data = {'User Image url': np.array(images), 'Name': np.array(names),
        #        'Post Content': np.array(contents), 'Likes': np.array(number_likes)}
        df = pd.DataFrame(data)

        df.dropna(subset=["link"], inplace=True)
        return df

    def close(self):
        self.driver.quit()


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import simpledialog

    ROOT = tk.Tk()

    ROOT.withdraw()

    #USERNAME = simpledialog.askstring(title="Login",
    #                                  prompt="Username")
    #PASSWORD = simpledialog.askstring(title="Login",
    #                                  prompt="Password")
    USERNAME = 'jcerwin@andrew.cmu.edu'
    PASSWORD ='Carmel25!'

    linkedin = LinkedinScrapper(USERNAME, PASSWORD, False)
    time.sleep(5)
    df = linkedin.scrape()

    linkedin.close()
    df.to_csv('../data/linkedin.csv')

    print(df.head())


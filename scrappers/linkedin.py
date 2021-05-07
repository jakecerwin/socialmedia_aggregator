#!/usr/bin/env python
# coding: utf-8

"""
@author: Gini and Jake Cerwin
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
#from requests_html import HTMLSession
import time
import pandas as pd




class LinkedinScrapper:
    def __init__(self, username, password):
        options = webdriver.ChromeOptions()
        #options.headless = True
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

            personal_image = soup.findAll('img',
                                          attrs={'class': 'presence-entity__image ivm-view-attr__img--centered EntityPhoto-circle-3 feed-shared-actor__avatar-image EntityPhoto-circle-3 lazy-image ember-view'})
            personal_images = []
            names = []

            for i in personal_image:
                # print(i['src'])
                d = i['src']
                e = i['title']
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

    def close(self ):
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


"""
# In[107]:


from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USERNAME = simpledialog.askstring(title="Login",
                                  prompt="Username")
PASSWORD = simpledialog.askstring(title="Login",
                                  prompt="Password")


# In[108]:


#go to LinkedIN's Login page
self.driver.get('https://www.linkedin.com/login/')


# In[109]:


# login to account before starting to scrape

username = USERNAME
password = PASSWORD
elementID = self.driver.find_element_by_id('username')
elementID.send_keys(username)

elementID = self.driver.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()


# In[125]:


#  Get page source code

for _ in range(1,20):
    src = self.driver.page_source
    soup = BeautifulSoup(src, "lxml")

    content = soup.findAll('span', attrs = {'class':'break-words'}) + soup.findAll('article', attrs = {'class':'feed-shared-announcement__description-container'})
    contents = []
    for i in content:
        c = i.get_text()
        print(c)
        contents.append({c})

    personal_image = soup.findAll('img', attrs={'class': 'presence-entity__image ivm-view-attr__img--centered EntityPhoto-circle-3 feed-shared-actor__avatar-image EntityPhoto-circle-3 lazy-image ember-view'})
    personal_images = []
    names = []
    for i in personal_image:
    #print(i['src'])
        d = i['src']
        e = i['title']
        personal_images.append({d})
        names.append({e})
        
    number_likes = []
    for i in soup.findAll('span', attrs={'class': 'v-align-middle social-details-social-counts__reactions-count'}):
        e = i.get_text()
        number_likes.append({e})
    self.driver.execute_script("window.scrollTo(1,100000)")
    time.sleep(2)
    


# In[126]:


#Clean Data
data = {'User Image url': pd.Series(personal_images),'Name':pd.Series(names), 'Post Content': pd.Series(contents), 'Likes' : pd.Series(number_likes)}
df = pd.DataFrame(data)
print(df.head())
df.dropna(subset = ["User Image url"], inplace=True)


# In[100]:


df.to_csv('C:/Users/DELL/PycharmProjects/linkedin/Clean_Data.csv', index = False)


# In[ ]:
"""





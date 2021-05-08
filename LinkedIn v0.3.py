#!/usr/bin/env python
# coding: utf-8

# In[58]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import tkinter as tk


# In[59]:


#instantiate the Chrome class web driver and pass the Chrome Driver Manager
browser = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
browser.maximize_window() 


# In[60]:


from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USERNAME = simpledialog.askstring(title="Login",
                                  prompt="Username")
PASSWORD = simpledialog.askstring(title="Login",
                                  prompt="Password")


# In[61]:


#go to LinkedIN's Login page
browser.get('https://www.linkedin.com/login/')


# In[62]:


# login to account before starting to scrape

username = USERNAME
password = PASSWORD
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()


# In[91]:


#  Get page source code

for _ in range(1,5):
    
    src = browser.page_source
    soup = BeautifulSoup(src, "lxml")


    #finding content
    try:
        content = soup.findAll('span', attrs = {'class':'break-words'})
        contents = []
        for i in content:
            c = i.get_text()
            contents.append({c})
    except KeyError:
        continue
    except TypeError:
        continue
    except ValueError:
        continue

    #finding image and name
    try:
        the_image = soup.findAll('div', attrs={'class': 'feed-shared-actor__avatar ivm-image-view-model ember-view'})
        images = []
        names = []
        for i in the_image:
            if i is not None:
                image = i.img['src']
                name = i.img['alt']
                images.append({image})
                names.append({name})
            else:
                continue
    except KeyError:
        continue
    except TypeError:
        continue
    except ValueError:
        continue
    
    #finding likes
    try:
        number_likes = []
        for i in soup.findAll('span', attrs={'class': 'v-align-middle social-details-social-counts__reactions-count'}):
            e = i.get_text()
            number_likes.append({e})
    except KeyError:
        continue
    except TypeError:
        continue
    except ValueError:
        continue
        
    browser.execute_script("window.scrollTo(1,100000)")
    time.sleep(2)


# In[92]:


#Clean Data

data = {'User Image url': pd.Series(images),'Name':pd.Series(names), 'Post Content': pd.Series(contents), 'Likes' : pd.Series(number_likes)}
df = pd.DataFrame(data)
df.dropna(subset = ["User Image url"], inplace=True)


# In[93]:


df.head()


# In[94]:


df.to_csv('C:/Users/DELL/PycharmProjects/linkedin/Clean_Data.csv', index = False)


# In[ ]:





#!/usr/bin/env python
# coding: utf-8

# In[80]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
#from requests_html import HTMLSession
import time
import pandas as pd


# In[81]:


#instantiate the Chrome class web driver and pass the Chrome Driver Manager
browser = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
browser.maximize_window() 


# In[82]:


#go to LinkedIN's Login page
#browser = HTMLSession()
browser.get('https://www.linkedin.com/login/')


# In[83]:


# login to account before starting to scrape

username = 'ginibasu@gmail.com'
password = 'Swastika@2418'
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()


# In[88]:


#  Get page source code
src = browser.page_source

for scroll in range(1,5):
    soup = BeautifulSoup(src, "lxml")

    
    name = soup.findAll('span', attrs={'class': 'feed-shared-actor__name'})
    names = []
    for i in name:
        print(i.get_text())
        a = i.get_text()
        names.append({a})

    description = soup.findAll('span', attrs={'class': 'feed-shared-actor__description t-12 t-normal t-black--light'})
    descriptions = []
    for i in description:
        #print(i.get_text())
        b = i.get_text()
        descriptions.append({b})

    content = soup.findAll('span', attrs={'class': 'break-words'})
    content1 = soup.findAll('h2', attrs={'class': 'feed-shared-announcement__title t-14 t-black--light'})
    contents = []
    for i in content:
        print(i.get_text())
        if i.get_text() is None:
            c = "\n"
        else:
            c = i.get_text()
        contents.append({c})

    personal_image = soup.findAll('img', attrs={'class': 'presence-entity__image ivm-view-attr__img--centered EntityPhoto-circle-3 feed-shared-actor__avatar-image EntityPhoto-circle-3 lazy-image ember-view'})
    personal_images = []
    for i in personal_image:
        print(i['src'])
        d = i['src']
        personal_images.append({d})

print(names)
print("Length of names: ",len(names))
print(descriptions)
print("Length of descriptions: ",len(descriptions))
print(contents)
print("Length of content: ",len(contents))
print(personal_images)
print("Length of images: ",len(personal_images))


# In[87]:


#data1
data = {'User Image url': pd.Series(personal_images),'Name':pd.Series(names), 'Decsriptions':pd.Series(descriptions),'Post Content': pd.Series(contents)}
df = pd.DataFrame(data)
df.to_csv('RawData _ Image', index = False)
df.to_csv('C:/Users/DELL/PycharmProjects/linkedin/Raw_Data.csv', index = False)
#data2
data2 = {'Post Content': contents}
df1 = pd.DataFrame(data2)
df1.to_csv('RawData _ Content', index = False)

#data3
data3 = {'Name':names, 'Decsriptions':descriptions}
df2 = pd.DataFrame(data3)
df2.to_csv('RawData _ Name', index = False)


#!/usr/bin/env python
# coding: utf-8

# In[22]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
#from requests_html import HTMLSession
import time
import pandas as pd


# In[23]:


#instantiate the Chrome class web driver and pass the Chrome Driver Manager
browser = webdriver.Chrome(ChromeDriverManager().install())

#Maximize the Chrome window to full-screen
browser.maximize_window() 


# In[24]:


#go to LinkedIN's Login page
#browser = HTMLSession()
browser.get('https://www.linkedin.com/login/')


# In[25]:


# login to account before starting to scrape

username = 'ginibasu@gmail.com'
password = 'Swastika@2418'
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()


# In[28]:


#  Get page source code
src = browser.page_source

for _ in range(1,3):
    browser.execute_script("window.scrollTo(1,200000)")
    print("scrolling")
    time.sleep(1)

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
    #content1 = soup.findAll('h2', attrs={'class': 'feed-shared-announcement__title t-14 t-black--light'})
contents = []
for i in content:
    c = i.get_text()
    contents.append({c})

personal_image = soup.findAll('img', attrs={'class': 'presence-entity__image ivm-view-attr__img--centered EntityPhoto-circle-3 feed-shared-actor__avatar-image EntityPhoto-circle-3 lazy-image ember-view'})
personal_images = []
for i in personal_image:
    #print(i['src'])
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


# In[29]:


#Clean Data
data = {'User Image url': pd.Series(personal_images),'Name':pd.Series(names), 'Decsriptions':pd.Series(descriptions),'Post Content': pd.Series(contents)}
df = pd.DataFrame(data)
#df.to_csv('RawData _ Image', index = False)
df.to_csv('C:/Users/DELL/PycharmProjects/linkedin/Clean_Data.csv', index = False)

#Raw Data
with open('C:/Users/DELL/PycharmProjects/linkedin/Raw_Data.txt','w',encoding='utf-8') as writer:
    writer.write(str(soup))

writer.close()


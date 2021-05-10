# -*- coding: utf-8 -*-
"""
@author: Jake
"""

import pandas as pd
import time
import tkinter as tk

#import frontend
from frontend.social_hub_gui import SocialHubApp
import frontend.gui_controller as gc


# import backend
from scrappers.pinterest import PinterestScrapper
from scrappers.linkedin import LinkedinScrapper
from scrappers.instagram import InstagramScrapper
from scrappers.weheartit import WeheartitScrapper



# Interface for image objects will be a queue (list) of

static = True

# Scrapped data format
# postid - 2 letter social media prefix followed by 8 digit unique number
# likes - int
# category - string
# link - string image link
# data- string



usernamePinterest = 'jake.cerwin@yahoo.com'
passwordPinterest = 'datafocusedpythOn'

usernameLinkedIn  = 'jake.cerwin@yahoo.com'
passwordLinkedIn  = '1800317'


instagram_followers = ['carnegiemellon', 'iris_rover', 'mse_cmu']
weheartit_searches = ['tech', 'travel']


# create scrappers
linkedin = LinkedinScrapper(usernameLinkedIn, passwordLinkedIn)
pinterest = PinterestScrapper(usernamePinterest, passwordPinterest)
instagram = InstagramScrapper(instagram_followers)
weheartit = WeheartitScrapper(weheartit_searches)

#scrape
df_linkedin = linkedin.scrape()
df_pinterest = pinterest.scrape()
df_instagram = instagram.scrape()
df_weheartit = weheartit.scrape()

# save
df_pinterest.to_csv('data/pinterest.csv', index=False)
df_linkedin.to_csv('data/linkedin.csv', index=False)
df_instagram.to_csv('data/instagram.csv', index=False)
df_weheartit.to_csv('data/weheartit.csv', index=False)

linkedin.close()
pinterest.close()
weheartit.close()
instagram.close()

"""
pinterest = PinterestScrapper(username, password)
df = pinterest.scrape()
pinterest.refresh()
df = pinterest.scrape()
pinterest.close()
"""
"""
root = tk.Tk()
root.title("SocialHub1.0")
root.geometry('800x500')
root.resizable(0, 0)
root.configure(bg='orange')

# create menu
menu = tk.Menu(root)
item = tk.Menu(menu)
item.add_command(label='Exit', command=root.destroy)
item.add_command(label='Refresh', command=gc.refresh)
menu.add_cascade(label='File', menu=item)

root.config(menu=menu)
SocialHubApp(root).pack(side="top", fill="both", expand=True)
root.mainloop()
"""

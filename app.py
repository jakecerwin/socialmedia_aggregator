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



# Interface for image objects will be a queue (list) of

static = True

# Scrapped data format
# postid - 2 letter social media prefix followed by 8 digit unique number
# likes - int
# category - string
# link - string image link
# data- string

df_labels = pd.Series(['postid','likes','category','imagelink','data'])

usernamePinterest = 'jake.cerwin@yahoo.com'
passwordPinterest = 'datafocusedpythOn'

usernameLinkedIn  = 'jake.cerwin@yahoo.com'
passwordLinkedIn  = '1800317'

if not static:
    instagram_followers = ['carnegiemellon', 'iris_rover', 'mse_cmu', 'tartanathletics', 'cmusasc']
    weheartit_searches = ['tech', 'travel', 'plants', 'design']


    # create scrappers
    linkedin = LinkedinScrapper(usernameLinkedIn, passwordLinkedIn)
    pinterest = PinterestScrapper(usernamePinterest, passwordPinterest)
    instagram = InstagramScrapper(instagram_followers)
    weheartit = WeheartitScrapper(weheartit_searches)
    scrappers = [linkedin, pinterest, instagram, weheartit]
    scrapper_labels = ['linkedin', 'pinterest', 'instagram', 'weheartit']


    # scrape
    dfs = [pd.DataFrame(df_labels)] * len(scrappers)
    for i in range(len(scrappers)):

        try:
            df = scrappers[i].scrape()
            if df is not None:
                dfs[i] = df
        except:
            print("failure: " + scrapper_labels[i] )





    # save
    for i in range(len(scrappers)):
        dfs[i].to_csv('data/'+str(scrapper_labels[i])+'.csv', index=False)


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

if static:
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


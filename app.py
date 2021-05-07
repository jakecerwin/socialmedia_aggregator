# -*- coding: utf-8 -*-
"""
@author: Jake
"""

import pandas as pd
import time
import tkinter as tk

#import frontend
from frontend/social_hub_gui import SocialHubApp



# import backend
from scrappers.pinterest import PinterestScrapper
from scrappers.linkedin import LinkedinScrapper
from scrappers.instagram import InstagramScrapper
#from scrappers.weheartit

usernamePinterest = 'jake.cerwin@yahoo.com'
passwordPinterest = 'datafocusedpythOn'

usernameLinkedIn  = 'jake.cerwin@yahoo.com'
passwordLinkedIn  = '1800317'

""""
linkedin = LinkedinScrapper(usernameLinkedIn, passwordLinkedIn)
time.sleep(5)
df = linkedin.scrape()
breakpoint()
linkedin.close()
"""
"""
pinterest = PinterestScrapper(username, password)
df = pinterest.scrape()
pinterest.refresh()
df = pinterest.scrape()
pinterest.close()
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
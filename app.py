# -*- coding: utf-8 -*-
"""
@author: Jake
"""

import pandas as pd
import time, os, shutil
import tkinter as tk

#import frontend
from frontend.social_hub_gui import SocialHubApp
import frontend.gui_controller as gc


# import backend



# Interface for image objects will be a queue (list) of


# Scrapped data format
# postid - 2 letter social media prefix followed by 8 digit unique number
# likes - int
# category - string
# link - string image link
# data- string

df_labels = pd.Series(['postid','likes','category','imagelink','data'])
"""
usernamePinterest = 'jake.cerwin@yahoo.com'
passwordPinterest = 'datafocusedpythOn'

usernameLinkedIn  = 'jake.cerwin@yahoo.com'
passwordLinkedIn  = '1800317'
"""

# move example_data to data
shutil.rmtree('user_data', ignore_errors=True)
shutil.rmtree('data', ignore_errors=True)

shutil.copytree('default_user_data', 'user_data')
shutil.copytree('example_data', 'data')


# run application
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


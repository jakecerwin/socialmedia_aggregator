# -*- coding: utf-8 -*-
"""
Created on Tue May  4 11:28:55 2021
@author: Jake
"""

import tkinter as tk
from PIL import ImageTk, Image

import frontend.gui_controller as gc
import pandas as pd
import numpy as np
from frontend.main_page_gui import MainPage

from run import scrape

LARGEFONT = ("Verdana", 35)
idir = 'frontend/images/'

class AccountPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=500, bg='#3e433f')

        self.title_frame = TitleFrame(self)
        self.title_frame.pack()

        self.login = AccountFrame(self, controller)
        self.login.pack()


class AccountFrame(tk.Frame):
    def __init__(self, parent, controller):

        accounts = pd.read_csv('user_data/accounts.csv')
        following = pd.read_csv('user_data/instagram_follows.csv')
        topics = pd.read_csv('user_data/weheartit_topics.csv')
        followingstr,topicstr = '', ''

        for i, row in following.iterrows():
            #print(row.to_numpy()[0])
            if  followingstr != '' :
                followingstr += ', '
            followingstr += row.to_numpy()[0]


        for i, row in topics.iterrows():
            #print(row.to_numpy()[0])
            if topicstr!= '':
                topicstr += ', '
            topicstr += row.to_numpy()[0]



        pinterest = accounts.loc[accounts['media'] == 'pinterest']
        linkedin = accounts.loc[accounts['media'] == 'linkedin']

        self.pi_acc = tk.StringVar(value=pinterest['username'].to_numpy()[0])
        self.pi_pas = tk.StringVar(value=pinterest['password'].to_numpy()[0])
        self.lk_acc = tk.StringVar(value=linkedin['username'].to_numpy()[0])
        self.lk_pas = tk.StringVar(value=linkedin['password'].to_numpy()[0])



        self.ig = tk.StringVar(value=followingstr)
        self.wh = tk.StringVar(value=topicstr)

        tk.Frame.__init__(self, parent, width=600, height=400, bg='#3e433f')

        tk.Label(self, text='Pinterest Account:', fg='white', bg='#3e433f').grid(row=0, column=0)
        tk.Entry(self, textvariable=self.pi_acc).grid(row=0, column=1)
        tk.Label(self, text='Pinterest Password:', fg='white', bg='#3e433f').grid(row=1, column=0)
        tk.Entry(self, textvariable=self.pi_pas).grid(row=1, column=1)
        tk.Label(self, text='Linkedin Account:', fg='white', bg='#3e433f').grid(row=2, column=0)
        tk.Entry(self, textvariable=self.lk_acc).grid(row=2, column=1)
        tk.Label(self, text='Linkedin Password:', fg='white', bg='#3e433f').grid(row=3, column=0)
        tk.Entry(self, textvariable=self.lk_pas).grid(row=3, column=1)

        tk.Label(self, text='For the following seperate',
                 fg='white', bg='#3e433f').grid(row=4, column=0, sticky='e')
        tk.Label(self, text='search terms by commas',
                 fg='white', bg='#3e433f').grid(row=4, column=1, sticky='w')

        tk.Label(self, text='Instagram Accounts to follow:', fg='white', bg='#3e433f').grid(row=5, column=0)
        tk.Entry(self, textvariable=self.ig).grid(row=5, column=1)
        tk.Label(self, text='WeHeartIt Topics:', fg='white', bg='#3e433f').grid(row=6, column=0)
        tk.Entry(self, textvariable=self.wh).grid(row=6, column=1)




        """
        tk.Label(self, text='Name', fg='white', bg='#3e433f').grid(row=1, column=0, sticky='w')
        self.user_name = tk.Entry(self, textvariable=self.u_name).grid(row=1, column=1)
        tk.Label(self, text='Password', fg='white', bg='#3e433f').grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(self, textvariable=self.pw).grid(row=2, column=1)
        """
        tk.Label(self, text='click when ready', fg='white', bg='#3e433f').grid(row=7, column=0)
        tk.Button(self, text='submit', command=lambda: self.submit(controller)).grid(row=7, column=1)


    def submit(self, controller):

        #gc.log_in(self.u_name.get(), self.pw.get())


        df = pd.DataFrame(np.array([['pinterest', self.pi_acc.get(), self.pi_pas.get()],
                                     ['linkedin', self.lk_acc.get(),self.lk_pas.get()]]),
                                     columns=['media', 'username', 'password'], )

        df.to_csv('user_data/accounts.csv', index= False)

        ig = self.ig.get()
        ig_follows = ig.replace(' ', '').split(',')
        while True:
            try:
                ig_follows.remove("")
            except:
                break
        df = pd.DataFrame(ig_follows, columns=['account'])
        df.to_csv('user_data/instagram_follows.csv', index=False)

        wh = self.wh.get()
        wh_topics = wh.replace('  ', ' ').replace(', ', ',').replace(' ,', ',').split(',')
        while True:
            try:
                wh_topics.remove("")
            except:
                break
        df = pd.DataFrame(wh_topics, columns=['topic'])
        df.to_csv('user_data/weheartit_topics.csv', index=False)



        print('scraping')
        scrape()

        controller.load_main() # change to dynamic


class TitleFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400, height=200, bg='#3e433f')

        with Image.open(idir+'brand_logo.png') as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((400, 200), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self, image=self.profile_img, width=400, height=200, bg='#3e433f')
        self.profile_img_label.pack(pady=30)
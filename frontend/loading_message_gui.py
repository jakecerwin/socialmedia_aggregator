# -*- coding: utf-8 -*-
"""
@author:  Jake
"""

import tkinter as tk
from PIL import ImageTk, Image


LARGEFONT = ("Verdana", 35)
idir = 'frontend/images/'


class LoadingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=500, bg='#3e433f')

        self.title_frame = TitleFrame(self)
        self.title_frame.pack()

        self.login = LoadingFrame(self, controller)
        self.login.pack()

class LoadingFrame(tk.Frame):


    def __init__(self, parent, controller):


        tk.Frame.__init__(self, parent, width=600, height=400, bg='#3e433f')
        #tk.Label(self, text='Welcome to socialHub', fg='white', bg='#3e433f').grid(row=1, column=1, sticky='n')
        tk.Label(self, text='Use Static Data:', fg='white', bg='#3e433f').grid(row=2, column=0)

        """
        tk.Label(self, text='Name', fg='white', bg='#3e433f').grid(row=1, column=0, sticky='w')
        self.user_name = tk.Entry(self, textvariable=self.u_name).grid(row=1, column=1)
        tk.Label(self, text='Password', fg='white', bg='#3e433f').grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(self, textvariable=self.pw).grid(row=2, column=1)
        """
        tk.Label(self, text='Loading', fg='white', bg='#3e433f').grid(row=3, column=0)
        #tk.Button(self, text='launch', command=lambda: self.log_in(controller, self.static)).grid(row=3, column=1)




class TitleFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400, height=200, bg='#3e433f')

        with Image.open(idir+'brand_logo.png') as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((400, 200), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self, image=self.profile_img, width=400, height=200, bg='#3e433f')
        self.profile_img_label.pack(pady=30)
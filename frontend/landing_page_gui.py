# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:25:07 2021
@author: Vivian
"""

import tkinter as tk
from PIL import ImageTk, Image
from frontend/main_page_gui import MainPage
import frontend/gui_controller as gc

LARGEFONT = ("Verdana", 35)


class LandingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=500, bg='#3e433f')

        self.title_frame = TitleFrame(self)
        self.title_frame.pack()

        self.login = LoginFrame(self, controller)
        self.login.pack()


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        self.u_name = tk.StringVar()
        self.pw = tk.StringVar()

        tk.Frame.__init__(self, parent, width=600, height=400, bg='#3e433f')

        tk.Label(self, text='Name', fg='white', bg='#3e433f').grid(row=1, column=0, sticky='w')
        self.user_name = tk.Entry(self, textvariable=self.u_name).grid(row=1, column=1)
        tk.Label(self, text='Password', fg='white', bg='#3e433f').grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(self, textvariable=self.pw).grid(row=2, column=1)
        tk.Button(self, text='login', command=lambda: self.log_in(controller)).grid(row=3, column=1)

    def log_in(self, controller):
        gc.log_in(self.u_name.get(), self.pw.get())
        controller.show_frame(MainPage)


class TitleFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400, height=200, bg='#3e433f')

        with Image.open('brand_logo.PNG') as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((400, 200), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self, image=self.profile_img, width=400, height=200, bg='#3e433f')
        self.profile_img_label.pack(pady=30)
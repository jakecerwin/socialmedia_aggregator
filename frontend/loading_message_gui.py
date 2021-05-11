# -*- coding: utf-8 -*-
"""
@author:  Jake
"""

import tkinter as tk
from PIL import ImageTk, Image
from frontend.main_page_gui import MainPage
import frontend.gui_controller as gc


LARGEFONT = ("Verdana", 35)
idir = 'frontend/images/'


class LandingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=800, height=500, bg='#3e433f')

        self.title_frame = TitleFrame(self)
        self.title_frame.pack()

        self.login = LoginFrame(self, controller)
        self.login.pack()


class TitleFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400, height=200, bg='#3e433f')

        with Image.open(idir+'brand_logo.png') as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((400, 200), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self, image=self.profile_img, width=400, height=200, bg='#3e433f')
        self.profile_img_label.pack(pady=30)
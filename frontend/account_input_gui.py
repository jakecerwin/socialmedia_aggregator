import tkinter as tk
from PIL import ImageTk, Image
from frontend.main_page_gui import MainPage
import frontend.gui_controller as gc
import pandas as pd

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
        self.u_name = tk.StringVar()
        self.pw = tk.StringVar()

        tk.Frame.__init__(self, parent, width=600, height=400, bg='#3e433f')
        #tk.Label(self, text='Welcome to socialHub', fg='white', bg='#3e433f').grid(row=1, column=1, sticky='n')
        tk.Label(self, text='Instagram Password:', fg='white', bg='#3e433f').grid(row=2, column=0)
        if self.static:
            tk.Button(self, image=self.on, text='use example data',
                      fg='#3e433f', bg='#3e433f',
                      command=lambda: self.toggle()).grid(row=2, column=1)
        else:
            tk.Button(self, image=self.ff, text='use example data',
                      fg='#3e433f', bg='#3e433f',
                      command=lambda: self.toggle()).grid(row=2, column=1)
        """
        tk.Label(self, text='Name', fg='white', bg='#3e433f').grid(row=1, column=0, sticky='w')
        self.user_name = tk.Entry(self, textvariable=self.u_name).grid(row=1, column=1)
        tk.Label(self, text='Password', fg='white', bg='#3e433f').grid(row=2, column=0, sticky='w')
        self.password = tk.Entry(self, textvariable=self.pw).grid(row=2, column=1)
        """
        tk.Label(self, text='click when ready', fg='white', bg='#3e433f').grid(row=3, column=0)
        tk.Button(self, text='launch', command=lambda: self.log_in(controller, self.static)).grid(row=3, column=1)

    def log_in(self, controller, static):
        gc.log_in(self.u_name.get(), self.pw.get())
        if static:
            controller.show_frame(MainPage)
        else:
            print('scraping')
            scrape_test()
            print('done')
            controller.show_frame(MainPage) # change to dynamic


class TitleFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400, height=200, bg='#3e433f')

        with Image.open(idir+'brand_logo.png') as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((400, 200), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self, image=self.profile_img, width=400, height=200, bg='#3e433f')
        self.profile_img_label.pack(pady=30)
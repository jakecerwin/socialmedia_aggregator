# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:38:18 2021
@author: Vivian and Jake
"""

import tkinter as tk
from frontend.landing_page_gui import LandingPage
from frontend.main_page_gui import MainPage
from frontend.account_page_gui import AccountPage
import frontend.gui_controller as gc


class SocialHubApp(tk.Frame):

    # __init__ function for class SocialHub
    def __init__(self, parent, *args, **kwargs):
        # __init__ function for class Tk
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (LandingPage, AccountPage, MainPage,):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LandingPage)

    def load_main(self):
        for F in (LandingPage, AccountPage, MainPage,):
            frame = F(self.container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)


    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Driver Code
if __name__ == "__main__":
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
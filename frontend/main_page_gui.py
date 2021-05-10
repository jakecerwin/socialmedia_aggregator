# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:32:15 2021
@author: Vivian and Jake
"""

import tkinter as tk
from PIL import ImageTk, Image
import io
import requests
import frontend.gui_controller as gc

# import messagebox from tkinter module
import tkinter.messagebox
idir = 'frontend/images/'
ddir = 'data/graphs/'



class MainPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.img_ls = []

        # add variable here to store user_name, email
        pass

        # create frames for layout
        leftFrame = LeftFrame(self, controller)
        leftFrame.grid(row=0, column=0)

        # right = RightFrame(self)

        rightFrame = RightFrame(self)
        rightFrame.grid(row=0, column=1)
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(0, weight=1)
        rightFrame.grid_propagate(False)


class LeftFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=250, height=500, bg='#515151')

        # 1.1 profile pannel
        self.controller = controller
        self.left_upper = tk.Frame(self, width=250, height=130, bg='#515151')
        self.left_upper.pack(side='top', fill='both')
        self.static = True

        # profile img
        with Image.open(idir+"placeholder.png") as img:
            self.profile_img = ImageTk.PhotoImage(img.resize((60, 60), Image.ANTIALIAS))

        self.profile_img_label = tk.Label(self.left_upper, image=self.profile_img, width=60, height=60)
        self.profile_img_label.place(relx=0.1, rely=0.3)

        # profile name and account
        #self.profile_name = tk.Label(self.left_upper, text='Edit Accounts', fg='white', bg='#515151')
        #self.profile_email = tk.Label(self.left_upper, text='email goes here', fg='white', bg='#515151')
        self.profile_email= tk.Button(self.left_upper, text='Edit Accounts', fg="black", width=15, height=2,
                                      bg='#515151', command=self.load_account_page)
        #self.profile_name.place(relx=0.4, rely=0.3)
        self.profile_email.place(relx=0.4, rely=0.5)

        # 1.2 button pannel

        self.left_lower = tk.Frame(self, width=250, height=460, bg='#515151')
        self.left_lower.pack(side='bottom', fill='both')
        """
        # buttons
        self.b_all = tk.Button(self.left_lower, text='All', fg="black", width=25, height=2, bg='#dadada',
                               command=gc.filter_platform('all', parent.img_ls))
        self.b_ins = tk.Button(self.left_lower, text='Instagram', fg="black", width=25, height=2, bg='#dadada',
                               command=gc.filter_platform('instagram', parent.img_ls))
        self.b_pin = tk.Button(self.left_lower, text='Pinterest', fg="black", width=25, height=2, bg='#dadada',
                               command=gc.filter_platform('pinterest', parent.img_ls))
        self.b_link = tk.Button(self.left_lower, text='LinkedIn', fg="black", width=25, height=2, bg='#dadada',
                                command=gc.filter_platform('linkedIn', parent.img_ls))
        self.b_whi = tk.Button(self.left_lower, text='We Heart It', fg="black", width=25, height=2, bg='#dadada',
                               command=gc.filter_platform('weheartit', parent.img_ls))
        """

        with Image.open(ddir+"weheartit.png") as img:
            self.wh_graph_img = ImageTk.PhotoImage(img.resize((200, 180), Image.ANTIALIAS))

        with Image.open(ddir+"instagram.png") as img:
            self.ig_graph_img = ImageTk.PhotoImage(img.resize((200, 180), Image.ANTIALIAS))


        self.b_graph_ins = tk.Button(self.left_lower, image=self.ig_graph_img, fg="white", width=200, height=180,
                                     bg='#9fbac1', command=gc.display_likes('instagram'))
        self.b_graph_whi = tk.Button(self.left_lower, image=self.wh_graph_img, fg="White", width=200, height=180,
                                     bg='#9fbac1', command=gc.display_likes('weheartit'))
        """
        self.b_all.place(relx=0.1, rely=0)
        self.b_ins.place(relx=0.1, rely=0.15)
        self.b_pin.place(relx=0.1, rely=0.3)
        self.b_link.place(relx=0.1, rely=0.45)
        self.b_whi.place(relx=0.1, rely=0.6)
        """

        self.b_graph_ins.place(relx=0.09, rely=0)
        self.b_graph_whi.place(relx=0.09, rely=0.41)

    def load_account_page(self):
        print('account page')
        from frontend.account_page_gui import AccountPage
        #gc.log_in(self.u_name.get(), self.pw.get())
        #print('account page')
        self.controller.show_frame(AccountPage)

    #def refresh():


class RightFrame(tk.Frame):
    def __init__(self, parent, static=True):
        tk.Frame.__init__(self, parent, width=550, height=500, bg='#c4c4c4')
        # 2.1 vertical scroll bar

        self.canvas = tk.Canvas(self, bg='red', width=550, height=500)
        # canvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        # canvas.pack(side='left')
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)

        self.inner_frame = tk.Frame(self.canvas, width=550, height=500, bg='#c4c4c4')
        self.inner_frame.bind('<Configure>', self.on_configure)
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor='n')

        self.v_scroll = tk.Scrollbar(self, command=self.canvas.yview)
        self.v_scroll.grid(row=0, column=1, sticky='nsew')
        self.canvas.config(yscrollcommand=self.v_scroll.set)

        parent.img_ls = []
        # populate the frame
        if static:
            df = gc.read_static('example_data')
        else:
            df = gc.read_static()
        df_shuffled = df.sample(frac=1).reset_index(drop=True)

        """
        for ind in df.index:
            response = requests.get(df_shuffled['Urls'][ind])
            print(df_shuffled['Urls'][ind])
            try:
                image_bytes = io.BytesIO(response.content)
                img = Image.open(image_bytes)
                parent.img_ls.append(ImageTk.PhotoImage(img))
                tk.Button(self.inner_frame, image=parent.img_ls[ind], text='img: ' + str(ind), width=425, height=300,
                          bg='grey', fg='white').grid(column=0, row=ind, pady=8, padx=50)
                tk.Label(self.inner_frame, text='@' + df_shuffled['User'][ind], fg='white', bg='grey').grid(column=0,
                                                                                                            row=ind,
                                                                                                            pady=8,
                                                                                                            padx=50,
                                                                                                            sticky='NW')
                tk.Label(self.inner_frame, text='❤ ' + df_shuffled['Likes'][ind], fg='red', bg='grey').grid(column=0,
                                                                                                            row=ind,
                                                                                                            pady=8,
                                                                                                            padx=50,
                                                                                                            sticky='SE')
                img.close()
            except:
                print('failed')
                break
        """
        i = 0
        for _, row in df_shuffled.iterrows():
            try:
                response = requests.get(row['link'])
            except:
                continue

            image_bytes = io.BytesIO(response.content)
            img = Image.open(image_bytes)
            parent.img_ls.append(ImageTk.PhotoImage(img))
            tk.Button(self.inner_frame, image=parent.img_ls[i], text='img: ' + str(i), width=425, height=300,
                  bg='grey', fg='white').grid(column=0, row=i, pady=8, padx=50)
            tk.Label(self.inner_frame, text='@' + row['category'], fg='white', bg='grey').grid(column=0,
                                                                                                row=i,
                                                                                                pady=8,
                                                                                                padx=50,
                                                                                                sticky='NW')
            tk.Label(self.inner_frame, text='❤ ' + str(row['likes']), fg='red', bg='grey').grid(column=0,
                                                                                            row=i,
                                                                                            pady=8,
                                                                                            padx=50,
                                                                                            sticky='SE')
            img.close()
            i += 1





    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
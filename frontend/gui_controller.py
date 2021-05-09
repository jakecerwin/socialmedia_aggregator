# -*- coding: utf-8 -*-
"""
Created on Tue May  4 11:28:55 2021
@author: Vivian
"""
import pandas as pd


# refresh scrape data (at the menu button)
def refresh():
    pass


# filter the current displayed images by platform
def filter_platform(platform_name, img_ls):
    if platform_name == 'all':
        pass
    else:
        pass


def display_likes(platform_name):
    pass


def read_img(): # will replace on backend to negate csv reliance
    img_urls = pd.DataFrame(columns=['Urls', 'User', 'Likes'])
    i = 0
    with open('cleaned_pinterest.csv', 'rt', encoding='utf-8') as f:
        for l in f.readlines()[1:]:
            # img_urls.append(l.split(',')[0])
            img_urls.loc[i] = [l.split(',')[0], l.split(',')[1].split('@')[0], 'Pinterest']
            i += 1

    with open('weheartit.csv', 'rt', encoding='utf-8') as f:
        for l in f.readlines()[1:]:
            # img_urls.append(l.split(',')[0])
            img_urls.loc[i] = [l.split(',')[0], l.split(',')[1], l.split(',')[2].rstrip()]
            i += 1
    with open('weheartit.csv', 'rt', encoding='utf-8') as f:
        for l in f.readlines()[1:]:
            # img_urls.append(l.split(',')[0])
            img_urls.loc[i] = [l.split(',')[0], l.split(',')[1], l.split(',')[2].rstrip()]
            i += 1
    return img_urls


# send user_name and password
def log_in(user_name, password):
    pass

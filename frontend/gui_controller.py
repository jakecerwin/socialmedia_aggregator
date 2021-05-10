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


def read_static(dir='data'): # will replace on backend to negate csv reliance
    #img_urls = pd.DataFrame(columns=['postid','likes','category','link','data'])
    filenames = [dir+'/instagram.csv', dir+'/linkedin.csv', dir+'/pinterest.csv', dir+'/weheartit.csv']
    combined_df = pd.concat([pd.read_csv(f) for f in filenames])

    return combined_df


def read_imgs(df_dict):
    return None


# send user_name and password
def log_in(user_name, password):
    pass

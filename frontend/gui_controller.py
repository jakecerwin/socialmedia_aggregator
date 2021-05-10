# -*- coding: utf-8 -*-
"""
Created on Tue May  4 11:28:55 2021
@author: Vivian and Jake
"""
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt




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


def read_static(dir='example_data'): # will replace on backend to negate csv reliance
    #img_urls = pd.DataFrame(columns=['postid','likes','category','link','data'])
    filenames = [dir+'/instagram.csv', dir+'/linkedin.csv', dir+'/pinterest.csv', dir+'/weheartit.csv']
    combined_df = pd.concat([pd.read_csv(f) for f in filenames])

    instagram = pd.read_csv(dir+'/instagram.csv')
    weheartit = pd.read_csv(dir+'/weheartit.csv')
    user = instagram.groupby("category").mean()


    user.plot.bar()
    plt.title('Average Instagram Likes per Account')

    plt.xlabel('Number of Likes')
    plt.ylabel('Account')
    plt.xticks(rotation=0)
    plt.savefig('data/graphs/instagram.png')
    plt.close()

    user = weheartit.groupby("category").mean()


    user.plot.bar()
    plt.title('Average WeHeartIt Likes per Search Term')
    plt.xlabel('Number of Likes')
    plt.ylabel('Search Term')
    plt.xticks(rotation=0)
    plt.savefig('data/graphs/weheartit.png')
    plt.close()

    return combined_df


def read_imgs(df_dict):
    return None


# send user_name and password
def log_in(user_name, password):
    pass

"""
author Jake
"""

import pandas as pd
import numpy as np


from scrappers.pinterest import PinterestScrapper
from scrappers.linkedin import LinkedinScrapper
from scrappers.instagram import InstagramScrapper
from scrappers.weheartit import WeheartitScrapper

def graph(instagram, weheartit):
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt


    user = instagram.groupby("category").mean()



    user.plot.bar()
    plt.title('Average Instagram Likes per Account')

    plt.xlabel('Number of Likes')
    plt.ylabel('Account')
    plt.xticks(rotation=10)
    plt.savefig('data/graphs/instagram.png')
    plt.close()

    user = weheartit.groupby("category").mean()

    user.plot.bar()
    plt.title('Average WeHeartIt Likes per Search Term')
    plt.xlabel('Number of Likes')
    plt.ylabel('Search Term')
    plt.xticks(rotation=10)
    plt.savefig('data/graphs/weheartit.png')
    plt.close()

    return None


def scrape():

    accounts = pd.read_csv('user_data/accounts.csv')
    following = pd.read_csv('user_data/instagram_follows.csv')
    topics = pd.read_csv('user_data/weheartit_topics.csv')
    following_lst, topics_lst = [], []

    for i, row in following.iterrows():
        following_lst.append(row.to_numpy()[0])

    for i, row in topics.iterrows():
        topics_lst.append(row.to_numpy()[0])

    pinterest = accounts.loc[accounts['media'] == 'pinterest']
    linkedin = accounts.loc[accounts['media'] == 'linkedin']

    usernamePinterest = pinterest['username'].to_numpy()[0]
    passwordPinterest = pinterest['password'].to_numpy()[0]
    usernameLinkedIn = linkedin['username'].to_numpy()[0]
    passwordLinkedIn = linkedin['password'].to_numpy()[0]

    df_labels = pd.Series(['postid', 'likes', 'category', 'imagelink', 'data'])

    #usernamePinterest = 'jake.cerwin@yahoo.com'
    #passwordPinterest = 'datafocusedpythOn'

    #usernameLinkedIn = 'jake.cerwin@yahoo.com'
    #passwordLinkedIn = '1800317'
    instagram_followers = ['carnegiemellon', 'iris_rover', 'mse_cmu', 'tartanathletics', 'cmusasc']
    weheartit_searches = ['tech', 'travel', 'plants', 'design']
    instagram_followers = following_lst
    weheartit_searches = topics_lst

    # create scrappers
    linkedin = LinkedinScrapper(usernameLinkedIn, passwordLinkedIn)
    pinterest = PinterestScrapper(usernamePinterest, passwordPinterest)
    instagram = InstagramScrapper(instagram_followers)
    weheartit = WeheartitScrapper(weheartit_searches)
    scrappers = [linkedin, pinterest, instagram, weheartit]
    scrapper_labels = ['linkedin', 'pinterest', 'instagram', 'weheartit']

    # scrape
    dfs = [pd.DataFrame(df_labels)] * len(scrappers)
    for i in range(len(scrappers)):

        try:
            df = scrappers[i].scrape()
            if df is not None:
                dfs[i] = df
        except:
            print("failure: " + scrapper_labels[i])

    # save
    for i in range(len(scrappers)):
        dfs[i].to_csv('data/' + str(scrapper_labels[i]) + '.csv', index=False)


    linkedin.close()
    pinterest.close()
    weheartit.close()
    instagram.close()

    instagram = pd.read_csv('data/instagram.csv')
    weheartit = pd.read_csv('data/weheartit.csv')

    #graph(instagram, weheartit)


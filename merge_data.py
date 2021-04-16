import csv
import pandas as pd


datadir = 'data' #need to alter for mac vs pc

instagram = pd.read_csv(datadir + '/cleaned_instagram.csv')
pinterest = pd.read_csv(datadir + '/cleaned_pinterest.csv')
weheartit = pd.read_csv(datadir + '/cleaned_weheartit.csv')
linkedin = pd.read_csv(datadir + '/cleaned_linkedin.csv')

# create image link database
merged_images = open('merged_images.csv', 'w')
fieldnames = ['application id', 'association', 'link']
writer = csv.writer(merged_images)
writer.writerow(fieldnames)

for post in instagram.iterrows():
    post = post[1]
    id = 'ig' + str(post[0])
    author = post[1]
    link = post[3]
    writer.writerow([id, author, link])

for post in pinterest.iterrows():
    id = 'pt' + str(post[0])
    post = post[1]

    author = post['user']
    link = post['pin_url']
    writer.writerow([id, author, link])

i = 0
for post in weheartit.iterrows():

    id = 'wh' + str(post[0]) # Long term we need to replace this with a more robust id
    post = post[1]
    author = post['Tags'][1:-1]
    link = post['URLs']
    writer.writerow([id, author, link])
    i += 1

merged_images.close()
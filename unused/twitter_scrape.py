from urllib.request import urlopen
from bs4 import BeautifulSoup
file = "twitterBBC.csv"
f = open(file, "w")
Headers = "tweet_user, tweet_text,  replies,  retweets\n"
f.write(Headers)
url = "https://twitter.com/BBCWorld"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# Gets the tweet
tweets = soup.find_all("li", attrs={"class":"js-stream-item"})

# Writes tweet fetched in file
for tweet in tweets:
    try:
        if tweet.find('p',{"class":'tweet-text'}):
            tweet_user = tweet.find('span',{"class":'username'}).text.strip()
            tweet_text = tweet.find('p',{"class":'tweet-text'}).text.encode('utf8').strip()
            replies = tweet.find('span',{"class":"ProfileTweet-actionCount"}).text.strip()
            retweets = tweet.find('span', {"class" : "ProfileTweet-action--retweet"}).text.strip()
            # String interpolation technique
            f.write(f'{tweet_user},/^{tweet_text}$/,{replies},{retweets}\n')
    except: AttributeError
f.close()
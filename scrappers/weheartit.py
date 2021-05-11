# -*- coding: utf-8 -*-
# author Jake
#install selenium, chromedriver

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image 
import requests, io, hashlib
import pandas as pd
import numpy as np

class WeheartitScrapper:
    def __init__(self, terms, debug=False):
        options = webdriver.ChromeOptions()
        options.headless = not debug
        self.terms = terms
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.maximize_window()
        self.seen = 0

    #fetch urls of images
    def fetch_image_urls(self, query, max_links_to_fetch, sleep_between_interactions=1):
        def scroll_to_end():

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(sleep_between_interactions)

        # build the weheartit query
        search_url="https://weheartit.com/search/entries?utf8=%E2%9C%93&ac=0&query={q}"

        # load the page
        url = search_url.format(q=query)
        self.driver.get(url)

        image_urls = set()
        #df=pd.DataFrame(columns=['Urls','Users','Hearts'])
        df=pd.DataFrame(columns=['postid', 'likes', 'category', 'link', 'data'])

        postids = []
        likes = []
        categories = []
        links = []
        data = []

        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end()

            # get all image thumbnail results

            thumbnail_results = self.driver.find_elements_by_css_selector("img[class$='thumbnail']")

            number_results = len(thumbnail_results)

            #print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail to get the image behind it
                if image_count > max_links_to_fetch: break
                #print('Before img click')
                #img.click()
                #print('After img click')
                #time.sleep(sleep_between_interactions)

                #except Exception:
                #    breakpoint()
                #    continue

                #time.sleep(5)

                # extract image urls, usernames, and heart count
                actual_images=self.driver.find_elements_by_css_selector("img[alt*='image']")
                #users=self.driver.find_elements_by_css_selector("a[class*='js-blc js-blc-t-user']")
                users=self.driver.find_elements_by_css_selector("a[class*='js-heart-button'")

                hearts=self.driver.find_elements_by_css_selector("span[class*='js-heart-count']")
                #hearts=self.driver.find_elements_by_class_name('js-heart-count')

                '''print('Images=', len(actual_images))
                print('Users=', len(users))
                print('Hearts=',len(hearts))'''
                #print('User list=',[x.get_attribute('innerText') for x in users])
                #print('Hearts list=',[x.get_attribute('innerText') for x in hearts])


                for actual_image,user,heart_count in zip(actual_images,users,hearts):
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))
                        #print(actual_image.get_attribute('src'),user.text,heart_count.text)
                        self.seen += 1
                        image_count +=1
                        if image_count > max_links_to_fetch: break
                        postid = 'wh'+ str(self.seen).zfill(8)
                        #add the image url,username and hearts to df
                        #print(postid)

                        postids.append(postid)
                        likes.append(heart_count.get_attribute('innerText'))
                        categories.append('weheartit/' + query)
                        links.append(actual_image.get_attribute('src'))
                        data.append(user.get_attribute('data-hearter-username'))

                        #df.loc[len(df.index)]=[postid, heart_count.get_attribute('innerText'), query,

                        #                       actual_image.get_attribute('src'),user.get_attribute('data-hearter-username')]
                        #df.loc[len(df.index)]=\
                        #    [actual_image.get_attribute('src'),user.get_attribute('data-hearter-username'),heart_count.get_attribute('innerText')]
                        #df.loc[len(df.index)]=[actual_image.get_attribute('src'),user.get_attribute('innerText'),heart_count.get_attribute('innerText')]

                #image_count = len(image_urls)
                """
                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!\n\nImage details:\n")
                    time.sleep(5)
                    break
                """
            else:
                #print("Found:", len(image_urls), "image links, looking for more ...")
                return
                time.sleep(5)
                load_more_button = self.driver.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    self.driver.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        #return image_urls,users,hearts
        data = {
            'postid': np.array(postids),
            'likes': np.array(likes),
            'category': np.array(categories),
            'link': np.array(links),
            'data': np.array(data)
        }
        df = pd.DataFrame(data)

        return df


    #call functions to fetch urls and download images
    def search_and_download(self, search_term:str,target_path='./images',number_images=5):
        #target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

        #if not os.path.exists(target_folder):
        #    os.makedirs(target_folder)

        #with self.driver as self.driver:
        res = self.fetch_image_urls(search_term, number_images, sleep_between_interactions=0.5)
        #print(res)

        #uncomment to download images
        """
        print('\n\nDowloading images.......\n\n')
        time.sleep(3)
        #download scraped images
        for elem in list(res.Urls.values):
            self.persist_image(target_folder,elem)
        """

        #data in csv
        return res

    def scrape(self):
        #search term
        df = None
        for term in self.terms:
            if df is None:
                df = self.search_and_download(term)
            else:
                new_df = self.search_and_download(term)
                df = df.append(new_df, ignore_index =True)
        return df

    def edit_terms(self, terms):
        self.terms = terms
        return None

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    weheartit = WeheartitScrapper(['houseplants', 'trucks'], True)
    df = weheartit.scrape()
    weheartit.close()
    print(df.head())

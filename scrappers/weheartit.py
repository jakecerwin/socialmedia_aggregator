# -*- coding: utf-8 -*-

#install selenium, chromedriver

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image 
import requests, io, hashlib, os
import pandas as pd

debug = True

class weheartitScrapper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.headless = not debug

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.seen = set()

    #fetch urls of images
    def fetch_image_urls(self, query:str, max_links_to_fetch:int, sleep_between_interactions:int=1):
        def scroll_to_end():

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(sleep_between_interactions)

        # build the weheartit query
        search_url="https://weheartit.com/search/entries?utf8=%E2%9C%93&ac=0&query={q}"

        # load the page
        url = search_url.format(q=query)
        self.driver.get(url)

        image_urls = set()
        df=pd.DataFrame(columns=['Urls','Users','Hearts'])
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
                try:
                    #print('Before img click')
                    img.click()
                    #print('After img click')
                    time.sleep(sleep_between_interactions)

                except Exception:
                    continue
                self.driver.headless=True
                time.sleep(5)

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

                        #add the image url,username and hearts to df
                        df.loc[len(df.index)]=[actual_image.get_attribute('src'),user.get_attribute('data-hearter-username'),heart_count.get_attribute('innerText')]
                        #df.loc[len(df.index)]=[actual_image.get_attribute('src'),user.get_attribute('innerText'),heart_count.get_attribute('innerText')]

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!\n\nImage details:\n")
                    time.sleep(5)
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(30)
                return
                load_more_button = self.driver.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    self.driver.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        #return image_urls,users,hearts
        return df

    #to download images
    def persist_image(self, folder_path:str,url:str):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
            print(f"SUCCESS - saved {url} - as {file_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")


    #call functions to fetch urls and download images
    def search_and_download(self, search_term:str,target_path='./images',number_images=5):
        target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        #with self.driver as self.driver:
        res = self.fetch_image_urls(search_term, number_images, sleep_between_interactions=0.5)
        print(res)

        #uncomment to download images
        '''print('\n\nDowloading images.......\n\n')
        time.sleep(3)
        #download scraped images
        for elem in list(res.Urls.values):
            persist_image(target_folder,elem)'''

        #data in csv
        return res

    def scrape(self, terms):
        #search term
        df = None
        for term in terms:
            if df is None:
                df = self.search_and_download(term)
            else:
                new_df = self.search_and_download(term)
                df.append(new_df, ignore_index =True)

        return df

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    weheartit = weheartitScrapper()
    df = weheartit.scrape(['houseplants', 'trucks'])
    weheartit.close()
    print(df.head())

# -*- coding: utf-8 -*-

#install selenium, chromedriver

import time
from selenium import webdriver
from PIL import Image 
import requests, io, hashlib, os
import pandas as pd


#fetch urls of images
def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(sleep_between_interactions)    
    
    # build the weheartit query
    search_url="https://weheartit.com/search/entries?utf8=%E2%9C%93&ac=0&query={q}"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    df=pd.DataFrame(columns=['Urls','Users','Hearts'])
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        
        thumbnail_results=wd.find_elements_by_css_selector("img[class$='thumbnail']")
        
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
            wd.headless=True
            time.sleep(5)
            
            # extract image urls, usernames, and heart count    
            actual_images=wd.find_elements_by_css_selector("img[alt*='image']")
            #users=wd.find_elements_by_css_selector("a[class*='js-blc js-blc-t-user']")
            users=wd.find_elements_by_css_selector("a[class*='js-heart-button'")
            
            hearts=wd.find_elements_by_css_selector("span[class*='js-heart-count']")
            #hearts=wd.find_elements_by_class_name('js-heart-count')
            
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
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    #return image_urls,users,hearts
    return df



options=webdriver.ChromeOptions()
#options.add_experimental_option("excludeSwitces", ["ignore-certificate-errors"])

#options.add_argument('headless')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-gpu')
#options.add_argument('window-size=0x0')
#options.headless=True
#options.add_argument('start-maximized')
#options.add_argument('disable-infobars')
#options.add_argument('--disable-extensions')

driver=webdriver.Chrome(options=options)
#fetch_image_urls('houseplants', 5, driver)

#to download images
def persist_image(folder_path:str,url:str): 
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
def search_and_download(search_term:str,target_path='./images',number_images=5):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with driver as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
        print(res)
    
    #uncomment to download images
    '''print('\n\nDowloading images.......\n\n')
    time.sleep(3)
    #download scraped images
    for elem in list(res.Urls.values):
        persist_image(target_folder,elem)'''
        
    #data in csv
    res.to_csv('weheartit.csv', index=False)
        
#search term        
search_and_download('houseplants')
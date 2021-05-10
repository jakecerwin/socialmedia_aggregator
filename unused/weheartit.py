# -*- coding: utf-8 -*-

#install selenium, chromedriver

import time
from selenium import webdriver
from PIL import Image 
import requests, io, hashlib, os
import json
from csv import DictWriter

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
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results=wd.find_elements_by_css_selector("img[class$='thumbnail']")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector("img[alt$='image']")
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
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

    return image_urls


driver=webdriver.Chrome()

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

#write csv header        
def write_csv_header():
    with open("data/cleaned_weheartit.csv", "w+") as csv_file:
        fieldnames = ['URLs']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

#write urls to csv        
def write_csv(urls):
    with open("data/cleaned_weheartit.csv", "a+") as csv_file:
        fieldnames = ['URLs']
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()
        writer.writerow({'URLs':urls})

#call functions to fetch urls, download images, and write to csv and json       
def search_and_download(search_term:str,target_path='./images',number_images=5):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome() as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
    
    #start image download into images folder
    for elem in res:
        persist_image(target_folder,elem)
        
    #raw data into json file
    with open('data/raw_weheartit.json', 'w') as outfile:
        json.dump(tuple(res), outfile)
        
        
    #cleaned data in csv
    write_csv_header()
    for elem in res:
        write_csv(elem.rstrip())
        
#search term
search_and_download('houseplants')
import instascrape as ig
import json

raw_data = open("raw_data_instagram.json", "w")

handles = ['instagram', 'carnegiemellon', 'iris_rover']
handles = ['carnegiemellon', 'iris_rover']
# Instantiate the scraper objects

for handle in handles:


    profile = ig.Profile(handle)
    profile.scrape()
    profile_posts = profile.get_recent_posts()
    i = 0
    for post in profile_posts:

        json.dump(post.json_dict, raw_data, indent=2)


        print(post.json_dict['__typename'])
        if post.json_dict['__typename'] == 'GraphImage':

            datetime = post.upload_date.strftime("%Y-%m-%d:%Hh%Mm")
            post.download(f"photos/{handle}{datetime}.png")

            id = post.json_dict['id']
            display_url = post.json_dict['display_url']
            caption = post.json_dict['edge_media_to_caption']
            thumbnail = post.json_dict['thumbnail_resources'][0]['src']


            i += 1
            if i > 5:
                break
    


raw_data.close()


"""
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


ig_username = 'account_test88'
ig_password = 'E_z47GGp?y?965g'

browser = webdriver.Chrome(ChromeDriverManager().install())

wait = WebDriverWait(browser, 10)

login_elem = browser.find_element_by_xpath(
   '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')

second_page_flag = wait.until(EC.presence_of_element_located(
    (By.CLASS_NAME, "KPnG0")))  # util login page appear


user = browser.find_element_by_name("username")

passw = browser.find_element_by_name('password')

ActionChains(browser)\
    .move_to_element(user).click()\
    .send_keys(ig_username)\
    .move_to_element(passw).click()\
    .send_keys(ig_password)\
    .perform()

login_button_ = browser.find_element_by_xpath(
    "//form[@class='HmktE']/div[3]/button")

login_button_.click()
"""

"""
    url = 'https://www.instagram.com/'+handle+'/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    photos = soup.find_all('img', class_='FFVAD')


    breakpoint()
"""
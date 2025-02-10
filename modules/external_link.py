import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from modules.chrome import ChromeDriverManager
from config.channelId import CHANNELID

def collect_creators(browser: webdriver.Chrome, channel_name):
    time.sleep(5)
    # 링크 가져오기
    print(f"[INFO] starting to find all link.")
    elements = browser.find_element(By.CSS_SELECTOR, '#links-section').find_elements(By.TAG_NAME, "yt-channel-external-link-view-model")

    links_list = []
    for element in elements:
        img_link = element.find_element(By.TAG_NAME, "img").get_attribute("src")
        elems = element.find_elements(By.TAG_NAME, "span")
        external_link = elems[1].find_element(By.TAG_NAME, "a").get_attribute('href')
        links_list.append({
            "name": f"{elems[0].text}", 
            "image_link": img_link, 
            "external_link": external_link
            })

    print(f"[INFO] found all link in the channel: {' '.join(row['name'] for row in links_list)}")
    return links_list
import json
from time import sleep
from selenium.webdriver.common.by import By
from modules.Link.Chrome import ChromeManager
from config.channelid_config import CHANNELID

def collect_creators(channel_name):
    gh = ChromeManager(url=f"https://www.youtube.com/channel/{CHANNELID[channel_name]}/about")
    gh.process_Chrome()
    driver = gh.browser

    sleep(5)
    # 링크 가져오기
    elements = driver.find_element(By.CSS_SELECTOR, '#links-section').find_elements(By.TAG_NAME, "yt-channel-external-link-view-model")

    dic = {}
    for element in elements:
        img_link = element.find_element(By.TAG_NAME, "img").get_attribute("src")
        elems = element.find_elements(By.TAG_NAME, "span")
        external_link = elems[1].find_element(By.TAG_NAME, "a").get_attribute('href')
        dic[f"{elems[0].text}"] = {"image_link":img_link, "external_link":external_link}

    with open(f"./json/{channel_name}_LinkData.json", "w", encoding="utf-8") as file:
        json.dump(dic, file, ensure_ascii=False, indent=4)
    gh.terminate_chrome_process()
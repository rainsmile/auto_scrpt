import time

from PIL import ImageGrab
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import cv2
import numpy as np
import pyautogui


# 获取浏览器列表
def get_list(serial_number):
    url = f"http://local.adspower.net:50325/api/v1/user/list?serial_number={serial_number}"
    response = requests.get(url=url)
    res = response.json()
    print(res)
    if len(res['data']['list']) == 0:
        return False
    else:
        serial_number = res['data']['list'][0]['serial_number']
        user_id = res['data']['list'][0]['user_id']
        return user_id


# 根据adsPower打开浏览器
def open_ads_browser(user_id, serial_number):
    print("正在打开浏览器。。。")
    response = requests.get(f"http://local.adspower.net:50325/api/v1/browser/start?user_id={user_id}&serial_number={serial_number}")
    print(response.json())
    selenium_host = response.json()['data']['ws']['selenium']
    chrome_path = response.json()["data"]["webdriver"]
    return selenium_host, chrome_path


# 连接adsPower浏览器
def connect_browser(selenium_host, path):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", selenium_host)
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.set_page_load_timeout(600)
    driver.implicitly_wait(30)
    driver.maximize_window()
    time.sleep(3)
    current_window = driver.current_window_handle
    all_windows = driver.window_handles
    for i in range(1, len(all_windows)):
        driver.switch_to.window(all_windows[i])
        driver.close()
    driver.switch_to.window(all_windows[0])
    print(all_windows, current_window)
    print("连接浏览器成功")
    return driver


# 通过xpath定位元素
def find_element_by_xpath(driver, xpath, timeout=10):
    element = WebDriverWait(driver, timeout=timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


def search_returnPoint(pic_file):
    screen_size = pyautogui.size()
    scale = 1
    img = cv2.imread('page.png')  # 要找的大图
    img_width = img.shape[1]
    img_height = img.shape[0]
    width_scale = img_width / screen_size.width
    height_scale = img_height / screen_size.height
    img = cv2.resize(img, (0, 0), fx=1, fy=1)
    template = cv2.imread(pic_file)
    template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
    template_size = template.shape[:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_ = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template_,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)
    point = ()
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + template_size[1], pt[1] + + template_size[0]), (7, 249, 151), 2)
        point = pt
    x_ = point[0] + template_size[1]/2
    y_ = point[1]
    pyautogui.moveTo(x_/width_scale, y_/height_scale+10, duration=1)
    pyautogui.click()
    print(f"定位下一步坐标({x_/width_scale}, {y_/height_scale+10})")
    return x_/width_scale, y_/height_scale


def connect_wallet(driver):
    url = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#unlock'
    driver.get(url)
    try:
        xpath = '//*[@id="password"]'
        element = find_element_by_xpath(driver, xpath)
        element.send_keys('weiyijia1993')
        xpath = '//*[@id="app-content"]/div/div[2]/div/div/button'
        element = find_element_by_xpath(driver, xpath)
        element.click()
        # xpath = '//*[@id="app-content"]/div/div[3]/div/div[5]/footer/button[2]'
        # element = find_element_by_xpath(driver, xpath)
        # element.click()
    except:
        pass
    time.sleep(2)
    driver.get('https://arcana.p12.games/')
    try:
        xpath = '//*[@id="__next"]/div/div[1]/div[1]/div[2]/button'
        element = find_element_by_xpath(driver, xpath)
        element.click()
    except:
        print("已经登录")
    else:
        xpath = '//*[@id=":r0:"]/div/div/button[1]'
        element = find_element_by_xpath(driver, xpath)
        element.click()
        time.sleep(10)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign.png")
        pyautogui.scroll(-500)
        time.sleep(1)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign_in.png")
        print("登录钱包成功")


def vote(driver, key_word):
    driver.get('https://arcana.p12.games/')
    xpath = '//*[@id="galleryLeaderboard"]/div[1]/div[2]/div[2]/div/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys(key_word)
    xpath = '//*[@id="galleryLeaderboard"]/div[1]/div[2]/div[2]/div/img'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    time.sleep(2)
    xpath = '//*[@id="galleryLeaderboard"]/div[2]/div[1]/div/div[1]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id=":rg:"]/div/div[2]/div[5]/div[2]/div[1]/p[2]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id=":rg:"]/div/div[2]/div[5]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 获取12票
    driver.get('https://arcana.p12.games/')
    xpath = '//*[@id="task"]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id="panel:r6:1"]/div/div/div[2]/div/div[2]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 再次投票
    driver.get('https://arcana.p12.games/')
    xpath = '//*[@id="galleryLeaderboard"]/div[1]/div[2]/div[2]/div/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys(key_word)
    xpath = '//*[@id="galleryLeaderboard"]/div[1]/div[2]/div[2]/div/img'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    time.sleep(2)
    xpath = '//*[@id="galleryLeaderboard"]/div[2]/div[1]/div/div[1]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id=":rg:"]/div/div[2]/div[5]/div[2]/div[1]/p[2]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id=":rg:"]/div/div[2]/div[5]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()


def close_browser(user_id):
    url = f'http://local.adspower.net:50325/api/v1/browser/stop?user_id={user_id}'
    requests.get(url=url)


if __name__ == "__main__":
    # 搜索关键字
    key_words = '长伴君存'
    f = open('task_id.txt')
    task_id = f.read()
    f.close()
    ts_l = task_id.split(',')
    for i in range(len(ts_l)):
        if ts_l[i].find('-') != -1:
            for s_num in range(int(ts_l[i].split('-')[0]), int(ts_l[i].split('-')[1]) + 1):
                user_id = get_list(s_num)
                host, selenium_path = open_ads_browser(user_id, s_num)
                if host:
                    browser = connect_browser(host, selenium_path)
                    connect_wallet(browser)
                    vote(driver=browser, key_word=key_words)
                    close_browser(user_id)
                else:
                    time.sleep(1)
        else:
            user_id = get_list(int(ts_l[i]))
            host, selenium_path = open_ads_browser(user_id, int(ts_l[i]))
            if host:
                browser = connect_browser(host, selenium_path)
                connect_wallet(browser)
                vote(driver=browser, key_word=key_words)
                close_browser(user_id)
            else:
                time.sleep(1)


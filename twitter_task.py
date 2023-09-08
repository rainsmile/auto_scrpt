import time
from PIL import ImageGrab
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
import numpy as np
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sys import platform
import json
import re


# 获取所有浏览器
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
    if response.json()['code'] == 0:
        selenium_host = response.json()['data']['ws']['selenium']
        chrome_path = response.json()["data"]["webdriver"]
        return selenium_host, chrome_path
    else:
        return False, False


# 连接adsPower浏览器
def connect_browser(selenium_host, path):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", selenium_host)
    driver = webdriver.Chrome(path, options=chrome_options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    time.sleep(5)
    current_window = driver.current_window_handle
    all_windows = driver.window_handles
    for i in range(1, len(all_windows)):
        driver.switch_to.window(all_windows[i])
        driver.close()
    driver.switch_to.window(all_windows[0])
    # if serial_number != driver.title:
    #     driver.switch_to.window(all_windows[0])
    print(all_windows, current_window)
    print("连接浏览器成功")
    return driver


def close_browser(user_id):
    url = f'http://local.adspower.net:50325/api/v1/browser/stop?user_id={user_id}'
    requests.get(url=url)


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
    except:
        pass


# 通过xpath定位元素
def find_element_by_xpath(driver, xpath, timeout=10):
    element = WebDriverWait(driver, timeout=timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


def twitter_task_1(driver):
    driver.get(
        'https://galxe.com/zkLink/campaign/GCn45UjHXE?referral_code=GRFr2JtzOqH43bjiZtUCLzEikm0GkemXYOvrO4UE_0E6Asv')
    time.sleep(1)
    cookies = driver.get_cookies()
    cookie_names = [i['name'] for i in cookies]
    if 'auth-token' not in cookie_names:
        return False
    # 第一个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 2)
    except:
        print("第一个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 第二个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[2]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 1)
    except:
        print("第二个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[2]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 第三个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[3]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 1)
    except:
        print("第三个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[3]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 第四个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[5]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 1)
    except:
        print("第四个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[5]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 第五个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[6]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 1)
    except:
        print("第五个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[6]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 第六个任务
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[7]/div/div[2]/div[1]/div/button/div[2]/div/div/div/div/div'
        find_element_by_xpath(driver, xpath, 1)
    except:
        print("第六个任务已做完")
    else:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[7]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(windows[0])
    # 刷新页面
    time.sleep(5)
    driver.refresh()
    return True


if __name__ == "__main__":
    f = open('task_id.txt')
    task_id = f. read()
    f.close()
    ts_l = task_id.split(',')
    for i in range(len(ts_l)):
        if ts_l[i].find('-') != -1:
            for s_num in range(int(ts_l[i].split('-')[0]), int(ts_l[i].split('-')[1])+1):
                user_id = get_list(s_num)
                host, selenium_path =  open_ads_browser(user_id, s_num)
                if host:
                    browser = connect_browser(host, selenium_path)
                    # connect_wallet(browser)
                    if twitter_task_1(browser):
                        print(f"页面{s_num}:任务完成")
                    else:
                        print(f"页面{s_num}未绑定推特")
                    close_browser(user_id)
                else:
                    time.sleep(1)
        else:
            user_id = get_list(int(ts_l[i]))
            host, selenium_path = open_ads_browser(user_id, int(ts_l[i]))
            if host:
                browser = connect_browser(host, selenium_path)
                # connect_wallet(browser)
                if twitter_task_1(browser):
                    print(f"页面{ts_l[i]}:任务完成")
                else:
                    print(f"页面{ts_l[i]}未绑定推特")
                close_browser(user_id)
            else:
                time.sleep(1)
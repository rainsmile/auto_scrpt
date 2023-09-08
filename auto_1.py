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
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(20)
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
        print("小狐狸钱包未注册或者已经登录")


def task(driver, email):
    url = "https://galxe.com/zkLink/campaign/GCi1dUDXE2"
    driver.get(url=url)
    try:
        xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div/div/div[3]/div[1]/div/button/div[2]/div/div/button'
        element = find_element_by_xpath(driver, xpath)
        element.click()
        xpath = '//*[@id="app"]/div[3]/div/div/div/div[3]/div[2]/input'
        element = find_element_by_xpath(driver, xpath)
        element.send_keys(email)
        xpath = '//*[@id="app"]/div[3]/div/div/div/div[3]/div[2]/button'
        element = find_element_by_xpath(driver, xpath)
        element.click()
    except Exception:
        pass
    time.sleep(10)
    # js = "window.open('{}','_blank');"
    # driver.execute_script(js.format('https://mail.google.com/mail/u/0/#inbox'))
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    xpath = '//*[@id=":1h"]/tbody/tr[1]/td[5]/div/div/span'
    element = find_element_by_xpath(driver, xpath, 5)
    temp = element.text
    code = re.findall('[0-9]{6}', temp)
    print(code[0])
    # driver.close()
    driver.switch_to.window(windows[0])
    xpath = '//*[@id="app"]/div[3]/div/div/div/div[4]/div[2]/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys(code[0])
    xpath = '//*[@id="app"]/div[3]/div/div/div/div[5]/div[1]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()


# 通过xpath定位元素
def find_element_by_xpath(driver, xpath, timeout=10):
    element = WebDriverWait(driver, timeout=timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


def google_login(driver, email, pwd, f_email):
    time.sleep(2)
    driver.get('https://accounts.google.com/v3/signin/identifier?hl=zh-CN&ifkv=AXo7B7X1pNnLWKkOnZPFRtvBClFI6Sdg91sBQVAFdLgPWj1nTnLbk6ycWnb7nWIa-JVZP7NI5GrU&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1106860416%3A1693410288051665')
    xpath = '//*[@id="identifierId"]'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys(email)
    xpath = '//*[@id="identifierNext"]/div/button/span'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys(pwd)
    xpath = '//*[@id="passwordNext"]/div/button/span'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    try:
        xpath = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/section/div/div/div/ul/li[3]/div/div[2]'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        xpath = '//*[@id="knowledge-preregistered-email-response"]'
        element = find_element_by_xpath(driver, xpath, 5)
        element.send_keys(f_email)
        time.sleep(2)
        xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
    except Exception:
        pass
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    try:
        xpath = '//*[@id=":4z.contentEl"]/div/div[2]/div[3]/label/span'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        xpath = '/html/body/div[20]/div[3]/button'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
        xpath = '/html/body/div[20]/div[3]/button[1]'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
    except:
        pass
    driver.refresh()


def get_code(driver):
    driver.get('https://mail.google.com/mail/u/0/#inbox')
    # windows = driver.window_handles
    # driver.switch_to.window(windows[-1])
    xpath = '//*[@id=":1h"]/tbody/tr[1]/td[5]/div/div/span'
    element = find_element_by_xpath(driver, xpath, 5)
    temp = element.text
    print(temp)
    code = re.findall('[0-9]{6}', temp)
    print(code[0])


def twitter_task_1(driver):
    driver.get(
        'https://galxe.com/zkLink/campaign/GCn45UjHXE?referral_code=GRFr2JtzOqH43bjiZtUCLzEikm0GkemXYOvrO4UE_0E6Asv')
    time.sleep(1)
    cookies = driver.get_cookies()
    cookie_names = [i['name'] for i in cookies]
    if 'auth-token' not in cookie_names:
        return False
    # 第一个任务
    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[1]/div/button/div[2]'

    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[1]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
    element = find_element_by_xpath(driver, xpath, 5)
    element.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(windows[0])
    # 第二个任务
    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[2]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
    element = find_element_by_xpath(driver, xpath, 5)
    element.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(windows[0])
    # 第三个任务
    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[3]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
    element = find_element_by_xpath(driver, xpath, 5)
    element.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(windows[0])
    # 第四个任务
    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[5]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
    element = find_element_by_xpath(driver, xpath, 5)
    element.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(windows[0])
    # 第五个任务
    xpath = '//*[@id="ga-data-campaign-model-2"]/div[2]/div[1]/div[2]/div[5]/div/div[1]/div[6]/div/div[2]/div[1]/div/button/div[1]/div[2]/div'
    element = find_element_by_xpath(driver, xpath, 5)
    element.click()
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    time.sleep(1)
    driver.close()
    driver.switch_to.window(windows[0])
    # 第六个任务
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
    f = open('email.txt')
    task_emails = f. readlines()
    f.close()
    f = open('task_id.txt')
    task_id = f.read()
    f.close()
    ts_l = task_id.split(',')
    m = 0
    for i in range(len(ts_l)):
        if ts_l[i].find('-') != -1:
            for s_num in range(int(ts_l[i].split('-')[0]), int(ts_l[i].split('-')[1]) + 1):
                user_id = get_list(s_num)
                host, selenium_path = open_ads_browser(user_id, s_num)
                if host:
                    browser = connect_browser(host, selenium_path)
                    connect_wallet(browser)
                    try:
                        google_login(browser, task_emails[m].split('----')[0], task_emails[m].split('----')[1],
                                     task_emails[m].split('----')[2])
                        print(f"第{m}个邮箱已注册成功")
                        task(browser, task_emails[m].split('----')[0])
                        print(f"第{m}个邮箱已绑定成功")
                        m += 1
                    except IndexError:
                        print("谷歌邮箱数量不足")
                    close_browser(user_id)
                else:
                    time.sleep(1)
        else:
            user_id = get_list(int(ts_l[i]))
            host, selenium_path = open_ads_browser(user_id, int(ts_l[i]))
            if host:
                browser = connect_browser(host, selenium_path)
                connect_wallet(browser)
                try:
                    google_login(browser, task_emails[m].split('----')[0], task_emails[m].split('----')[1],
                                 task_emails[m].split('----')[2])
                    print(f"第{m}个邮箱已注册成功")
                    task(browser, task_emails[m].split('----')[0])
                    print(f"第{m}个邮箱已绑定成功")
                    m += 1
                except IndexError:
                    print("谷歌邮箱不足")
                close_browser(user_id)
            else:
                time.sleep(1)
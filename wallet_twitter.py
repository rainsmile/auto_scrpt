import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


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


# 创建分组
def search_group():
    url = 'http://local.adspower.net:50325/api/v1/group/list'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    if len(response.json()['data']['list']) == 0:
        return 0
    else:
        return response.json()['data']['list'][0]['group_id']


# 创建页面
def create_browser(group_id=0):
    url = "http://local.adspower.net:50325/api/v1/user/create"
    payload = json.dumps({
        "group_id": group_id,
        "user_proxy_config": {
            "proxy_soft": "other",
            "proxy_type": "socks5",
            "proxy_host": "d46201e0.singapore.socks5.ltd",
            "proxy_port": "49299",
            "proxy_user": "0fee772e",
            "proxy_password": "9acd341f"
        },
        "fingerprint_config": {
            "automatic_timezone": 1,
            "language": [
                "en-US",
                "en"
            ],
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36",
            "flash": "block",
            "browser_kernel_config": {
                "version": "ua_auto",
                "type": "chrome"
            },
            "scan_port_type": "1",
            "allow_scan_ports": "",
            "location": "ask",
            "device_name_switch": "1",
            "device_name": "",
            "speech_switch": "1",
            "location_switch": "1",
            "language_switch": "1",
            "accuracy": "1000",
            "screen_resolution": "none",
            "mac_address_config": {
                "model": "1",
                "address": ""
            },
            "media_devices": "1",
            "canvas": "1",
            "client_rects": "1",
            "webgl": "3",
            "webgl_config": {
                "unmasked_vendor": "Google Inc. (ATI Technologies Inc.)",
                "unmasked_renderer": "ANGLE (AMD, AMD Radeon Pro 560X OpenGL Engine, OpenGL 4.1)"
            },
            "webgl_image": "1",
            "audio": "1",
            "webrtc": "disabled",
            "do_not_track": "default",
            "hardware_concurrency": "12",
            "device_memory": "8",
            "gpu": "0"
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    user_id = response.json()['data']['id']
    serial_number = response.json()['data']['serial_number']
    print(f"创建新浏览器成功，用户ID：{user_id}，浏览器编号：{serial_number}")
    return user_id, serial_number


# 根据adsPower打开浏览器
def open_ads_browser(user_id, serial_number):
    print("正在打开浏览器。。。")
    response = requests.get(f"http://local.adspower.net:50325/api/v1/browser/start?user_id={user_id}&serial_number={serial_number}")
    print(response.json())
    selenium_host = response.json()['data']['ws']['selenium']
    chrome_path = response.json()["data"]["webdriver"]
    with open('selenium.txt', 'w') as f:
        f.write(f'{selenium_host}&{chrome_path}')
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
    # if serial_number != driver.title:
    #     driver.switch_to.window(all_windows[0])
    print(all_windows, current_window)
    print("连接浏览器成功")
    return driver


# 通过xpath定位元素
def find_element_by_xpath(driver, xpath, timeout=10):
    element = WebDriverWait(driver, timeout=timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return element


# 创建小狐狸钱包账号
def create_wallet(driver):
    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#onboarding/welcome')
    # 勾选使用条款
    time.sleep(3)
    try:
        xpath = '//*[@id="onboarding__terms-checkbox"]'
        element = find_element_by_xpath(driver, xpath)
        element.click()
    except WebDriverException:
        time.sleep(3)
        xpath = '//*[@id="onboarding__terms-checkbox"]'
        element = find_element_by_xpath(driver, xpath)
        element.click()
    # 点击创建新钱包
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/ul/li[2]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击我同意
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div/button[1]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 输入新密码
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[1]/label/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys("weiyijia1993")
    # 输入确认密码
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[2]/label/input'
    element = find_element_by_xpath(driver, xpath)
    element.send_keys("weiyijia1993")
    # 勾选我明白了
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/div[3]/label/input'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击创建新钱包
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/form/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击保护我的钱包
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button[2]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击显示助记词
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[6]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 获取助记词
    mnemonic_words = []
    for i in range(1, 13):
        xpath = f'//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div/div[{i}]/div[2]'
        element = find_element_by_xpath(driver, xpath)
        mnemonic_word = element.text
        mnemonic_words.append(mnemonic_word)
    # 点击下一步
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[6]/div/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 判断需要填写的助记词
    elements = driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div')
    for i in range(len(elements)):
        if elements[i].find_element_by_xpath('.//div[2]').text == '':
            xpath = f'//*[@id="app-content"]/div/div[2]/div/div/div/div[4]/div/div[{i+1}]/div[2]/input'
            element = find_element_by_xpath(driver, xpath)
            element.send_keys(mnemonic_words[i])
    # 点击确认
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击知道了
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击下一步
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 点击完成
    xpath = '//*[@id="app-content"]/div/div[2]/div/div/div/div[2]/button'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    print("创建钱包成功")
    return


# 绑定推特
def connect_twitter(driver, twitter_token):
    driver.get('https://twitter.com/?lang=zh')
    # 注入cookie
    print({"name": 'auth_token', "value": twitter_token})
    driver.add_cookie({"name": 'auth_token', "value": twitter_token})
    driver.refresh()
    print("进入Twitter")


if __name__ == "__main__":
    group_id_ = search_group()
    twitter_f = open('twitter.txt', 'r')
    twitter_tokens = twitter_f.readlines()
    twitter_f.close()
    f = open('task_id.txt')
    task_id = f.read()
    f.close()
    ts_l = task_id.split(',')
    if len(task_id) == 0:
        for i in range(len(twitter_tokens)):
            id, serial_id = create_browser(group_id_)
            host, chrome_driver = open_ads_browser(id, serial_id)
            browser = connect_browser(host, chrome_driver)
            create_wallet(browser)
            twitter_token_ = twitter_tokens[i].split('----')[-1]
            connect_twitter(browser, twitter_token_.replace('\n', ''))
            browser.close()
    else:
        m = 0
        for i in range(len(ts_l)):
            if ts_l[i].find('-') != -1:
                for s_num in range(int(ts_l[i].split('-')[0]), int(ts_l[i].split('-')[1]) + 1):
                    user_id = get_list(s_num)
                    host, selenium_path = open_ads_browser(user_id, s_num)
                    if host:
                        browser = connect_browser(host, selenium_path)
                        create_wallet(browser)
                        twitter_token_ = twitter_tokens[m].split('----')[-1]
                        connect_twitter(browser, twitter_token_.replace('\n', ''))
                        m += 1
                        browser.close()
                    else:
                        time.sleep(1)
            else:
                user_id = get_list(int(ts_l[i]))
                host, selenium_path = open_ads_browser(user_id, int(ts_l[i]))
                if host:
                    browser = connect_browser(host, selenium_path)
                    create_wallet(browser)
                    twitter_token_ = twitter_tokens[m].split('----')[-1]
                    connect_twitter(browser, twitter_token_.replace('\n', ''))
                    m += 1
                    browser.close()
                else:
                    time.sleep(1)


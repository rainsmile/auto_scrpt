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
with open('step.txt', 'r') as f:
    s = f.read()
    if s == "":
        step_num = 0
    else:
        step_num = float(s)


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
    driver.switch_to.window(driver.current_window_handle)
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


def connect_wallet(driver):
    global step_num
    try:
        if step_num != 1:
            driver.get('https://galxe.com/OmniNetwork/campaign/GCoi5UXwTa')
        # 点击connect
        xpath = '//*[@id="topNavbar"]/div/div[2]/div[2]/div[1]/div[2]'
        element = find_element_by_xpath(driver, xpath)
        element.click()
        # 点击小狐狸钱包 //*[@id="app"]/div[3]/div/div/div/div[2]/div[2]/div
        xpath = '//*[@id="app"]/div'
        elements = driver.find_elements_by_xpath(xpath)
        xpath = f'//*[@id="app"]/div[{len(elements)-2}]/div/div/div/div[2]/div[2]/div'
        print(xpath)
        element = find_element_by_xpath(driver, xpath)
        element.click()
        # 截图
        time.sleep(3)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint('next.png')
        time.sleep(2)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint('connect.png')
        print("绑定钱包成功")
    finally:
        with open('step.txt', 'w') as f:
            f.write('1')
    try:
        time.sleep(15)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign.png")
        pyautogui.scroll(-500)
        time.sleep(1)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign_in.png")
        print("绑定Twitter成功")
    except Exception:
        time.sleep(15)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign.png")
        pyautogui.scroll(-500)
        time.sleep(1)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign_in.png")
        print("绑定Twitter成功")


def search_returnPoint(pic_file):
    screen_size = pyautogui.size()
    scale = 1
    img = cv2.imread('page.png')  # 要找的大图
    img_width = img.shape[1]
    img_height = img.shape[0]
    width_scale = img_width / screen_size.width
    height_scale = img_height / screen_size.height
    img = cv2.resize(img, (0, 0), fx=1, fy=1)
    template = cv2.imread(pic_file)  # 图中的小图
    template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
    template_size = template.shape[:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template_ = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template_,cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    # res大于70%
    loc = np.where(result >= threshold)
    # 使用灰度图像中的坐标对原始RGB图像进行标记
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


# 绑定推特
def connect_twitter(driver, twitter_token):
    global step_num
    try:
        # 登陆推特
        if step_num < 2 or step_num >= 3:
            driver.get('https://twitter.com/?lang=zh')
            # 注入cookie
            print({"name": 'auth_token', "value": twitter_token})
            driver.add_cookie({"name": 'auth_token', "value": twitter_token})
            driver.refresh()
            print("进入Twitter")
        else:
            driver.get('https://twitter.com/?lang=zh')
            driver.add_cookie({"name": 'auth_token', "value": twitter_token})
            driver.refresh()
            print("进入Twitter")
    finally:
        with open('step.txt', 'w') as f:
            f.write('2.1')
    # 进入
    driver.get('https://galxe.com/twitterConnect')
    # driver.get('https://galxe.com/accountSetting?tab=Account')
    # # 设置
    # xpath = '//*[@id="app"]/div/main/div/div/div/div[2]/div[1]/span/div[2]'
    # element = find_element_by_xpath(driver, xpath)
    # element.click()
    # # 进入推特
    # xpath = '//*[@id="app"]/div/main/div/div/div/div[2]/div[3]/span/div/div[2]/div[1]/div'
    # element = find_element_by_xpath(driver, xpath)
    # element.click()
    # # 点击推特
    # xpath = '//*[@id="app"]/div[1]/main/div/div/div/div[2]/div/button'
    # element = find_element_by_xpath(driver, xpath)
    # element.click()
    # 获取gid
    gid = ''
    cookies = driver.get_cookies()
    for i in cookies:
        if i['name'] == 'galxe-id':
            gid = i['value']
    driver.get(f'https://twitter.com/intent/tweet?text=Verifying+my+Twitter+account+for+my+%23GalxeID+gid%3A{gid}+@Galxe%20%0A%0A&url=galxe.com/galxeid')
    try:
        xpath = '//*[@id="layers"]/div[3]/div/div/div[2]/div/div[2]/div/div/div/div/div/div[2]/div[4]'
        element = find_element_by_xpath(driver, xpath, 10)
        element.click()
    except Exception:
        pass
    # 点击post
    xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]/div'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[9]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    #                /html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[5]
    xpath = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[5]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    xpath = '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[1]'
    element = find_element_by_xpath(driver, xpath)
    element.click()
    # 输入链接
    driver.get('https://galxe.com/twitterConnect')
    # 复制链接
    xpath = '//*[@id="app"]/div/main/div/div/div/div[3]/div/div[3]/input'
    if platform == 'darwin':
        driver.find_element_by_xpath(xpath).send_keys(Keys.COMMAND, 'v')
    else:
        driver.find_element_by_xpath(xpath).send_keys(Keys.CONTROL, 'v')
    # 点击verify
    xpath = '//*[@id="app"]/div/main/div/div/div/div[3]/div/button'
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    try:
        time.sleep(5)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign.png")
        pyautogui.scroll(-500)
        time.sleep(1)
        im = ImageGrab.grab()
        im.save(r'page.png')
        search_returnPoint("sign_in.png")
        print("绑定Twitter成功")
    except Exception:
        pass
    finally:
        with open('step.txt', 'w') as f:
            f.write('2.2')


def connect_discord(driver, discord_token):
    global step_num
    try:
        if step_num < 3 or step_num > 4:
            driver.get('https://discord.com/login')
            script_str = '''
            function login(token) { setInterval(() => { document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"` }, 50); setTimeout(() => { location.reload(); }, 2500); }
            login('%s')
            ''' % discord_token
            driver.execute_script(script_str)
            driver.refresh()
            print("进入discord")
        else:
            script_str = '''
                        function login(token) { setInterval(() => { document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"` }, 50); setTimeout(() => { location.reload(); }, 2500); }
                        login('%s')
                        ''' % discord_token
            driver.execute_script(script_str)
            driver.refresh()
            print("进入discord")
    finally:
        with open('step.txt', 'w') as f:
            f.write('3.1')
    driver.get('https://galxe.com/accountSetting?tab=SocialLinlk')
    cookies = driver.get_cookies()
    account_id = ''
    for i in cookies:
        if i['name'] == 'account':
            account_id = i['value']
    try:
        driver.get(f'https://discord.com/oauth2/authorize?client_id=947863296789323776&redirect_uri=https://galxe.com&response_type=code&scope=identify%20guilds%20guilds.members.read&prompt=consent&state=Discord_Auth;{account_id}')
        xpath = '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/div/div[2]/button[2]'
        time.sleep(3)
        element = find_element_by_xpath(driver, xpath)
        element.click()
        # driver.get('https://galxe.com/accountSetting?tab=SocialLinlk')
        print("绑定discord成功")
    except Exception:
        pass


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
        xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[3]'
        element = find_element_by_xpath(driver, xpath, 5)
        element.click()
    except Exception:
        pass


# 开始了
if __name__ == "__main__":
    group_id_ = search_group()
    twitter_f = open('twitter.txt', 'r')
    discord_f = open('discord.txt', 'r')
    google_f = open('email.txt', 'r')
    twitter_tokens = twitter_f.readlines()
    discord_tokens = discord_f.readlines()
    google = google_f.readlines()
    for i in range(min(len(twitter_tokens), len(discord_tokens))):
        with open('step.txt', 'r') as f:
            ll = f.read()
            step_num = float(ll)
        with open('selenium.txt', 'r') as file:
            res = file.read()
            if res == "":
                id, serial_id = create_browser(group_id_)
                host, chrome_driver = open_ads_browser(id, serial_id)
            else:
                host = res.split('&')[0]
                chrome_driver = res.split('&')[1]
        browser = connect_browser(host, chrome_driver)
        if step_num <= 1:
            create_wallet(browser)
            connect_wallet(browser)
        twitter_token_ = twitter_tokens[i].split('----')[-1]
        discord_token_ = discord_tokens[i].split(":")[-1]
        if step_num < 3:
            connect_twitter(browser, twitter_token_.replace('\n', ''))
        if step_num < 4:
            connect_discord(browser, discord_token_.replace('\n', ''))
        with open('selenium.txt', 'w') as file:
            file.write('')
        with open('step.txt', 'w') as f:
            f.write('0')
        email_ = google[i].split('----')[0]
        pwd_ = google[i].split('----')[1]
        f_email_ = google[i].split('----')[2]
        google_login(browser, email_, pwd_, f_email_)
        browser.close()
    if len(twitter_tokens) > len(discord_tokens):
        print("discord token不足")
    elif len(twitter_tokens) < len(discord_tokens):
        print("twitter token不足")
    twitter_f.close()
    discord_f.close()


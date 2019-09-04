from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
SLEEP_TIME = 3
HEADERS = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"
}

def request_by_selenium_chrome(url,headless=False):
    """
    使用selenium的chrome访问页面
    :param url:
    :param headless:
    :return: HTML
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_page_load_timeout(10)
    browser.get(url)
    html =  browser.page_source
    time.sleep(SLEEP_TIME)
    browser.close()
    return html

def request_by_requests(url,**kwargs):
    """
    使用request库请求
    :param url:
    :param proxies:
    :return: html
    """
    if "proxies" in kwargs:
        proxies = kwargs["proxies"]
    else:
        proxies = None
    try:
        time.sleep(SLEEP_TIME)
        html = requests.get(url,headers = HEADERS,timeout = 5,proxies=proxies)
        if html.status_code == 200:
            return html.text
        else:
            raise Exception
    except Exception:
        raise Exception
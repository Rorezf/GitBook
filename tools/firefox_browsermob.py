#coding: utf-8

import json, os, base64
from time import sleep
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FIREFOX_PATH = FirefoxBinary(BASE_PATH + '/firefox/firefox')
DRIVER_PATH = BASE_PATH + '/geckodriver'
BMP_PATH = BASE_PATH + '/browsermob/bin/browsermob-proxy'

server = Server(BMP_PATH)
server.start()
proxy = server.create_proxy()
profile = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
profile.accept_untrusted_certs = True

firefox_options = Options()
firefox_options.add_argument('-headless')

driver = webdriver.Firefox(executable_path=DRIVER_PATH, firefox_binary=FIREFOX_PATH, firefox_profile=profile, firefox_options=firefox_options)
driver.set_page_load_timeout(15)
driver.implicitly_wait(10)
driver.get('https://www.baidu.com')
sleep(1)
driver.execute_script('window.open()')
handles = driver.window_handles
driver.switch_to_window(handles[-1])
# driver.execute_script('window.resizeTo(1920,1080);')
proxy.new_har('test')
driver.get('https://www.baidu.com')
sleep(10)
with open('result.har', 'w') as result:
    json.dump(proxy.har, result)
server.stop()
driver.quit()
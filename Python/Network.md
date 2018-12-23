# Network

---

## ssl

```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

---

## Requests

```
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

response = requests.get(env_url, cookies=self.cookies)
response = requests.post(self.url, headers = self.headers, cookies = self.cookies, data = self.data, verify = self.verify)
env_content = response.json()

def getParams():
    with open('temp.txt', 'r') as f:
        content = f.read()
    url = re.compile(r'curl \"(.*?)\"').findall(content)[0].replace('^', '')
    headers = {}
    cookies = {}
    data = []

    headers_key = re.compile(r'-H \"(.*?):').findall(content)
    headers_value = re.compile(r'-H \".*?: (.*?)\" ').findall(content)
    for i in range(len(headers_key)):
        if headers_key[i] != 'Cookie':
            headers[headers_key[i]] = headers_value[i].replace('^', '').replace('\\', '')
        else:
            cookie_temp = headers_value[i].replace('^', '').replace('\\', '').split('; ')
            for c in range(len(cookie_temp)):
                cookie_content = cookie_temp[c].replace('\"', '').split('=')
                cookies[cookie_content[0]] = cookie_content[1]

    data_temp = re.compile(r'--data \"(.*?)\" ').findall(content)
    if data_temp:
        data_temp = data_temp[0].replace('^', '').split('&')
        for i in range(len(data_temp)):
            data_value = data_temp[i].split('=')
            if not '%' in data_value[1]:
                data.append((data_value[0], data_value[1]))
            else:
                data_value[1] = unquote(data_value[1])
                data.append((data_value[0], data_value[1]))
    if re.compile(r'--insecure').findall(content):
        verify = False
    else:
        verify = True
    return url, headers, cookies, data, verify
```

---

## BeautifulSoup

```
from bs4 import BeautifulSoup
content = self.browser.response().read()
soup = BeautifulSoup(content, "lxml")
bidList = soup.select(".bz_id_column a")
bidList = [int(eachBid.string) for eachBid in bidList]

resolutionList = soup.select(".bz_resolution_column span")
resolutionList = [eachRsl.attrs['title'] for eachRsl in resolutionList]
```

---

## Spider

### Mechanize

```
import mechanize
self.browser = mechanize.Browser()
cookie = cookielib.LWPCookieJar()
self.browser.set_cookiejar(cookie)
self.browser.set_handle_equiv(True) 
self.browser.set_handle_gzip(False) 
self.browser.set_handle_redirect(True) 
self.browser.set_handle_referer(True)
self.browser.set_handle_robots(False)
self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
self.browser.addheaders = [('User-agent',"Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")]
self.browser.add_password(BUGZILLA, base64.b64decode(AUTHORIZATION), 
	base64.b64decode(AUTHORIZATION))

self.browser.open(BUGZILLA)
self.browser.select_form(nr=1)
self.browser.form['Bugzilla_login'] = base64.b64decode(SPIDER_USR)
self.browser.form['Bugzilla_password'] = base64.b64decode(SPIDER_PWD)
self.browser.submit()
```

### Selenium

#### Phantomjs

```
from selenium import webdriver
PJS_PATH = '/usr/local/share/syncDb/driver/phantomjs/bin/phantomjs'
PJS_ARGS = ['--ignore-ssl-errors=true', '--load-images=false']
SERVICE_ARGS = ['--ignore-ssl-errors=true', '--load-images=yes', '--disk-cache=no', '--webdriver-loglevel=none']

self.driver = webdriver.PhantomJS(executable_path=PJS_PATH, service_args=PJS_ARGS)
self.driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
self.driver.implicitly_wait(10)
self.driver.set_page_load_timeout(10)
self.driver.set_script_timeout(10)
self.driver.quit()

def getLoginCookie(self):
	self.driver.get(JENKINS)
	loginInput = """
		jQuery('#j_username').val('{}');
		jQuery('input[name="j_password"]').val('{}');
	""".format(base64.b64decode(SPIDER_USR), base64.b64decode(SPIDER_PWD))
	self.driver.execute_script(loginInput)
	loginClick = "jQuery('#yui-gen1-button').trigger('click');"
	self.driver.execute_script(loginClick)

	time.sleep(0.5)
	cookies = self.driver.get_cookies()
	self.tearDown()

	targetCookie = {str(eachCookie['name']): str(eachCookie['value'])
	for eachCookie in cookies if "JSESSIONID" in eachCookie['name']}
	return targetCookie

browser_log = filter(lambda x: str(pageid) in x, self.driver.get_log('browser'))

self.driver.delete_all_cookies()
for c in range(len(self.COOKIE_NAME)):
    self.driver.add_cookie({
        'domain': DOMAIN,
        'name': self.COOKIE_NAME[c],
        'value': self.COOKIE_VALUE[c],
        'path': '/',
        'expires': None
        })
self.driver.refresh()
```

#### PhantomJs/JavaScript

```
// var page = this;
page.onLoadStarted = function(){
    page.navigationStart = new Date().getTime();
};
page.onResourceRequested = function (req) { 
    page.browserLog.push({'%s': {'requestID': req.id, 'startUrl': req.url, 'startTime': req.time.toISOString()}});
};
page.onResourceReceived = function (res) {
    if (res.stage === 'end' && res.statusText == 'OK') {
        page.browserLog.push({'%s': {'responseID': res.id, 'endUrl': res.url, 'status': res.status, 'endTime': res.time.toISOString()}});
    }
    else if (res.stage === 'start' && res.statusText == 'OK') {
        page.browserLog.push({'%s': {'responseID': res.id, 'bodySize': res.bodySize}});
    }
};
page.onLoadFinished = function(){
    var onloadTime = new Date().getTime() - page.navigationStart;
    page.browserLog.push({'%s': {'onload': onloadTime}});
    page.browserLog.push({'%s': {'navTime': page.navigationStart}});
};
```

#### Firefox & Browsermob

```
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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
```

---

## Graylog

```
class ContextFilter(logging.Filter):
    def __init__(self, req_env):
        self.req_env = req_env

    def filter(self, record):
        record.req_env = self.req_env
        return True


class graylogService():
    def __init__(self, environment):
        logging.basicConfig(level=logging.INFO)
        self.gelfLogger = logging.getLogger(self.__class__.__name__)
        if environment == 'testing':
            handler = GelfTcpHandler(host=HOST, port=PORT, debug=True, 
                include_extra_fields=True, _service='udata-web-monitor', env='development')
        self.gelfLogger.addHandler(handler)

    def recordLog(self):

        if type == 'screen':
            msg = "[graylog][%s][pageid: %s][jspName: %s][onloadTime: %sms][screenTime: %sms][status: %s]" %(req_game, req_page_id, req_page_name, req_page_onload_timing, req_page_screen_timing, req_page_status)
        elif type == 'resource':
            msg = "[graylog][%s][pageid: %s][jspName: %s][%s: %sms][bodySize: %s]" %(req_game, req_page_id, req_page_name, req_page_resource, req_page_resource_timing, req_page_resource_bodySize)
        elif type == 'msg':
            msg = "[graylog][%s][%s]" %(req_game, msg)
        else:
            msg = '[graylog][no msg]'

        msgFilter = ContextFilter(req_id = req_id, req_game = req_game, req_page_id = req_page_id,
        req_page_name = req_page_name, req_page_module = req_page_module, req_page_resource = req_page_resource,
        req_page_resource_timing = req_page_resource_timing, req_page_resource_type = req_page_resource_type, 
        req_page_screen_timing = req_page_screen_timing, req_page_onload_timing = req_page_onload_timing, 
        req_page_status = req_page_status, req_page_resource_bodySize = req_page_resource_bodySize, req_env = req_env)

        self.gelfLogger.addFilter(msgFilter)
        self.gelfLogger.info(msg)
        self.gelfLogger.removeFilter(msgFilter)
```
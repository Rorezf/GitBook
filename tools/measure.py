#coding: utf-8
import requests, re, threading, Queue, csv, sys
from time import time, sleep
from urllib import unquote
dataCollect = Queue.Queue()

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

class measureGo(threading.Thread):
    def __init__(self, url, headers, cookies, data, verify):
        threading.Thread.__init__(self)
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.verify = verify

    def run(self):
        global dataCollect
        try:
            if self.data:
                start = time()
                response = requests.post(self.url, headers = self.headers, cookies = self.cookies, data = self.data, verify = self.verify)
                duration = round(time() - start, 3) * 1000
            else:
                start = time()
                response = requests.get(self.url, headers = self.headers, cookies = self.cookies, verify = self.verify)
                duration = round(time() - start, 3) * 1000
            temp = [self.url, response.status_code, len(response.content), duration]
            dataCollect.put(temp)
        except:
            raise IOError('Something were wrong with cURL.')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Please input entire params: [Threads Number] [Interval Time] [Loop Count]'
    else:
        thread_num = int(sys.argv[1])
        delay_time = float(sys.argv[2])
        loop_num = int(sys.argv[3])

        csvFile = open('result.csv', 'wb')
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(['url', 'status', 'RawBodySize', 'duration(ms)'])
        url, headers, cookies, data, verify = getParams()

        for i in range(loop_num):
            threads = []
            for i in range(thread_num):
                th = measureGo(url, headers, cookies, data, verify)
                th.start()
                threads.append(th)
                sleep(delay_time)
            for th in threads:
                th.join()
        while not dataCollect.empty():
            temp = dataCollect.get()
            csvWriter.writerow([temp[0], temp[1], temp[2], temp[3]])
        csvFile.close()
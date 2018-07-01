#coding: utf-8
import requests, re, yaml, json, time, datetime
from urllib import unquote
from dateutil.relativedelta import relativedelta

today = datetime.date.today()
yesterDay = (today - datetime.timedelta(days = 1)).strftime('%Y%m%d')
beforeDay = (today - datetime.timedelta(days = 2)).strftime('%Y%m%d')
sevenDaysAgo = (today - datetime.timedelta(days = 7)).strftime('%Y%m%d')
sevenWeeksAgo = (today - datetime.timedelta(days = 49)).strftime('%Y%m%d')
this_month_first_day = datetime.date(day = 1, month = today.month, year = today.year)
last_month_last_day = (this_month_first_day - datetime.timedelta(days = 1)).strftime('%Y%m%d')
six_month_fist_day = (this_month_first_day - relativedelta(months = 6)).strftime('%Y%m%d')

def dayInterval(day_one, day_two):
    day_one_timeStamp = time.mktime(time.strptime(day_one, '%Y%m%d'))
    day_two_timeStamp = time.mktime(time.strptime(day_two, '%Y%m%d'))
    interval = int((day_one_timeStamp - day_two_timeStamp) / 86400.0)
    return interval

def getAppData():
    AppData = {}
    with open('app.txt', 'r') as f:
        content = f.read()
    content += '\n'
    urlList = re.compile(r"keydata_(\w.*?) HTTP").findall(content)
    dataList = re.compile(r'{\".*?}\n').findall(content)

    for i in range(len(urlList)):           
        if "operation" in urlList[i]:          # 数组时间顺序
            temp = json.loads(dataList[i])['data']['login']['data']
            if abs(dayInterval(temp[0][0], temp[1][0])) == 1:
                AppData['operation_day_loginData'] = temp
                AppData['operation_day_payData'] = json.loads(dataList[i])['data']['prepaid']['data']
            elif abs(dayInterval(temp[0][0], temp[1][0])) == 7:
                AppData['operation_week_loginData'] = temp
                AppData['operation_week_payData'] = json.loads(dataList[i])['data']['prepaid']['data']
            elif abs(dayInterval(temp[0][0], temp[1][0])) >= 28:
                AppData['operation_month_loginData'] = temp
                AppData['operation_month_payData'] = json.loads(dataList[i])['data']['prepaid']['data']

        elif "cu" in urlList[i]:               # 数组时间顺序
            AppData['cu_data'] = json.loads(dataList[i])['data']

        elif "pay" in urlList[i]:              # 数组时间顺序
            temp = json.loads(dataList[i])['thead']
            if len(temp) == 2:
                AppData['pay_cash'] = json.loads(dataList[i])['data']
            elif u'\u4ed8\u8d39\u7387' in temp[1]:
                AppData['pay_rate'] = json.loads(dataList[i])['data']
            elif u'\u4ed8\u8d39' in temp[1]:
                AppData['pay_role'] = json.loads(dataList[i])['data']
            elif 'ARPU' in temp[1]:
                AppData['pay_arpu'] = json.loads(dataList[i])['data']
            elif 'VIP' in temp[2]:
                AppData['pay_vip'] = json.loads(dataList[i])['data']

        elif "ltv" in urlList[i]:              # 数组时间倒序
            if not AppData.has_key('ltv_account_data'):
                AppData['ltv_account_data'] = json.loads(dataList[i])['data']
            else:
                AppData['ltv_role_data'] = json.loads(dataList[i])['data']

        elif "retention" in urlList[i]:        # 数组时间顺序
            if not AppData.has_key('retention_account_data'):
                AppData['retention_account_data'] = json.loads(dataList[i])['data']
            elif not AppData.has_key('retention_role_data'):
                AppData['retention_role_data'] = json.loads(dataList[i])['data']
            else:
                AppData['retention_device_data'] = json.loads(dataList[i])['data']

        elif "channel" in urlList[i]:          # 字典,时间为键,值为列表
            temp = json.loads(dataList[i])['thead']
            if u'\u767b\u5f55' in temp[1]:
                AppData['channel_login_data'] = json.loads(dataList[i])['data']
            elif u'\u4ed8\u8d39\u7387' in temp[1]:
                AppData['channel_pay_data'] = json.loads(dataList[i])['data']
            elif 'ARPU' in temp[1]:
                AppData['channel_arpu_data'] = json.loads(dataList[i])['data']
            elif u'\u6b21\u65e5' in temp[1]:
                AppData['channel_retention_data'] = json.loads(dataList[i])['data']

        elif "player" in urlList[i]:           # 字典,时间为键,值为列表
            temp = json.loads(dataList[i])['thead']
            if u'\u7b49\u7ea7' in temp[0]:
                AppData['player_level_data'] = json.loads(dataList[i])['data']
            elif u'\u670d\u52a1\u5668' in temp[0]:
                AppData['player_server_data'] = json.loads(dataList[i])['data']
            elif u'\u7701\u4efd' in temp[0]:
                AppData['player_map_data'] = json.loads(dataList[i])['data']
    return AppData

def getResponse(index, type = None):
    headers = {}
    cookies = {}
    data = []
    with open('api.yaml', 'r') as f:
        content = yaml.load(f)
    content = content[index]['cURL']
    url = re.compile(r'curl \"(.*?)\"').findall(content)[0].replace('^', '')
    if index == 2:
        if type:
            url = url.replace('login', type)
            if type == 'rete':
                url = url.replace(yesterDay, beforeDay)

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
        data_temp = data_temp[0]
        if index == 0:
            if type == 'week':
                data_temp = data_temp.replace('type=day', 'type=week').replace(sevenDaysAgo, sevenWeeksAgo)
            elif type == 'month':
                data_temp = data_temp.replace('type=day', 'type=month').replace(sevenDaysAgo, six_month_fist_day).replace(yesterDay, last_month_last_day)
        elif index == 1:
            if type:
                data_temp = data_temp.replace('account', type)
        elif index == 3:
            if 'level' in type:
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=6').replace('^&mapType=china', '')
            elif 'server' in type:
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=8').replace('^&mapType=china', '')
        elif index == 4:
            if 'role' in type:
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=8')
            elif 'rate' in type:
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=9').replace('os=-127', 'os=-127^&idx=account')
            elif 'arpu' in type:
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=10').replace('os=-127', 'os=-127^&idx=account')
            elif 'vip' in type:
                start_temp = re.compile(r'startDate=(.*?)\^&').findall(data_temp)[0]
                data_temp = data_temp.replace('dataDesc=7', 'dataDesc=11').replace(start_temp, yesterDay)

        data_temp = data_temp.replace('^', '').split('&')
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

    try:
        if data:
            response = requests.post(url, headers = headers, cookies = cookies, data = data, verify = verify)
        else:
            response = requests.get(url, headers = headers, cookies = cookies, verify = verify)
        return response.json()
    except:
        raise IOError('Something were wrong with cURL config.')
#coding: utf-8
import csv, ssl, urllib, urllib2, os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
ssl._create_default_https_context = ssl._create_unverified_context
rcParams['grid.linewidth'] = 0.5

def calculate(flag):
    if not flag:
        return False
    basic_general = {'onload': {}, 'screen': {}, 'timeOut': 0, 'total': 0}
    custom_general = {'onload': {}, 'screen': {}, 'timeOut': 0, 'total': 0}
    general = {'JspForMobileGameOp': basic_general, 'JspForMobileGame': custom_general}
    failedPages = {'JspForMobileGameOp': [], 'JspForMobileGame': [] }
    resource = {}
    csvFile = open('temp.csv', 'r')
    csvReader = csv.DictReader(csvFile)

    for row in csvReader:
        if row['req_page_resource_type']:
            if not resource.has_key(row['req_page_name']):
                resource[row['req_page_name']] = {
                    'css':   {'totalTime': 0, 'counter': 0, 'maxTime': 0}, 'js': {'totalTime': 0, 'counter': 0, 'maxTime': 0},
                    'img':   {'totalTime': 0, 'counter': 0, 'maxTime': 0}, 'xhr': {'totalTime': 0, 'counter': 0, 'maxTime': 0},
                    'font':  {'totalTime': 0, 'counter': 0, 'maxTime': 0}, 'doc': {'totalTime': 0, 'counter': 0, 'maxTime': 0},
                    'other': {'totalTime': 0, 'counter': 0, 'maxTime': 0}}
            resource[row['req_page_name']][row['req_page_resource_type']]['totalTime'] += int(row['req_page_resource_timing'])
            resource[row['req_page_name']][row['req_page_resource_type']]['counter'] += 1
            if resource[row['req_page_name']][row['req_page_resource_type']]['maxTime'] < int(row['req_page_resource_timing']):
                resource[row['req_page_name']][row['req_page_resource_type']]['maxTime'] = int(row['req_page_resource_timing'])
        elif row['req_page_screen_timing']:
            if row['req_page_module'] == 'JspForMobileGame':
                if not general[row['req_page_module']]['onload'].has_key(row['req_page_id']):
                    general[row['req_page_module']]['onload'][row['req_page_id']] = {'total': 0, 'counter': 0}
                    general[row['req_page_module']]['screen'][row['req_page_id']] = {'total': 0, 'counter': 0}    
                general[row['req_page_module']]['onload'][row['req_page_id']]['total'] += int(row['req_page_onload_timing'])
                general[row['req_page_module']]['onload'][row['req_page_id']]['counter'] += 1
                general[row['req_page_module']]['screen'][row['req_page_id']]['total'] += int(row['req_page_screen_timing'])
                general[row['req_page_module']]['screen'][row['req_page_id']]['counter'] += 1
            else:
                if not general[row['req_page_module']]['onload'].has_key(row['req_page_name']):
                    general[row['req_page_module']]['onload'][row['req_page_name']] = {'total': 0, 'counter': 0}
                    general[row['req_page_module']]['screen'][row['req_page_name']] = {'total': 0, 'counter': 0}   
                general[row['req_page_module']]['onload'][row['req_page_name']]['total'] += int(row['req_page_onload_timing'])
                general[row['req_page_module']]['onload'][row['req_page_name']]['counter'] += 1
                general[row['req_page_module']]['screen'][row['req_page_name']]['total'] += int(row['req_page_screen_timing'])
                general[row['req_page_module']]['screen'][row['req_page_name']]['counter'] += 1
        else:
            if row['req_page_module'] == 'JspForMobileGame':
                if not row['req_page_id'] in failedPages[row['req_page_module']]:
                    failedPages[row['req_page_module']].append(row['req_page_id'])
            else:
                if not row['req_page_name'] in failedPages[row['req_page_module']]:
                    failedPages[row['req_page_module']].append(row['req_page_name'])
                    
    for module in general:
        failedPagesCounter = 0
        for page in failedPages[module]:
            if not page in general[module]['onload']:
                failedPagesCounter += 1
        general[module]['timeOut'] = failedPagesCounter
        general[module]['total'] = len(general[module]['onload']) + failedPagesCounter
        for page in general[module]['onload']:
            general[module]['onload'][page]['averTime'] = round(float(general[module]['onload'][page]['total']) / float(general[module]['onload'][page]['counter']), 1)
            general[module]['screen'][page]['averTime'] = round(float(general[module]['screen'][page]['total']) / float(general[module]['screen'][page]['counter']), 1)
    
    for jspName in resource:
        for resourceType in resource[jspName]:
            if resource[jspName][resourceType]['counter']:
                resource[jspName][resourceType]['averTime'] = round(float(resource[jspName][resourceType]['totalTime']) / float(resource[jspName][resourceType]['counter']), 1)
            else:
                resource[jspName][resourceType]['averTime'] = 0
    csvFile.close()

    return general, resource

# 资源均值/峰值堆积图
def draw_resource_stack(resource):
    jspNameList = []
    resourceAver = []
    resourceMax = []
    resourceTypeList = []
    for jspName in resource:
        averTemp = []
        maxTemp = []
        jspNameList.append(jspName)
        for resourceType in resource[jspName]:
            if not resourceType in resourceTypeList:
                resourceTypeList.append(resourceType)
            averTemp.append(resource[jspName][resourceType]['averTime'])
            maxTemp.append(resource[jspName][resourceType]['maxTime'])
        resourceAver.append(averTemp)
        resourceMax.append(maxTemp)
    pd_averTime = pd.DataFrame(resourceAver, index = jspNameList, columns = pd.Index(resourceTypeList, name = 'ResourceType'))
    pd_maxTime = pd.DataFrame(resourceMax, index = jspNameList, columns = pd.Index(resourceTypeList, name = 'ResourceType'))
    pd_averTime_pct = pd_averTime.div(pd_averTime.sum(1).astype(float), axis = 0)
    
    figure = plt.figure("Resource Proportition", figsize=(12, 9))
    ax = figure.add_subplot(111)
    pd_averTime_pct.plot(kind = 'bar', ax = ax, stacked = True)
    plt.title('Resource Proportition')
    plt.legend(bbox_to_anchor = (1.01, 1))
    plt.tick_params(top = False, right = False)
    plt.xticks(rotation = 30, fontsize = 8.5)
    figure.savefig(BASE_DIR + '/static/img/resource_proportition.png')

    figure = plt.figure("Resource", figsize=(12, 9))
    ax = figure.add_subplot(111)
    pd_maxTime.plot(kind = 'bar', ax = ax, color = ['c', 'orange', 'deepskyblue', 'limegreen', 'fuchsia', 'gold', 'tomato'])
    pd_averTime.plot(kind = 'bar', ax = ax, color = ['aqua', 'wheat', 'skyblue', 'lime', 'violet', 'lemonchiffon', 'lightsalmon'])
    plt.title('Resource')
    plt.tick_params(top = False, right = False)
    plt.grid(True)
    plt.xticks(rotation = 30, fontsize = 8.5)
    plt.legend(['img/max', 'doc/max', 'js/max', 'xhr/max', 'other/max', 'font/max', 'css/max', 'img/aver', 'doc/aver', 'js/aver', 'xhr/aver', 'other/aver', 'font/aver', 'css/aver'])
    figure.savefig(BASE_DIR + '/static/img/resource_max_aver.png')

# onload和screen时间直方图和箱形图
def draw_general(general):
    general_basic = []
    general_jspName = []
    for jspName in general['JspForMobileGameOp']['onload']:
        general_jspName.append(jspName)
        general_basic.append([general['JspForMobileGameOp']['onload'][jspName]['averTime'], general['JspForMobileGameOp']['screen'][jspName]['averTime']])
    pd_general_basic = pd.DataFrame(general_basic, index = general_jspName, columns = pd.Index(['onloadTime', 'screenTime'], name = 'GeneralTime'))
    
    general_custom = []
    for pageid in general['JspForMobileGame']['onload']:
        general_custom.append([general['JspForMobileGame']['onload'][pageid]['averTime'], general['JspForMobileGame']['screen'][pageid]['averTime']])
    pd_general_custom = pd.DataFrame(general_custom, index = range(1, len(general['JspForMobileGame']['onload']) + 1), columns = pd.Index(['onloadTime', 'screenTime'], name = 'GeneralTime'))

    figure = plt.figure('Box', figsize=(12, 9))
    ax1 = figure.add_subplot(121)
    ax2 = figure.add_subplot(122)

    pd_general_basic.plot(kind = 'box', ax = ax1, grid = True)
    plt.sca(ax1)
    plt.title('Basic Analysis Box')

    pd_general_custom.plot(kind = 'box', ax = ax2, grid = True)
    plt.sca(ax2)
    plt.title('Custom Indicators Box')
    # figure.savefig(BASE_DIR + 'general_box.png')

    figure = plt.figure('Basic Analysis Bar', figsize=(12, 9))
    ax = figure.add_subplot(111)
    pd_general_basic.plot(kind = 'bar', ax = ax, grid = True)
    plt.title('Basic Analysis Bar')
    plt.xticks(rotation = 30, fontsize = 8.5)
    # figure.savefig(BASE_DIR + '/static/img/general_basic_bar.png')
    plt.show()

# 基础分析和定制指标页面的正常页面数和超时页面数饼状图
def draw_timeout_pie(general):
    for module in general:
        pie_figure = plt.figure(module + ' pie', figsize = (12, 9))
        if general[module]['timeOut'] == 0:
            sizes = [general[module]['total']]
            plt.pie(sizes, labels = ['normal'], colors = ['yellowgreen'], autopct = '%1.1f%%')
        else:
            sizes = [general[module]['total'] - general[module]['timeOut'], general[module]['timeOut']]
            plt.pie(sizes, explode = (0.05, 0), labels = ['normal', 'timeOut'], colors = ['yellowgreen', 'lightcoral'], autopct = '%1.1f%%', startangle = 45)
        plt.axis('equal')
        if module == 'JspForMobileGameOp':
            plt.title('Basic Analysis')
        elif module == 'JspForMobileGame':
            plt.title('Custom Indicators')
        imgName = BASE_DIR + '/static/img/' + module + '_pie.png'
        pie_figure.savefig(imgName)

def dealData(start, end, game):
    flag = getData(start, end, game)
    return calculate(flag)

if __name__ == '__main__':
    general, resource = calculate(True)
    draw_general(general)
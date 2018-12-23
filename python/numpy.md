# Numpy

## Matplot

```text
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
```

### 均值/峰值堆积图

```text
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
```

### 直方图和箱形图

```text
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
```

### 饼状图

```text
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
```


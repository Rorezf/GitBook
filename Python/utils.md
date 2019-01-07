# Utils

## Time

```python
import time, datetime

def str2datetime(strtime):
    return datetime.datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S.%f')

def datetime2str(dateobj):
    return dateobj.strftime('%Y-%m-%d %H:%M:%S.%f')

def datetime2timestamp(dateobj):    #13位不带小数点，毫秒级别 time.time()为13位带小数点秒级别
    return long(time.mktime(dateobj.timetuple()) * 1000.0 + dateobj.microsecond / 1000.0)

def str2timestamp(strtime):
    return datetime2timestamp(str2datetime(strtime))

def timestamp2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000.0)

def timestamp2str(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')

today = datetime.datetime.now()
todayStr = today.strftime("%Y-%m-%d")
endDate = today + datetime.timedelta(1)
endDate = endDate.strftime("%Y-%m-%d")
```


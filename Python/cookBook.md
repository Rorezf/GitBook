# Cook Book

## 数据结构

1. 序列分解：
```python
data = [1,2,3,4,5,6]
_, *midElem, _ = data
```

2. 保存最后N个元素：
```python
from collections import deque
que = deque(maxlen=2)
que.append(1)
que.appendleft(2)	# 队列已满时会弹出开始时的记录
que.pop()	# 弹出最后的记录

# 添加/弹出元素的复杂度都是O(1)，列表操作则为O(N)
```

3. 最大/小元素
```python
# 单纯找到一个最大/小元素
max()/min()

# 寻找的元素量较小时
heapq.nlargest()/nsmallest()
```

4. 一键多值字典
```python
from collections import defaultdict, OrderedDict
d = defaultdict(list)
d['a'].append(1)	# if not a in d: d['a'] = []
d['a'].append(2)	# d = {'a', [1,2]}

d = defaultdict(set)
d['a'].append(1)
d['a'].append(2)

# OrderedDict内部维护了一个双向链表，大小是普通自带字典的两倍多
d = OrderedDict()
d['a'] = 1
d['b'] = 2
```

4.5  移除重复项并保持原有顺序
```python
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
```

5. 对切片命名
```python
SHARES = slice(1,5)
PRICE = slice(9,12)
s = data[SHARES]
```

6. 元素出现的次数
```python
from collections import Counter
x = ['a', 'b', 'a']
wordCounter = Counter(x)
topThree = wordCounter.most_common(3)
aNum = wordCounter['a']

y = ['b', 'c']
wordCounter.update(y)
```

7. 字典排序
```python
from operator import itemgetter, attrgetter
data = [
	{'name': 'a', 'id': 2},
	{'name': 'b', 'id': 1}
]
sortByName = sorted(data, key=itemgetter('name'))
sortByName = sorted(data, key=lambda x: x['name'])
# 性能上itemgetter更优，同样适用于min/max
# attrgetter与itemgetter类似，用于属性方面
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def __repr__(self):
        retrun 'User ID: {}'.format(self.user_id)

users = [User(11), User(5), User(3), User(4)]
sortByUserID = sorted(users, key=attrgetter('user_id'))
```

8. 分组记录
```python
from operator import itemgetter
from itertools import groupby	#groupby生成迭代器
data = [
	{'name': 'a', 'id': 2},
	{'name': 'b', 'id': 1},
	{'name': 'a', 'id': 3}
]
data.sort(key=itemgetter("name"))
for name, items in groupby(data, key=itemgetter('name')):
	print(name)
	for item in items:
		print(item)
#	a
#		{'name': 'a', 'id': 2}
#		{'name': 'a', 'id': 3}
#	b
#		{'name': 'b', 'id': 1}
```

8.5 筛选元素
```python
from itertools import compress
data = ['a', 'b', 'c', 'd', 'e', 'f']
filterValue = [1, -1, 0, 1, 0, 1]
filterResult = compress(data, [val > 0 for val in filterValue])
print(list(filterResult))
# ['a', 'd', 'f'] compress返回迭代器
```

9. 名称映射到序列的元素中
```python
from collections import namedtuple
x = namedtuple('x', ['name', 'id'])
y = x('a', 1)
# y.name = 'a', y.id = 1
# 不可直接重新赋值，若需改变，则 y._replace(name='b')

    Stock = namedtuple('Stock', ['name', 'shares', 'prices'])
    def computeCost(records):
        total = 0.0
        for rec in records:
            s = Stock(*rec)
            total += s.shares * s.prices
        return total

    data = [
        ['a', 1, 5],
        ['b', 2, 5],
        ['c', 3, 5]
    ]
    totalCost = computeCost(data)
    print(totalCost) # 30.0
```

10. 多个映射合并为一
```python
from collections import ChainMap
a = {'x': 1, 'y': 2}
b = {'y': 3, 'z': 4}
c = ChainMap(a, b)
# c = {'x': 1, 'y': 2, 'z': 4} 相同键以前者为准
```

---

## 字符串和文本

1. 任意分隔符拆分字符串

   ```python
   import re
   line = 'asdf fjdk; afed, fjeks,asdf,   foo'
   print(re.split(r'[;,\s]\s*', line))
   # ['asdf', 'fjdk', 'afed', 'fjeks', 'asdf', 'foo']
   
   # 注意区别于捕获组模式
   print(re.split(r'(;|,|\s)\s*', line)) # 捕获组
   # ['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjeks', ',', 'asdf', ',', 'foo']
   print(re.split(r'(?:;|,|\s)\s*', line)) # 非捕获组
   ['asdf', 'fjdk', 'afed', 'fjeks', 'asdf', 'foo']
   ```

2. 首尾匹配文本

   ```python
   fileName = 'spam.txt'
   fileName.endswith('.txt') # True
   fileName.startswith('spam') # True
   
   # 多项匹配
   rules = ('.txt', '.py') # 注意这里是元组
   fileName.endswith(rules) # True
   ```

3. Shell通配符匹配

   ```python
   from fnmatch import fnmatch, fnmatchcase
   fnmatch('Data45.csv', 'Data[0-9]*') # True
   fnmatch('foo.txt', '*.TXT') # windows下为True Mac下为False
   fnmatchcase('foo.txt', '*.TXT') # 区分大小写 False
   
   ```
   
4. 复杂文本替换

   ```python
   import re
   text = 'Today is 01/10/2021. Tomorrow is 01/11/2021'
   replaceResult = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
   print(replaceResult) # Today is 2021-01-10. Tomorrow is 2021-01-11
   
   # 更加复杂的情况
   def formatDate(m):
           monthName = month_abbr[int(m.group(1))]
           return '{} {} {}'.format(m.group(2), monthName, m.group(3))

   replaceResult = re.sub(r'(\d+)/(\d+)/(\d+)', formatDate, text)
   print(replaceResult) # Today is 10 Jan 2021. Tomorrow is 11 Jan 2021

   # subn 查看替换次数
   replaceResult, n = re.subn(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
   print(replaceResult, n) # Today is 2021-01-10. Tomorrow is 2021-01-11 2

   # 涉及大小写的复杂情况
   text = 'UPPER PYTHON lower python, Mixed Python'
   a = re.sub('python', 'snake', text, re.I)
   print(a) # UPPER PYTHON lower snake, Mixed Python

   # 旧版本Python可能不会自适应大小写情况，需要用到支撑函数
   def matchCase(word):
           def replace(m):
               text = m.group()
               if text.isupper():
                   return word.upper()
               elif text.islower():
                   return word.lower()
               elif text[0].isupper():
                   return word.capitalize()
               else: return word
           return replace
       
   replaceResult = re.sub('python', matchCase('snake'), text, re.I)
   print(replaceResult) # UPPER PYTHON lower snake, Mixed Python

   ```
5. 非贪婪模式匹配

   ```python
   text = 'Please say "NO". "YES"'
   print(re.findall(r'\"(.*)\"', text)) # ['NO". "YES'] 一个元素
   print(re.findall(r'\"(.*?)\"', text)) # ['NO', 'YES'] 两个元素
   ```

6. 匹配多行模式

   ```python
   text = """
      /* this is a 
          comment */
   """
   print(re.findall(r'/\*(.*?)\*/'), text) # []
   # 句点(.)匹配任意字符，但默认情况下不能匹配换回符，可加上DOTALL标记来适配所有字符
   print(re.findall(r'/\*(?:.*?)\*/', text, re.DOTALL)) # ['/* this is a \n        comment */']
   ```

7. 将Unicode文本统一为规范形式

   ```python
   import unicodedata
   
   s1 = 'Spicy Jalape\u00f1o' # 'Spicy Jalapeño'
   s2 = 'Spicy Jalapen\u0303o' # 'Spicy Jalapeño'
   s1 == s2 # False
   
   t1 = unicodedata.normalize('NFC', s1)
   t2 = unicodedata.normalize('NFC', s2)
   print(t1 == t2) # True NFC表示字符是全组成的，尽可能使用单个代码点
   
   t3 = unicodedata.normalize('NFD', s1)
   t4 = unicodedata.normalize('NFD', s2)
   print(t3 == t4) # True NFD表示使用组合字符，每个字符能完全解开
   
   # 去掉音符标记
   t = unicodedata.normalize('NFD', s1)
   ''.join(c for c in t if not unicodedata.combining(c)) # Spicy Jalapeno
   ```

8. 文本过滤和清理

   ```python
   # 去掉两侧多余空格
   with open(fileName, 'r') as f:
       lines = (line.strip() for line in f)
       for line in lines:
           pass
   
   # 清理特定字符
   # 实际上对于简单的替换，用replace比translate更高效
   s = 'pytho\u00f1\fis\tawesome\r\n' 
   # pythoñis      awesome
   #       is      awesome
   remap = {
           ord('\t'): ' ',
           ord('\f'): ' ',
           ord('\r'): None
       }
   a = s.translate(remap) # pythoñ is awesome
   # 把所有的Unicode组合字符去掉
   combiningChars = dict.fromkeys(
           c for c in range(sys.maxunicode)
               if unicodedata.combining(chr(c))
       ) # dict.fromkeys 构建一个将每个Unicode组合字符都映射为None的字典
   tmp = unicodedata.normalize('NFD', a)
   b = tmp.translate(combiningChars) # python is awesome
   
   # 将所有的Unicode十进制数字字符映射为对应的ASCII版本
   digitmap = {
           c: ord('0') + unicodedata.digit(chr(c))
               for c in range(sys.maxunicode)
                   if unicodedata.category(chr(c)) == 'Nd'
       }
   x = '\u0661\u0662\u0663'
   print(x.translate(digitmap)) # 123
   
   # 利用编码方式清理文本
   # 当输出目标是ASCII形式文本时可用下面的例子
   s = 'pytho\u00f1 is awesome\n'
   a = unicodedata.normalize('NFD', s)
   b = a.encode('ascii', 'ignore').decode('ascii') # python is awesome
   ```

9. 给字符串中的变量名做插值处理

   ```python
       s = '{name} has {n} messages.'
       print(s.format(name='Guido', n=18)) # Guido has 18 messages.
   
       name = 'AK'
       n = 29
       print(s.format_map(vars())) # AK has 29 messages.
   
       class Info:
   
           def __init__(self, name, n):
               self.name = name
               self.n = n
               
       a = Info('YAHA', 22)
       print(s.format_map(vars(a))) # YAHA has 22 messages.
   
       # 处理某个值缺失的问题
       class safeSub(dict):
           
           def __missing__(self, key):
               return '{' + key + '}'
       
       class Info2:
   
           def __init__(self, name):
               self.name = name
       
       b = Info2('LINK')
       print(s.format_map(safeSub(vars(b)))) # LINK has {n} messages.
   ```

10. 在字节串上进行文本操作

    ```python
    data = b'Hello World'
    print(data[0:5]) # b'Hello'
    print(data.startswith(b'He')) # True
    print(data.split(b' ')) # [b'Hello', b'World']
    print(data.replace(b'World', b'Python')) # b'Hello Python'
    print(data.decode('ascii')) # Hello World
    ```

---

## 数字、日期和时间

1. 对数值四舍五入

   ```python
   round(1.23, 1) # 1.2
   round(1.27, 1) # 1.3
   round(12345, -1) # 12340
   round(12345, -2) # 12300
   ```

2. 精确的小数计算

   ```python
   from decimal import Decimal
   
   a = 4.2
   b = 2.1
   print(a+b) # 6.300000000000001
   
   a = Decimal('4.2')
   b = Decimal('2.1')
   print(a+b) # 6.3
   ```

3. 不同进制数

   ```python
   x = 1234
   print(bin(x)) # 0b10011010010
   print(oct(x)) # 0o2322
   print(hex(x)) # 0x4d2
   # format 没有前缀
   print(format(x, 'b')) # 10011010010
   print(format(x, 'o')) # 2322
   print(format(x, 'x')) # 4d2
   
   # 字符串转为十进制数
   print(int('10011010010', 2)) # 1234
   print(int('2322', 8)) # 1234
   print(int('4d2', 16)) # 1234
   ```

4. 随机选择

   ```python
   import random
   
   values = [1, 2, 3, 4, 5, 6, 7]
   print(random.choice(values)) # 随机选择样本中的一个
   print(random.sample(values, 3)) # 随机列出N个元素组成的列表
   
   random.shuffle(values) # 随机排序
   print(values)
   
   print(random.randint(0,99)) # 在输入的范围内随机生成一个int类型数
   
   # 修改初始种子值
   random.seed(b'bytedata')
   random.seed(1234)
   
   random.uniform() # 计算均匀分布值
   random.gauss() # 计算正态分布值
   ```

5. 时间计算

   ```python
   # pip install python-dateutil
   from datetime import datetime, timedelta

   a = datetime.today()
   b = timedelta(days=2, hours=6)
   print(a+b) # 2021-01-13 17:15:26.851837
   
   # datetime 可正确处理平闰年
   a = datetime(2012, 3, 1)
   b = datetime(2012, 2, 27)
   print(a-b) # 3 days, 0:00:00
   
   a = datetime(2013, 3, 1)
   b = datetime(2013, 2, 27)
   print(a-b) # 2 days, 0:00:00
   
   # dateutil 可以填补 datetime 在月份处理上的空缺
   a = datetime(2013, 2, 27)
   b = a + relativedelta(months=+3)
   print(b) # 2013-05-27 00:00:00
   
   c = datetime(2013, 4, 13)
   d = relativedelta(c, a)
   print(d) # relativedelta(months=+1, days=+17)
   ```
   
6. 计算上周N的日期

   ```python
   from datetime import datetime, timedelta
   from dateutil.rrule import *
   from dateutil.relativedelta import relativedelta
   
   weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
               'Saturday', 'Sunday']
   
   def getPreviousDate(dayName, startDate=None):
       if startDate is None:
           startDate = datetime.today()
       
       dayIndex = startDate.weekday()
       targetIndex = weekDays.index(dayName)
       
       daysAgo = (7 + dayIndex - targetIndex) % 7
       if daysAgo == 0: daysAgo = 7
   
       targetDate = startDate - timedelta(days=daysAgo)
       return targetDate
   
   today = datetime.today()
   lastFri = getPreviousDate('Friday', today)
   print(lastFri)
   
   today = datetime.today()
   lastFri = today + relativedelta(weekday=FR(-1))
   print(lastFri)
   ```

7. 找出某月的日期范围

   ```python
   def getMonthRange(startDate=None):
       if startDate is None: startDate = date.today()
       monthFirstDate = startDate.replace(day=1)
   
       xx, daysInMonth = monthrange(monthFirstDate.year, monthFirstDate.month)
       endDate = monthFirstDate + timedelta(days=daysInMonth)
       return (monthFirstDate, endDate)
   
   firstDay, lastDay = getMonthRange()
   targetMonthRange = []
   while firstDay < lastDay:
       targetMonthRange.append(firstDay)
       firstDay += timedelta(days=1)
   print(targetMonthRange)
   ```

8. 字符串和日期互转

   ```python
   a = datetime.today()
   print(a.strftime('%A %B %d, %Y')) # Monday January 11, 2021
   
   b = datetime.strptime('2021-01-02', '%Y-%m-%d')
   print(b) # 2021-01-02 00:00:00
   
   # strptime的性能通常情况下欠佳，若确定日期格式，需要处理大量数据时，通过自编函数效率更高
   def parseYMD(dateTimeStr):
       year, month, day = dateTimeStr.split('-')
       return datetime(int(year), int(month), int(day))
   c = parseYMD('2021-01-02')
   print(c) # 2021-01-02 00:00:00
   ```

9. 时区问题

   ```python
   localNow = datetime.now()
   print(localNow) # 本地时间
   
   central = timezone('US/Central')
   theTime = central.localize(localNow)
   print(theTime) # 中心时区
   
   anotherTime = theTime.astimezone(timezone('Asia/Kolkata'))
   print(anotherTime) # 其它时区（此处为印度）
   
   utcTime = localNow.astimezone(utc)
   print(utcTime) # 避免搞乱，可以使用统一的UTC时间存储和处理，使用时再本地化
   ```

---

## 迭代器和生成器


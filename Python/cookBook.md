# Cook Book

## Data Structure

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

9. 名称映射到序列的元素中
```python
from collections import namedtuple
x = namedtuple('x', ['name', 'id'])
y = x('a', 1)
# y.name = 'a', y.id = 1
# 不可直接重新赋值，若需改变，则 y._replace(name='b')
```

10. 多个映射合并为一
```python
from collections import ChainMap
a = {'x': 1, 'y': 2}
b = {'y': 3, 'z': 4}
c = ChainMap(a, b)
# c = {'x': 1, 'y': 2, 'z': 4} 相同键以前者为准
```
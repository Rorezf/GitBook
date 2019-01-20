# Spider

## 数据清洗

### n-gram模型

```python
def ngrams(inputs, n):
	inputs = re.sub(r'\n+', ' ', inputs)
	inputs = re.sub(r' +', ' ', inputs)
	inputs = bytes(inputs, 'utf-8')
	inputs = inputs.decode('ascii', 'ignore')

	inputs = inputs.split(' ')
	outputs = []
	for i in range(len(inputs)-n+1):
		outputs.append(inputs[i:i+n])
	return outputs
```

### 相关函数

1. string.punctuation: python所有的标点符号
2. collections.OrderedDict: 对Dict进行排序

## 数据采集

### Requests

1. 登录状态：
```python
session = requests.Session()
session.post(...)
session.get(...)
```

2. HTTP基本接入认证：
```python
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('user', 'password')
requests.post(url='http://...', auth=HTTPBasicAuth)
```
# Spider

## 随机数

1. 目标： 均匀分布，难以预测
2. 随机数种子：
   * 完全相同的种子会产生同样的“随机”数序列
   * 增加随机性：不断变化的种子（如： 系统时间）
   * python的为随机数生成器使用梅森旋转算法，符合要求但耗费CPU资源


## 深网/暗网

1. 深网与浅网(surface web 搜索引擎可以抓取的网络)对立
2. 暗网(Darknet): 建立在已有的网络基础上，使用Tor(The Onion Router)客户端，带有运行在http之上的协议（提供了信息交换的安全隧道）


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

## 马尔科夫模型

## 自然语言分析： NLTK

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

3. 提交文件：
```python
f = open('/path/of/file', 'rb')
files = {'inputName': f}
r = requests.post('url', files=files)
f.close()
```

## 图像识别与文字处理

### OCR(光学文字识别)库

1. Pillow(PIL): 图片处理
2. Tesseract: 可以通过训练识别任何字体/Unicode字符
	* 使用方法： tesseract text.tif textoutput | cat textoutput.txt
	* 示例：
		```python
			from PIL import Image
			import subprocess

			def cleanFile(filePath, newFilePath):
				image = Image.open(filePath)
				# 对图片进行阈值过滤
				image = image.point(lambda x: 0 if x < 143 else 255)
				image.save(newFilePath)

				subprocess.call(["tesseract", newFilePath, "output"])

				outputFile = open("output.txt", 'r')
				print(outputFile.read())
				outputFile.close()
		```
3. 训练Tesseract
	* 准备训练样本，样本文件命名为验证码结果（如：XyMa.jpg）
	* 准确告诉Tesseract每个字符的内容，如：
		s 15 26 33 55 0 => 编号为0的左下角(15,26)到右上角(33,55)的内容是s
	* 可以使用Tesseract OCR Chopper工具进行标注，保存为.box文件，命名与图片对应

## 远程采集

1. 注意请求头的设置，使其看起来更像普通用户，或从电脑端与移动端之间切换
2. Tor代理：改变IP地址

```python
import socks, socket
from urllib.request import urlopen

socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
socket.socket = socks.socksocket
print(urlopen('url').read())
```
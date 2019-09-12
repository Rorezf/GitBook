# Django

## Setting

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_PORT = 25
EMAIL_HOST = 'smtp.qiye.163.com'
EMAIL_HOST_USER = 'sqagz_gitlab@casachina.com.cn'
EMAIL_HOST_PASSWORD = base64.b64decode('MTIzNDVBYQ==')

ADMINS = [
    ('luozhifeng', 'luozhifeng@casachina.com.cn'),
    ('shaoyunshi', 'shaoyunshi@casachina.com.cn')]
SERVER_EMAIL = 'sqagz_gitlab@casachina.com.cn'
DEFAULT_FROM_EMAIL = 'sqagz_gitlab@casachina.com.cn'

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'db': REDIS_SESSION_INDEX,
    'prefix': 'session',
    'socket_timeout': 3,
    'retry_on_timeout': False
}

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(REDIS_HOST, REDIS_PORT, REDIS_CACHE_INDEX),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

```

## MySQL

```python
class SQL:
	__pool = None

	def __init__(self, defaultDB="jenkins"):
		self._conn = SQL.__getConn(defaultDB)
		self._cur = self._conn.cursor()

	@staticmethod
	def __getConn(defaultDB):
		if SQL.__pool is None:
			__pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=40, 
				host='172.0.2.201', port=3306, user='admin', charset='utf8',
				passwd=base64.decodestring("Y2FzYQ=="), db=defaultDB)
		return __pool.connection()

	def linkSQL(self):
		return self._conn, self._cur
```

## Django-conn-pool

```python
pip install Django-conn-pool

SQLALCHEMY_QUEUEPOOL = {
    'pool_size': 10,
    'max_overflow': 10,
    'timeout': 5,
    'recycle': 119,
}

DATABASES = {
    'default': {
        'ENGINE': 'django_conn_pool.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'xxx',
        'USER': 'xxx',
        'PASSWORD': 'xxx',
        'PORT': 3306,
    },
    'other': {
        'ENGINE': 'django_conn_pool.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'xxx',
        'USER': 'xxx',
        'PASSWORD': 'xxx',
        'PORT': 3306,
    },
}
```

## Redis

```python
class RedisObj:
	__pool = None

	def __init__(self, dbIndex):
		self._redis = RedisObj.__getPool(dbIndex)

	@staticmethod
	def __getPool(dbIndex):
		if RedisObj.__pool is None:
			__pool = redis.ConnectionPool(host='172.0.2.95', port='6379', db=dbIndex)
		return redis.Redis(connection_pool=__pool)

	def linkRedis(self):
		return self._redis
```

## File Download

```python
def file_iterator(file_name, chunk_size=512):
    with open(file_name,'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

response = StreamingHttpResponse(file_iterator(fileName))
response['Content-Type'] = 'application/vnd.ms-excel'
dis_temp = 'attachment;filename="{}"'.format(fN)
response['Content-Disposition'] = dis_temp
return response
```

## Others

```python
def getHostIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	return s.getsockname()[0]

def scpFileToLocal(fileSite, localSite):
    child = pexpect.spawn('scp {} {}'.format(fileSite, localSite))
    child.expect('password:')
    child.sendline(base64.b64decode(SSH_PSWD))
    child.read()

def registerSmb(self):
    child = self.hostAuth(SMB_COMMAND, False, self.usr)
    child.expect('password')
    child.sendline(base64.b64decode(DEFAULT_PWD))
    child.expect('password')
    child.sendline(base64.b64decode(DEFAULT_PWD))
    child.read()

```

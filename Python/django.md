# Django

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
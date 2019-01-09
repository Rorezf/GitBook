# Algorithms

## function

### Bunch模式

```python
class Bunch(dict):
	def __init__(self, *args, **kwds):
		super(Bunch, self).__init__(*args, **kwds)
		self.__dict__ = self

x = Bunch(name='hello', value='world')
x.name (hello)
```
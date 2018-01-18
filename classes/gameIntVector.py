class GVector():
	"""
	двумерный целочисленный вектор
	"""
	def __init__(self, x=0, y=0):
		self.x = int(x)
		self.y = int(y)

	def __str__(self):
		return 'Эт короче экзампляр GVector c координатами ({0},{1})'.format(self.x, self.y)
	def __add__(self, v2):
		return GVector(self.x + v2.x, self.y + v2.y)

	def __sub__(self, v2):
		return GVector(self.x-v2.x, self.y-v2.y)

	def __mul__(self, m):
		return GVector(int(self.x * m), int(self.y * m))

	def __getitem__(self, key):
		if key == 0:
			return self.x
		elif key == 1:
			return self.y
		else:
			raise BaseException('Нету больше ничего')

	def __setitem__(self, key, value):
		if key == 0:
			self.x = int(value)
		elif key == 1:
			self.y = int(value)
		else:
			raise BaseException('Нету больше ничего')

	def get(self):
		return (self.x, self.y)
		
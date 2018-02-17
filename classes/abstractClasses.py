import classes.gameIntVector
from classes.gameIntVector import GVector
from abc import abstractmethod, ABC

class RenderedObject(ABC):
	"""
    Этот класс - предок последующих отрисовываемых объектов
	"""
	def __init__(self, initPoint, focus):
		self.initPoint = initPoint
		self.focus = focus

	def __iter__(self):
		"""Функция возвращает итератор. Нужна для того, 
		чтобы использовать объект в качестве массива координат
		"""
		return iter(self.initPoint.get())

	@abstractmethod
	def draw(self, screen):
		"""отрисовывает объект на экране screen"""

	@abstractmethod
	def move(self, dt):
		"""изменяет параметры объекта в зависимости от времени dt"""

	def collide(self, point):
		"""Возвращает True, если точка point находится в пределах объекта"""
		return False

class PickableObject(ABC):
	"""Абстрактный класс для объектов, подбираемых в инвентарь"""
	def __init__(self, inventoryName):
		"""inventoryName - имя, под которым будет отображаться элемент в инвентаре"""
		self.inventoryName = inventoryName
	@abstractmethod
	def pick(self):
		"""вызывается при нажатии на кнопку "подобрать" игроком"""
		
	


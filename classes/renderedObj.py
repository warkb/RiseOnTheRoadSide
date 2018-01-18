import classes.gameIntVector
from classes.gameIntVector import GVector
from abc import abstractmethod

class RenderedObject():
	"""
    Этот класс - предок последующих
	"""
	def __init__(self, initPoint, focus):
		self.initPoint = initPoint
		self.focus = focus

	@abstractmethod
	def draw(self, screen):
		self.focus.x, self.focus.y = focus

	@abstractmethod
	def move(self, dt):
		pass
		
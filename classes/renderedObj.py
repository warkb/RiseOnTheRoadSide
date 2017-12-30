import classes.gameIntVector
from classes.gameIntVector import GVector

class RenderedObject():
	"""
    Этот класс - предок последующих
	"""
	def __init__(self, initPoint, initVel=GVector(0,0)):
		self.initPoint = initPoint
		self.initVel = initVel

	def move(self, dt):
		pass
		
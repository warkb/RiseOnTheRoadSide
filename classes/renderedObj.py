import classes.gameIntVector
from classes.gameIntVector import GVector

class RenderedObject():
	"""
    Этот класс - предок последующих
	"""
	def __init__(self, initPoint, initVel=GVector(0,0)):
		self.initPoint = initPoint
		self.initVel = initVel

		self.focus = GVector()

	def draw(self, screen, focus):
		self.focus.x, self.focus.y = focus

	def move(self, dt):
		pass
		
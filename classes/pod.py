import pygame
from classes.appFunctions import hexToTuple
from classes.renderedObj import RenderedObject
from classes.gameIntVector import GVector

class Pod(pygame.surface.Surface, RenderedObject):
	"""
	Подложка под героем с травой
	которая перемещается так, чтобы всегда быть под героем
	"""
	def __init__(self, x, y, w, h):
		pygame.surface.Surface.__init__(self, (int(w), int(h)))
		RenderedObject.__init__(self, GVector(x, y))
		self.color = '65A835'
		self.fill(hexToTuple(self.color))
	def draw(self, screen, focus):
		RenderedObject.draw(self, screen, focus)
		screen.blit(self, (self.initPoint - self.focus).get())

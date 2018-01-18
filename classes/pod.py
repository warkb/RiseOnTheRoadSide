import pygame
from pygame.locals import*
from classes.appFunctions import hexToTuple
from classes.renderedObj import RenderedObject
from classes.gameIntVector import GVector
from random import randint

class Pod(pygame.surface.Surface, RenderedObject):
	"""
	Подложка под героем с травой
	которая перемещается так, чтобы всегда быть под героем
	"""
	def __init__(self, x, y, w, h, focus):
		pygame.surface.Surface.__init__(self, (int(w), int(h)), flags=SRCALPHA,
			depth=32)
		RenderedObject.__init__(self, GVector(x, y), focus=focus)
		self.width = w
		self.height = h
		self.grassWidth = 20
		self.grassHeight = 20
		self.grassNum = 20
		self.genField()


	def genField(self):
		"""Заполняет подложку травой"""
		pygame.surface.Surface.__init__(self, (int(self.width), int(self.height)),
		 flags=SRCALPHA, depth=32)
		#debug
		#self.fill((randint(10, 250), randint(10, 250), randint(10, 250)))
		for _ in range(self.grassNum):
			x = randint(0, 0 - self.grassWidth + self.width)
			y = randint(0, 0 - self.grassHeight + self.height)
			self.blit(Grass(self.grassWidth, self.grassHeight),
				(x, y))

		
	def draw(self, screen):
		fvx, fvy = (self.focus - self.initPoint).get()
		if fvx > self.width:
			self.initPoint.x += 2 * self.width
			self.genField()
		if fvx < -self.width:
			self.initPoint.x -= 2 * self.width
			self.genField()

		if fvy > self.height:
			self.initPoint.y += 2 * self.height
			self.genField()
		if fvy < -self.height:
			self.initPoint.y -= 2 * self.height
			self.genField()

		screen.blit(self, (self.initPoint - self.focus).get())


class Grass(pygame.surface.Surface, RenderedObject):
	"""Трава, которая будет на подложке"""
	def __init__(self, w, h):
		pygame.surface.Surface.__init__(self, (int(w), int(h)))
		self.color = '65A835'
		self.fill(hexToTuple(self.color))

		
import classes.renderedObj
from classes.renderedObj import RenderedObject, GVector
import pygame
from math import sin, cos

class Player(RenderedObject):
	"""docstring for Player"""
	def __init__(self, x, y):
		RenderedObject.__init__(self, GVector(x,y))
		self.rad = 30
		self.angle = 0
		self.half = GVector(self.rad, self.rad)
		self.color = (0, 205, 244)

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (self.initPoint).get(), self.rad, 2)
		pygame.draw.line(screen, self.color, self.initPoint.get(), 
			(self.initPoint+(GVector(sin(self.angle), 
				-cos(self.angle))*self.rad)).get(), 2)
		
		
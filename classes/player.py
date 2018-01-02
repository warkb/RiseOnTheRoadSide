import classes.renderedObj
from classes.renderedObj import RenderedObject, GVector
import pygame
from math import sin, cos
from classes.appFunctions import hexToTuple

class Player(RenderedObject):
	"""docstring for Player"""
	def __init__(self, x, y):
		initPlayerVelocity = GVector(0, 0)
		RenderedObject.__init__(self, GVector(x,y), initPlayerVelocity)
		self.rad = 30
		self.angle = 0
		self.color = hexToTuple('F48C16')
		self.frictionalCoefficient = 7
		#константы, отвечающие за движение по нажатию клавиши
		self.pushVelocity = 400#скорость, получаемая при нажатии кнопки вперед

	def goUp(self):
		"""
		Вызывается при нажатии кнопки движения вперед
		"""
		self.initVel.y = -self.pushVelocity
	def goDown(self):
		"""
		Вызывается при нажатии кнопки движения назад
		"""
		self.initVel.y = self.pushVelocity
	def goRight(self):
		"""
		Вызывается при нажатии кнопки движения направо
		"""
		self.initVel.x = self.pushVelocity
	def goLeft(self):
		"""
		Вызывается при нажатии кнопки движения налево
		"""
		self.initVel.x = -self.pushVelocity
	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (self.initPoint).get(), self.rad, 3)
		pygame.draw.aaline(screen, self.color, self.initPoint.get(), 
			(self.initPoint+(GVector(sin(self.angle), 
				-cos(self.angle))*self.rad)).get(), 3)

	def move(self, dt):
		"""
		запускается каждую итерацию, двигает героя,
		менятет его скорость
		"""
		self.initVel -= self.initVel * self.frictionalCoefficient * dt
		self.initPoint += self.initVel * dt
		
		
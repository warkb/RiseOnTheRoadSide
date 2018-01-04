import classes.renderedObj
from classes.renderedObj import RenderedObject, GVector
import pygame
from math import sin, cos, atan2, pi
from classes.appFunctions import hexToTuple

class Player(RenderedObject):
	"""docstring for Player"""
	def __init__(self, x, y):
		initPlayerVelocity = GVector(0, 0)
		RenderedObject.__init__(self, GVector(x,y), initPlayerVelocity)
		self.rad = 30
		self.angle = 0
		self.color = hexToTuple('F48C16')
		self.frictionalCoefficient = 13
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
	def draw(self, screen, focus):
		RenderedObject.draw(self, screen, focus)
		viewPoint = (self.initPoint+(GVector(sin(self.angle)*self.rad, 
				-cos(self.angle)*self.rad))-self.focus).get()
		pygame.draw.circle(screen, self.color, (self.initPoint-self.focus).get(),
		 self.rad, 3)
		pygame.draw.line(screen, self.color, (self.initPoint-self.focus).get(), 
			viewPoint, 3)
	def move(self, dt):
		"""
		запускается каждую итерацию, двигает героя,
		менятет его скорость, а также угол
		"""
		x, y = pygame.mouse.get_pos()
		x += self.focus.x
		y += self.focus.y
		self.angle = atan2(y - self.initPoint.y, x - self.initPoint.x) + pi/2
		self.initVel -= self.initVel * self.frictionalCoefficient * dt
		self.initPoint += self.initVel * dt
		
		
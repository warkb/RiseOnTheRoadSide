import classes.abstractClasses
from classes.artefact import Artefact
from classes.abstractClasses import RenderedObject, GVector
from classes.commonConsts import pickKeyStr
import pygame
from math import sin, cos, atan2, pi
from classes.appFunctions import hexToTuple, isCollideRoundAndPoint

class Player(RenderedObject):
	"""docstring for Player"""
	def __init__(self, x, y, focus, game):
		initPlayerVelocity = GVector(0, 0)
		RenderedObject.__init__(self, GVector(x,y), focus)
		self.game = game

		self.initVel = GVector()
		self.rad = 30
		self.angle = 0
		self.color = hexToTuple('F48C16')
		self.frictionalCoefficient = 13
		#константы, отвечающие за движение по нажатию клавиши
		self.pushVelocity = 400#скорость, получаемая при нажатии кнопки вперед

		self.inventory = []
		self.pickDistance = 60#расстояние, с которого игрок может взять предмет
		fontObj = pygame.font.Font('freesansbold.ttf', 18)
		self.takeKeySurf = fontObj.render(pickKeyStr, True, (255, 255, 255))
		self.takeKeyRect = self.takeKeySurf.get_rect()

		self.eRad = 12 # радиус черного кружочка под буковкой взять


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
	
	def pickObject(self, game):
		"""отправляет объет в инвентарь"""
		pickObj = game.objectUnderPick
		if pickObj:
			self.inventory.append(pickObj.inventoryName)
			if isinstance(pickObj, Artefact):
				game.getFreeFlyingText().revival(pickObj)
			pickObj.pick()

	def draw(self, screen):
		viewPoint = (self.initPoint+(GVector(sin(self.angle)*self.rad, 
				-cos(self.angle)*self.rad))-self.focus).get()
		pygame.draw.circle(screen, self.color, (self.initPoint-self.focus).get(),
		 self.rad, 3)
		pygame.draw.line(screen, self.color, (self.initPoint-self.focus).get(), 
			viewPoint, 3)

		# Если есть объект, который можно взять
		if self.game.objectUnderPick:
			# отрисовываем буковку, на которую назначено взять
			self.takeKeyRect.center = self.initPoint - self.focus
			pygame.draw.circle(screen, hexToTuple('884A01'), 
				self.initPoint - self.focus,
				self.eRad)
			screen.blit(self.takeKeySurf, self.takeKeyRect)


	def move(self, dt):
		"""
		запускается каждую итерацию, двигает героя,
		менятет его скорость, а также угол
		"""
		x, y = pygame.mouse.get_pos()
		x += self.focus[0]
		y += self.focus[1]
		self.angle = atan2(y - self.initPoint.y, x - self.initPoint.x) + pi/2
		self.initVel -= self.initVel * self.frictionalCoefficient * dt
		self.initPoint += self.initVel * dt
		
		
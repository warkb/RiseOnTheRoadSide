import pygame

from classes.artefact import Artefact
from classes.abstractClasses import RenderedObject, GVector
from classes.appFunctions import (hexToTuple, isCollideRoundAndPoint, 
	getRandomAngleInArea, getRandomPointOnCircle)
from classes.commonConsts import pickKeyStr, RED
from math import sin, cos, atan2, pi
from random import random, randint, choice
from time import time

class AnotherStalker(RenderedObject):
	"""Сталкер управляемый искусственным интеллектом"""
	baseRadius = 30 # базовый радиус персонажа
	spread = 10 # разброс по радиусу персонажа
	padding = 10 # расстояние от края персонажа до края поверхности
	# состояния
	choiceDirectionState = 'choiceDirectionState'
	uselessWalk = 'uselessWalk'

	def __init__(self, game):
		self.bornRadius = 200 # Радиус, в котором появляются сталкеры в начале
		randomAngle = 2 * pi * random()
		px, py = game.player.initPoint
		x, y = (self.bornRadius * -cos(randomAngle) + px, 
			self.bornRadius * sin(randomAngle) + py)
		RenderedObject.__init__(self, GVector(x, y), game.focus)
		self.game = game
		self.focus = game.focus
		# в какую сторону смотрит персонаж
		self.angle = randomAngle * 180 / pi
		print(self.angle)
		#self.angle = 180

		# его цвет
		self.color = tuple([randint(10, 250) for _ in range(3)])

		# его радиус
		self.radiusCharacter = self.baseRadius + randint(-self.spread, self.spread)
		self.createBaseSurf()

		# параметры для искусственного интеллекта
		self.state = self.uselessWalk
		self.maxWalkTime = randint(10, 30) # время, пока персонаж просто идет
		self.velocity = randint(50, 200) # скорость персонажа
		self.walkTime = self.maxWalkTime # текущий статус таймера

	def createBaseSurf(self):
		self.baseSurf = pygame.Surface(((self.radiusCharacter + self.padding) * 2, 
			(self.radiusCharacter + self.padding) * 2), flags=pygame.SRCALPHA)
		pygame.draw.circle(self.baseSurf, self.color, (self.radiusCharacter + self.padding, 
			self.radiusCharacter + self.padding), 
			self.radiusCharacter, 3)
		# рисуем линии
		randomPoints = [getRandomPointOnCircle(self.radiusCharacter - 2, 
			self.radiusCharacter + self.padding,
			self.radiusCharacter + self.padding) 
		for _ in range(8)]
		for i in range(0, 8, 2):
			pygame.draw.line(self.baseSurf, self.color, randomPoints[i],
				randomPoints[i + 1], 3)

		# рисуем кружочек, который будет показывать, куда смотрит персонаж
		pygame.draw.circle(self.baseSurf, self.color, (self.padding, 
			self.radiusCharacter + self.padding), 7)


		pygame.draw.circle(self.baseSurf, RED, (self.radiusCharacter + self.padding, 
			self.radiusCharacter + self.padding), 5)

	def draw(self, screen):
		newSurf = pygame.transform.rotate(self.baseSurf, self.angle)
		newRect = newSurf.get_rect()
		newRect.center = self.initPoint - self.focus
		screen.blit(newSurf, newRect)

		# screen.blit(newSurf, self.initPoint - self.focus - 
		# 	GVector(self.radiusCharacter + self.padding, 
		# 		self.radiusCharacter + self.padding))

	def move(self, dt):
		"""
		Как будет двигаться персонаж?
		Есть некоторое время, за которое персонаж тупо идет куда глаза глядят
		Как только оно Проходит, статус меняется на changeAngle.
		В статусе changeAngle сторона(угол), в которую смотрит персонаж меняется.
		Угол тем меньше, чем дальше персонаж от игрока. Если персонаж уже на каком-то
		расстоянии от игрока, он выбирает направление исключительно в сторону игрока.
		"""
		if self.state == self.uselessWalk:
			# сдвинуться
			# уменьшьть оставшееся время
			# если оставшееся время кончилось - меняем состояние 
			# на поворот
			angleRad = self.angle * pi / 180
			m = self.velocity * dt

			self.initPoint.x += -cos(angleRad) * m
			# print("x %s " % self.initPoint.x)
			self.initPoint.y += sin(angleRad) * m
			# print("y %s " % self.initPoint.y)
			self.walkTime -= dt





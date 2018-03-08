import pygame

from bisect import bisect
from pygame.locals import*
from classes.abstractClasses import RenderedObject, PickableObject
from classes.gameIntVector import GVector
from classes.commonConsts import (artefactsTypes, WIDTHSCREEN, HEIGHTSCREEN, 
	artefactSize, artTypesTuple, artProbsTuple, FPS)
from random import random, choice
from classes.appFunctions import generateRandomInJaggedArea, isCollideRoundAndPoint

"""
Туду: есть интересная идея: заставить артефакты случайно перемещаться, и ввести переменую,
которая будет отвечать за вероятность того, что артефакт сдвинется в сторону игрока
(или даже аномалии, типо артефакт завлекает сталкера в аномалию)
"""


class Artefact(RenderedObject, PickableObject):
	"""Артефакты, которые можно собирать в инвентарь"""
	pulseRad = 3 # колебания радиуса артефакта
	maxPulse = FPS
	def __init__(self, focus, inventoryName='grayball'):
		RenderedObject.__init__(self, GVector(), focus=focus)
		self.inventoryName = inventoryName
		if not inventoryName in artTypesTuple:
			self.inventoryName ='grayball'
		PickableObject.__init__(self, self.inventoryName)
		self.color = artefactsTypes[self.inventoryName]['color']
		self.price = artefactsTypes[self.inventoryName]['price']
		self.radius = artefactSize

		self.deltaPulse = choice([-1, 1])
		self.pulse = 0


	def toPulse(self):
		"""
		Отвечает за пульсирование артефакта
		"""
		self.pulse += self.deltaPulse * self.price / 500
		if self.pulse < - self.maxPulse or self.pulse > self.maxPulse:
			self.deltaPulse *= -1
		return int(self.pulseRad * (self.pulse / self.maxPulse))


	def move(self, dt):
		#если игрок слишком далеко отошел от артефакта
		if not self.initPoint.inRectangle(self.focus - GVector(WIDTHSCREEN, HEIGHTSCREEN),
			self.focus + GVector(WIDTHSCREEN, HEIGHTSCREEN) * 2):
			#переместим за пределы видимости игрока
			self.relocate()

	def draw(self, screen):
		""""""
		pygame.draw.circle(screen, self.color, self.initPoint - self.focus, 
			self.radius + self.toPulse())

	def relocate(self):
		"""
		Перемещает артефакт за пределы видимости игрока в случае, 
		если игрок слишком далеко отойдет или заберет артефакт в инвентарь
		"""
		bArray = [WIDTHSCREEN, HEIGHTSCREEN]
		bArray[choice((0, 1))] = -self.radius#это нужно для того, чтобы артефакты
		#распределялись по полю более равномерно
		self.initPoint.x = generateRandomInJaggedArea(-WIDTHSCREEN, bArray[0], 
			WIDTHSCREEN, WIDTHSCREEN * 2)
		self.initPoint.y = generateRandomInJaggedArea(-HEIGHTSCREEN, bArray[1], 
			HEIGHTSCREEN, HEIGHTSCREEN * 2)
		self.initPoint += self.focus
		self.setTypeRandomly()

	def setTypeRandomly(self):
		"""
		меняет тип артефакта на случайный, в зависимости от цены: чем дороже,
		тем ниже вероятность
		"""
		posArr = []
		curPos = 0
		for posb in artProbsTuple:
			curPos += posb
			posArr.append(curPos)

		self.inventoryName = artTypesTuple[bisect(posArr, random())]
		self.color = artefactsTypes[self.inventoryName]['color']
		self.price = artefactsTypes[self.inventoryName]['price']

	def pick(self):
		self.relocate()

	def collide(self, point):
		return isCollideRoundAndPoint(self, point, self.radius)
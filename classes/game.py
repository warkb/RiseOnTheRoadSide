import pygame
import classes.player

from classes.player import Player
from classes.abstractClasses import PickableObject
from sys import exit
from classes.artefact import Artefact
from classes.anotherStalker import AnotherStalker
from classes.appFunctions import hexToTuple, isCollideRoundAndPoint
from classes.debugInfo import DebugInfo
from classes.flyingText import FlyingText
from classes.pod import Pod
from classes.commonConsts import (WIDTHSCREEN, HEIGHTSCREEN, artefactQuantitiy, 
	pickKey, FPS, flyingTextCount, QUANTITY_OF_ANOTHER_STALKERS)
from classes.gameIntVector import GVector
from pygame.locals import *

class Game():
	"""
	Это экземпляр класса, в конструкторе которого будет запускаться игра
	TODO: Сделать так, чтобы pygame и прочие запускались из папки lib
	*Есть ещё такая идея, списки объектов запихивать не в list, а в set
	"""
	def __init__(self):
		self.WIDTHSCREEN = WIDTHSCREEN
		self.HEIGHTSCREEN = HEIGHTSCREEN

		#переменные фокуса
		self.focus = GVector()

		#зазор для фокуса
		self.focusMargin = int(self.HEIGHTSCREEN / 4)

		self.MAINCOLOR = hexToTuple('B6F788')
		self.fpsClock = pygame.time.Clock()
		self.player = Player(self.WIDTHSCREEN / 2, self.HEIGHTSCREEN / 2, self.focus, self)
		#добавляем подложки
		self.pods = []
		for i in [-1, 0, 1]:
			for j in [0, -1, 1]:
				self.pods.append(Pod(i * self.WIDTHSCREEN, j * self.HEIGHTSCREEN,
				 self.WIDTHSCREEN, self.HEIGHTSCREEN, self.focus))
		self.addArtefacts()

		# добавляем flying text
		self.flyingTexts = [FlyingText(self.focus) for _ in range(flyingTextCount)]
		# self.flyingTexts = 
		self.debugInfo = DebugInfo(self)
		self.anotherStalkerS = tuple([AnotherStalker(self) 
			for _ in range(QUANTITY_OF_ANOTHER_STALKERS)])
		self.objects = (
				self.pods,
				self.artefacts,
				self.anotherStalkerS,
				[self.player],
				self.flyingTexts,
				[self.debugInfo]
				)
		self.mousePoint = (0, 0) # кортеж с координатами мыши, чтобы несколько раз
		# не узнавать её координаты через функцию
		self.objectUnderPick = None
		self.run()

	def getObjectUnderPoint(self, point, ignoreList=[]):
		"""
		Возвращает ссылку на объект находящийся под точкой
		и не находящийся в списке ignoreList.
		Если ничего не находит - возвращает None
		"""
		for curArr in reversed([self.artefacts]):
			for obj in reversed(curArr):
				if not isinstance(obj, PickableObject):
					# если не подбираемый объект - смотрим следующий
					continue
				if obj.collide(point):
					if isCollideRoundAndPoint(self.player, obj, 
						self.player.pickDistance):
						return obj


	def addArtefacts(self):
		"""
		Добавляет на игровое поле артефакты
		"""
		self.artefacts = []
		for _ in range(artefactQuantitiy):
			artefact = Artefact(focus=self.focus)
			artefact.relocate()
			self.artefacts.append(artefact)


	def drawWorld(self):
		"""
		Вот эта вот замечательная функция 
		будет отрисовывать мир.
		По идее, она должна выполняться отдельным
		потоком, или с помощью модуля acyncio"""
		self.screen.fill(self.MAINCOLOR)
		for objArr in self.objects:
			for obj in objArr:
				obj.draw(self.screen)
		pygame.display.update()

	def moveWorld(self, dt):
		"""
		Все действия, связаанные с изменением параметров мира
		делаются в этой функции. Так же, выполняется с помощью
		потоков или asyncio"""
		#self.player.move(dt)
		for objArr in self.objects:
			for obj in objArr:
				obj.move(dt)

	def run(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.WIDTHSCREEN, 
			self.HEIGHTSCREEN), pygame.FULLSCREEN, 32)
		self.running = True
		dt = 0
		#обрабатываем события
		while self.running:
			self.moveWorld(dt)
			#пересчитываем фокус
			px, py = self.player.initPoint.get()
			mx, my = pygame.mouse.get_pos()#координаты мыши
			self.mousePoint = GVector(mx, my) + self.focus

			self.objectUnderPick = self.getObjectUnderPoint(self.mousePoint)
			if px < self.focus[0] + self.focusMargin:
				self.focus[0] = px - self.focusMargin
			if px > self.focus[0] + self.WIDTHSCREEN - self.focusMargin:
				self.focus[0] = px - self.WIDTHSCREEN + self.focusMargin
			if py < self.focus[1] + self.focusMargin:
				self.focus[1] = py - self.focusMargin
			if py > self.focus[1] + self.HEIGHTSCREEN - self.focusMargin:
				self.focus[1] = py - self.HEIGHTSCREEN + self.focusMargin

			self.drawWorld()#<- пока тут, потом в поток занесу
			pressedKeys=pygame.key.get_pressed()
			#вперед
			if ((pressedKeys[K_UP] or pressedKeys[K_w]) and 
				not (pressedKeys[K_DOWN] or pressedKeys[K_s])):
				self.player.goUp()
			#наэад
			elif ((pressedKeys[K_DOWN] or pressedKeys[K_s]) and 
				not (pressedKeys[K_UP] or pressedKeys[K_w])):
				self.player.goDown()
			#направо
			if ((pressedKeys[K_RIGHT] or pressedKeys[K_d]) and 
				not(pressedKeys[K_LEFT] or pressedKeys[K_a])):
				self.player.goRight()
			#налево
			if ((pressedKeys[K_LEFT] or pressedKeys[K_a]) and 
				not (pressedKeys[K_RIGHT] or pressedKeys[K_d])):
				self.player.goLeft()
			#выход из игры
			if pressedKeys[K_ESCAPE]:
				self.running = False
			for event in pygame.event.get():
				if event.type == QUIT:
					#выходим по нажатию на крестик
					self.running = False
				elif event.type==KEYDOWN:
					#хватаем предмет
					if (event.key==pickKey):
						self.pickAction()
					elif event.key==K_ESCAPE:
						self.running = False

		#обработали---
			dt = (self.fpsClock.tick(FPS)) / 1000
		exit()

	def pickAction(self):
		"""выполняется, когда нажата клавиша взять"""
		self.player.pickObject(self)
		
	def getFreeFlyingText(self):
		"""
		Возвращает первый свободный flyingText
		Если таких нет - делает исключение
		"""
		for ft in self.flyingTexts:
			if not ft.active:
				return ft
		raise BaseException("Слишком мало летучих текстов")

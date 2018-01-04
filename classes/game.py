import pygame
from pygame.locals import *
import classes.player
from classes.player import Player
from sys import exit
from classes.appFunctions import hexToTuple
from classes.pod import Pod

class Game():
	"""
	TODO: Сделать так, чтобы pygame и прочие запускались из папки lib
	Это экземпляр класса, в конструкторе которого будет запускаться игра
	"""
	def __init__(self):
		self.WIDTHSCREEN = 1024
		self.HEIGHTSCREEN = 700

		#переменные фокуса
		self.focusX = 0
		self.focusY = 0

		#зазор для фокуса
		self.focusMargin = int(self.HEIGHTSCREEN / 4)

		self.MAINCOLOR = hexToTuple('B6F788')
		self.fps = 60
		self.fpsClock = pygame.time.Clock()
		self.player = Player(self.WIDTHSCREEN / 2, self.HEIGHTSCREEN / 2)
		#добавляем подложки
		self.pods = []
		for i in [-1, 0, 1]:
			for j in [0, -1, 1]:
				self.pods.append(Pod(i * self.WIDTHSCREEN, j * self.HEIGHTSCREEN,
				 self.WIDTHSCREEN, self.HEIGHTSCREEN))
		self.objects = {'player': [self.player], 'pods': self.pods}
		self.run()

	def drawWorld(self):
		"""
		Вот эта вот замечательноя функция 
		будет отрисовывать мир.
		По идее, она должна выполняться отдельным
		потоком, или с помощью модуля acyncio"""
		self.screen.fill(self.MAINCOLOR)
		#рисуем подложку
		fTuple = (self.focusX, self.focusY)
		for obj in self.objects['pods']:
			obj.draw(self.screen, fTuple)
		#рисуем игрока
		self.player.draw(self.screen, fTuple)
		pygame.display.update()

	def moveWorld(self, dt):
		"""
		Все действия, связаанные с изменением параметров мира
		делаются в этой функции. Так же, выполняется с помощью
		потоков или asyncio"""
		#self.player.move(dt)
		for key in self.objects:
			for obj in self.objects[key]:
				obj.move(dt)

	def run(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.WIDTHSCREEN, 
			self.HEIGHTSCREEN), 0, 32)
		self.running = True
		dt = 0
		#обрабатываем события
		while self.running:
			self.moveWorld(dt)
			#пересчитываем фокус
			px, py = self.player.initPoint.get()
			if px < self.focusX + self.focusMargin:
				self.focusX = px - self.focusMargin
			if px > self.focusX + self.WIDTHSCREEN - self.focusMargin:
				self.focusX = px - self.WIDTHSCREEN + self.focusMargin
			if py < self.focusY + self.focusMargin:
				self.focusY = py - self.focusMargin
			if py > self.focusY + self.HEIGHTSCREEN - self.focusMargin:
				self.focusY = py - self.HEIGHTSCREEN + self.focusMargin

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
				# elif event.type==KEYDOWN:
				# 	if (event.key==K_UP or event.key==K_w):
				# 		self.player.goUp()
				# 	elif event.key==K_ESCAPE:
				# 		self.running = False
		#обработали---
			dt = (self.fpsClock.tick(self.fps)) / 1000
		exit()

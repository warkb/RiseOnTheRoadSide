import pygame
from pygame.locals import *

class Game():
	"""
	TODO: Сделать так, чтобы pygame и прочие запускались из папки lib
	Это экземпляр класса, в конструкторе которого будет запускаться игра
	"""
	def __init__(self):
		self.HEIGHTSCREEN = 600
		self.WIDTHSCREEN = 800
		self.MAINCOLOR = (147, 255, 71)

		self.objects = {}
		self.run()

	def drawWorld(self):
		"""
		Вот эта вот замечательноя функция 
		будет отрисовывать мир.
		По идее, она должна выполняться отдельным
		потоком, или с помощью модуля acyncio"""
		self.screen.fill(self.MAINCOLOR)
		pass
		pygame.display.update()

	def moveWorld(self):
		"""
		Все действия, связаанные с изменением параметров мира
		делаются в этой функции. Так же, выполняется с помощью
		потоков или asyncio"""
		pass

	def run(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.WIDTHSCREEN, 
			self.HEIGHTSCREEN), 0, 32)
		self.running = True
		while self.running:
			self.drawWorld()
			for event in pygame.event.get():
				if event.type == QUIT:
					#выходим по нажатию на крестик
					self.running = False


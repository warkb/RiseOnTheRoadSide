import pygame

from classes.abstractClasses import RenderedObject
from classes.gameIntVector import GVector
from classes.commonConsts import FPS

pygame.init()

class FlyingText(RenderedObject):
	"""Это будет объект, 
	который будет содержать в себе текст,
	при этом равномерно поднимаясь вверх
	и плавно исчезая"""
	"""
	Как это по идее будет работать?
	Есть некий кортеж с объектами flying text. Как только взят предмет,
	мы берем свободный flying text, передаем ему тип артефакта и его цвет,
	делаем active, плюс - его позицию. 

	*сделать функцию getFree - возвращающую первый неактивный flying text
	*сделать для FlyingText функцию revival - делающую его статус активным,
	и отдающую ссылку на объект с артефактом
	*сделать в главном цикле визуализацию по кругу для FlyingText
	"""
	# дистанция, на которую поднимется надпись перед исчезновением
	upDistance = 100 

	fadeTime = 2 * FPS # как долго будет затухать текст
	fontSize = 32
	def __init__(self, focus):
		RenderedObject.__init__(self, GVector(), focus)
		self.color = None
		self.active = False
		self.fontObj = pygame.font.Font('freesansbold.ttf', self.fontSize)
		# счетчик показывающий, как много fps прошло с начала возрождения
		self.counter = 0 

	def revival(self, artefact):
		self.active = True
		self.counter = 0
		self.initPoint = GVector(artefact.initPoint.get())
		self.color = artefact.color
		self.text = '+' + str(artefact.price)
		self.textSurf = self.fontObj.render(self.text, True, self.color)
		self.textRect = self.textSurf.get_rect()

	def draw(self, screen):
		if self.active:
			# alpha = int(self.counter * 255 / self.fadeTime)
			# self.textSurf = self.fontObj.render(self.text, True, (alpha,alpha,alpha,alpha))
			self.textSurf = self.textSurf.convert_alpha()
			x, y = (self.initPoint - self.focus).get()
			self.textRect.center = (x, y - (self.counter * self.upDistance) / 
				self.fadeTime)
			screen.blit(self.textSurf, self.textRect)
			# pygame.draw.circle(screen, (0,0,0), self.initPoint - self.focus, 50)


	def move(self, dt):
		if self.active:
			self.counter += 1
			if self.counter > self.fadeTime:
				print("А точка отображения на экране %s" % (self.initPoint - self.focus))
				self.active = False


		

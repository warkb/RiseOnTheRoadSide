import pygame
from classes.abstractClasses import RenderedObject
from classes.appFunctions import hexToTuple


class DebugInfo(RenderedObject):
	"""
	Класс выводит отладочную информацию
	на экран
	"""
	def __init__(self, game):
		RenderedObject.__init__(self, (0, 0), None)
		self.game = game
		self.fps = 0
		self.font = pygame.font.Font('freesansbold.ttf', 32)
		self.margin = 10 # отступ от края
		self.color = hexToTuple('FE655B')

	def draw(self, screen):
		text = self.font.render("FPS: %s" % self.fps, True, self.color)
		screen.blit(text, (self.margin, self.margin))

	def move(self, dt):
		if dt != 0:
			self.fps = int(1 / dt)
		
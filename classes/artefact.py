import pygame
from pygame.locals import*
from classes.renderedObj import RenderedObject
from classes.gameIntVector import GVector
from classes.commonConsts import artefactsType, WIDTHSCREEN, HEIGHTSCREEN

class Artefact(RenderedObject):
	"""Артефакты, которые можно собирать в инвентарь"""
	def __init__(self, x, y, focus, artType='grayball'):
		RenderedObject.__init__(GVector(x, y))

		if not artType in artefactsType:
			artType ='grayball'

	def move(self, dt):
		pass

	def draw(self, screen):
		pass

	def relocate(self, focus):
		"""
		Перемещает артефакт за пределы видимости игрока в случае, 
		если игрок слишком далеко отойдет или заберет артефакт в инвентарь
		"""
		focusPoint = focus - 



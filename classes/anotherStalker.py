import pygame

from classes.artefact import Artefact
from classes.abstractClasses import RenderedObject, GVector
from classes.appFunctions import (hexToTuple, isCollideRoundAndPoint, 
    getRandomAngleInArea, getRandomPointOnCircle, getAngleFromPointToPoint, 
    distanceToPoint)
from classes.commonConsts import pickKeyStr, RED
from math import sin, cos, atan2, pi
from random import random, randint, choice
from time import time

class AnotherStalker(RenderedObject):
    """Сталкер управляемый искусственным интеллектом"""
    baseRadius = 20 # базовый радиус персонажа
    spread = 5 # разброс по радиусу персонажа
    padding = 10 # расстояние от края персонажа до края поверхности
    angleSpeed = 50
    seeArtefactDistance = 500 # на этом расстоянии бот видит артефакт
    pickDistance = 60 # с какого расстояния можно брать артефакт
    # состояния
    choiceDirectionState = 'choiceDirectionState'
    uselessWalk = 'uselessWalk'
    angleChangingStatus = 'angleChangingStatus'
    artefactHunt = 'artefactHunt'

    def __init__(self, game):
        self.bornRadius = game.WIDTHSCREEN # Радиус, в котором появляются сталкеры в начале
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
        self.color = tuple([randint(0, 25) * 10 for _ in range(3)])

        # его радиус
        self.radiusCharacter = self.baseRadius + randint(-self.spread, self.spread)
        self.createBaseSurf()

        # параметры для искусственного интеллекта
        self.state = self.uselessWalk
        self.maxWalkTime = randint(5, 15) # время, пока персонаж просто идет
        self.velocity = randint(100, 150) # скорость персонажа
        self.walkTime = self.maxWalkTime # текущий статус таймера

    def createBaseSurf(self):
        """
        Рисуем персонажа
        """
        self.baseSurf = pygame.image.load('img/persBase.png')
        pygame.draw.circle(self.baseSurf, self.color, 
            self.baseSurf.get_rect().center, self.radiusCharacter)
        pygame.draw.rect(self.baseSurf, self.color, (0, 0, 20, 20))

    def changeNewAngle(self):
        angle = getAngleFromPointToPoint(self.initPoint, self.game.player.initPoint)
        distanceToPlayer = distanceToPoint(self.initPoint, self.game.player.initPoint)
        if distanceToPlayer < self.game.WIDTHSCREEN:
            angle += randint(-90, 90) * ((self.game.WIDTHSCREEN - distanceToPlayer)
                / self.game.WIDTHSCREEN) # чем дальше игрок, тем меньше разброс
        return angle

    def draw(self, screen):
        newSurf = pygame.transform.rotate(self.baseSurf, self.angle + 90)
        newRect = newSurf.get_rect()
        newRect.center = self.initPoint - self.focus
        if distanceToPoint(self.initPoint, self.nearestArtefact.initPoint) < self.seeArtefactDistance:
            pygame.draw.circle(newSurf,(255, 0, 0), (10,10), 10)
        screen.blit(newSurf, newRect)

        # screen.blit(newSurf, self.initPoint - self.focus - 
        #     GVector(self.radiusCharacter + self.padding, 
        #         self.radiusCharacter + self.padding))

    def move(self, dt):
        """
        Как будет двигаться персонаж?
        Есть некоторое время, за которое персонаж тупо идет куда глаза глядят
        Как только оно Проходит, статус меняется на changeAngle.
        В статусе changeAngle сторона(угол), в которую смотрит персонаж меняется.
        Угол тем меньше, чем дальше персонаж от игрока. Если персонаж уже на каком-то
        расстоянии от игрока, он выбирает направление исключительно в сторону игрока.
        """
        # охота за артефактами старт
        # находим самый близкий артефакт
        self.nearestArtefact = self.game.artefacts[0]
        minDistance = distanceToPoint(self.initPoint, self.nearestArtefact)
        for artefact in self.game.artefacts:
            distance = distanceToPoint(self.initPoint, artefact)
            if distance < minDistance:
                self.nearestArtefact = artefact
                minDistance = distance
        # нашли самый близкий артефакт
        # теперь проверяем, видит ли бот этот артефакт
        if minDistance < self.seeArtefactDistance:
            # поворачиваемся и бежим в сторону артефакта
            self.state = self.artefactHunt
            # если угол не совпадает - поворачиваем бота
            angleToArtefact = getAngleFromPointToPoint(self.initPoint,
                self.nearestArtefact.initPoint)
            if abs(angleToArtefact - self.angle) > 1:
                if angleToArtefact - self.angle > 0:
                    self.angle += dt * self.angleSpeed
                else:
                    self.angle -= dt * self.angleSpeed
            elif self.seeArtefactDistance > self.pickDistance:
                # не можем дотянуться до артефакта
                # делаем шаг вперед
                self.makeStep(dt)

        else:
            if self.state == self.artefactHunt:
                self.state = self.uselessWalk
        # охота за артефактами конец
        if self.state == self.uselessWalk:
            # сдвинуться
            # уменьшьть оставшееся время
            # если оставшееся время кончилось - меняем состояние 
            # на поворот
            self.makeStep(dt)
            # print("y %s " % self.initPoint.y)
            self.walkTime -= dt
            if self.walkTime < 0:
                self.state = self.choiceDirectionState
                self.walkTime = self.maxWalkTime

        if self.state == self.choiceDirectionState:
            self.newAngle = self.changeNewAngle()
            if self.newAngle - self.angle > 0:
                self.dAngle = 1 # прирост угла будет положительным
            else:
                self.dAngle = -1
            self.state = self.angleChangingStatus;

        if self.state == self.angleChangingStatus:
            self.angle += dt * self.dAngle * self.angleSpeed
            if abs(self.angle - self.newAngle) < 3:
                self.state = self.uselessWalk
    def makeStep(self, dt):
        """
        Продвигаем персонажа вперед по курсу
        :param dt: Время между кадрами
        :return:
        """
        angleRad = self.angle * pi / 180
        m = self.velocity * dt

        self.initPoint.x += -cos(angleRad) * m
        # print("x %s " % self.initPoint.x)
        self.initPoint.y += sin(angleRad) * m
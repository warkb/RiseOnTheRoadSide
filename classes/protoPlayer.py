import pygame
from abc import abstractmethod, ABC
from classes.artefact import Artefact
from classes.abstractClasses import RenderedObject, GVector
from math import sin, cos, atan2, pi
from classes.commonConsts import pickKeyStr
from classes.appFunctions import hexToTuple, isCollideRoundAndPoint


class ProtoPlayer(RenderedObject, ABC):
    """
    Класс персонажей, в том числе и самого игрока
    Персонаж может: ходить, брать артефакты, взрываться от аномалий
    """

    def __init__(self, x, y, focus, game):
        RenderedObject.__init__(self, GVector(x, y), focus)
        self.game = game

        self.initVel = GVector()
        self.rad = 30
        self.angle = 0
        self.color = hexToTuple('F48C16')
        self.frictionalCoefficient = 13
        # константы, отвечающие за движение по нажатию клавиши
        self.pushVelocity = 400  # скорость, получаемая при нажатии кнопки вперед

        self.inventory = []
        self.pickDistance = 60  # расстояние, с которого игрок может взять предмет
        fontObj = pygame.font.Font('freesansbold.ttf', 18)
        self.takeKeySurf = fontObj.render(pickKeyStr, True, (255, 255, 255))
        self.takeKeyRect = self.takeKeySurf.get_rect()

        self.eRad = 12  # радиус черного кружочка под буковкой взять

    @abstractmethod
    def useBrains(self, dt):
        """
        Выполняется функция, определяющая
        какое действие выполнит персонаж
        Переопределяется в потомке
        """

    def move(self, dt):
        """
        запускается каждую итерацию, двигает героя,
        меняет его скорость, а также угол
        """
        self.useBrains(dt)
        self.initVel -= self.initVel * self.frictionalCoefficient * dt
        self.initPoint += self.initVel * dt

    def pickObject(self, game):
        """отправляет объет в инвентарь"""
        pickObj = game.objectUnderPick
        if pickObj:
            self.inventory.append(pickObj.inventoryName)
            if isinstance(pickObj, Artefact):
                game.getFreeFlyingText().revival(pickObj)
            pickObj.pick()

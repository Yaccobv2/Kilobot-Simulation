from cmath import sqrt
from math import fabs, pi, sin, cos, degrees, radians, exp
import pymunk
import numpy
import matplotlib

import pygame
import BasicFunc


def drawKilobots(kilobotArray, screen):
    for it in kilobotArray:
        it.drawKilobot(screen)


def drawFoods(kilobotArray, screen):
    for it in kilobotArray:
        it.drawFood(screen)


class Shape:

    def __init__(self, id, x, y,  r, g, b, radius):
        self.id = id
        self.index = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.radius = radius



    def GetX(self):
        return self.x

    def GetY(self):
        return self.y


    def drawCircle(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)

    def setPositon(self, x, y):
        self.x = x
        self.y = y

    def changeColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def changeColorKilobot(self, r, g, b):
        self.r = (255 / 7) * r
        self.g = (255 / 7) * g
        self.b = (255 / 7) * b


    def IsKilobotInsigt(self, kilobot):
            xDif = fabs(self.x - kilobot.x)
            yDif = fabs(self.y - kilobot.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < self.radius-15:
                return True



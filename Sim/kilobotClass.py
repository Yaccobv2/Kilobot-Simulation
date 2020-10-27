from cmath import sqrt
from math import fabs

import pygame


class Kilobot:

    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    x = 0
    y = 0
    r = 220
    g = 220
    b = 220
    fi = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (self.x, self.y), 20)

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def checkSingleCollision(self, X, Y):
            xDif = fabs(self.x - X)
            yDif = fabs(self.y - Y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < 40:
                return True
    def checkSingleCollisionPrediction(self,self_X,self_Y, X, Y):
            xDif = fabs(self_X - X)
            yDif = fabs(self_Y - Y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < 40:
                return True
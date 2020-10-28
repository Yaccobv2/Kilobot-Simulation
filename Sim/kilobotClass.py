from cmath import sqrt
from math import fabs, pi, sin, cos

import pygame


class Kilobot:

    def __init__(self, id, x, y, r, g, b):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b

    id = 0
    x = 0
    y = 0
    r = 220
    g = 220
    b = 220
    fi = 0
    removed = 0
    isStuck = 0

    def drawKilobot(self, screen, promien):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), promien)

    def moveKilobot(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        self.x = self.x + xSpeed
        self.y = self.y + ySpeed

    def calculateSpeedXY(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        return xSpeed, ySpeed

    def rotateKilobot(self, spinAngle):
        if self.isStuck == 1:
            self.fi = self.fi + 4
        else:
            self.fi = self.fi + spinAngle


    def checkSingleCollisionPrediction(self, self_X, self_Y, X, Y, promien):
        xSpeed, ySpeed = self.calculateSpeedXY(1)
        xDif = fabs(self_X - X)
        yDif = fabs(self_Y - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        self.isStuck = 0
        if Dif.real < 2 * promien + 1:
            self.isStuck = 1
            return True

    def checkWallCollisionPrediction(self, self_X, self_Y, resx, resy, promien):
        self.isStuck = 0
        if (self_X < promien + 1) | (self_Y < promien + 1) | (self_X > (resx - promien + 1)) | (
                self_Y > (resy - promien - 55 + 1)):
            self.isStuck = 1
            return True

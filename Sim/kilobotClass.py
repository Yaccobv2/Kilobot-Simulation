from cmath import sqrt
from math import fabs, pi, sin, cos

import pygame


def drawKilobots(kilobotArray, screen, promien):
    for it in kilobotArray:
        position = (it.x, it.y)
        it.drawKilobot(screen, promien)


class Kilobot:

    def __init__(self, id, x, y, fi, r, g, b):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fi = fi

    id = 0
    x = 0
    y = 0
    r = 0
    g = 0
    b = 0
    fi = 0
    removed = 0
    isStuck = 0

    def drawKilobot(self, screen, promien):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), promien)

    def setPositon(self, x, y):

        self.x = x
        self.y = y


    def changeColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def changeColorKilobot(self, r, g, b):
        self.r = (255/7)*r
        self.g = (255/7)*g
        self.b = (255/7)*b

    def moveKilobot(self, speed):
        angle = self.fi*pi/180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        self.x = self.x + xSpeed
        self.y = self.y + ySpeed

    def simple_move(self, x, y):

        self.x = self.x + x
        self.y = self.y + y

    def calculateSpeedXY(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        return xSpeed, ySpeed

    def rotateKilobot(self, spinAngle):
        self.fi = self.fi + spinAngle

    # predict collison between two kilobots for simple movement
    def checkSingleCollisionPrediction(self, self_X, self_Y, X, Y, promien):
        xSpeed, ySpeed = self.calculateSpeedXY(1)
        xDif = fabs(self_X - X)
        yDif = fabs(self_Y - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * promien + 1:
            return True

    # predict collison between kilobot and borders for simple movement
    def checkWallCollisionPrediction(self, self_X, self_Y, resx, resy, promien):
        if (self_X < promien + 1) | (self_Y < promien + 1) | (self_X > (resx - promien + 1)) | (
                self_Y > (resy - promien - 55 + 1)):
            return True

    # predict collison between two kilobots for rotation movement
    def checkCollisionPrediction_Rotaton(self, X, Y, promien, speed, fi_temp):
        fi_temp = self.fi+fi_temp
        angle = fi_temp*pi/180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        xDif = fabs(x_temp - X)
        yDif = fabs(y_temp - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * promien + 1:
            return True

    # predict collison between kilobot and borders for rotation movement
    def checkWallCollisionPrediction_Rotaton(self, resx, resy, promien, speed, fi_temp):
        fi_temp = self.fi + fi_temp
        angle = fi_temp * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        if (x_temp < promien + 1) | (y_temp < promien + 1) | (x_temp > (resx - promien + 1)) | (
                y_temp > (resy - promien - 55 + 1)):
            return True

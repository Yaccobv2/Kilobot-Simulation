from cmath import sqrt
from math import fabs, pi, sin, cos

import pygame


def drawKilobots(kilobotArray, screen):
    for it in kilobotArray:
        it.drawKilobot(screen)


def isIdPresent(inID, IDIRArray):
    for itr in IDIRArray:
        if itr == inID:
            return True
    else:
        return False


class Kilobot:

    def __init__(self, id, x, y, fi, r, g, b, radius):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fi = fi
        self.radius = radius
        self.inIRRangeKilobotID = []

    id = 0
    x = 0
    y = 0
    r = 0
    g = 0
    b = 0
    fi = 0
    removed = 0
    isStuck = 0
    infraredRadius = 50
    radius = 0

    def detectKilobotsInIRRange(self, kilobotArray):
        for botItr in kilobotArray:
            xDif = fabs(self.x - botItr.x)
            yDif = fabs(self.y - botItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if botItr.id == self.id:
                continue
            elif Dif.real < 2 * self.infraredRadius + 1:
                if not isIdPresent(botItr.id, self.inIRRangeKilobotID):
                    self.inIRRangeKilobotID.append(botItr.id)

    def drawKilobot(self, screen):
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

    def moveKilobot(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        self.x = self.x + xSpeed
        self.y = self.y + ySpeed

    def rotateKilobot(self, spinAngle):
        self.fi = self.fi + spinAngle

    def MotorsMoveKilobot(self, M1, M2):
        M_temp = M1 - M2
        self.fi = self.fi + M_temp*0.001
        xSpeed = sin(self.fi)
        ySpeed = cos(self.fi)
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

    # predict collison between two kilobots for simple movement
    def checkSingleCollisionPrediction(self, self_X, self_Y, X, Y):
        xSpeed, ySpeed = self.calculateSpeedXY(1)
        xDif = fabs(self_X - X)
        yDif = fabs(self_Y - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * self.radius + 1:
            return True

    # predict collison between kilobot and borders for simple movement
    def checkWallCollisionPrediction(self, self_X, self_Y, resx, resy):
        if (self_X < self.radius + 1) | (self_Y < self.radius + 1) | (self_X > (resx - self.radius + 1)) | (
                self_Y > (resy - self.radius - 55 + 1)):
            return True

    # predict collison between two kilobots for rotation movement
    def checkCollisionPrediction_Rotaton(self, X, Y, speed, fi_temp):
        fi_temp = self.fi + fi_temp
        angle = fi_temp * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        xDif = fabs(x_temp - X)
        yDif = fabs(y_temp - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * self.radius + 1:
            return True

    # predict collison between kilobot and borders for rotation movement
    def checkWallCollisionPrediction_Rotaton(self, resx, resy, speed, fi_temp):
        fi_temp = self.fi + fi_temp
        angle = fi_temp * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        if (x_temp < self.radius + 1) | (y_temp < self.radius + 1) | (x_temp > (resx - self.radius + 1)) | (
                y_temp > (resy - self.radius - 55 + 1)):
            return True


 # predict collison between two kilobots for Motors movement
    def checkCollisionPrediction_Motors(self, X, Y, fi_temp):
        angle = fi_temp
        xSpeed = sin(angle)
        ySpeed = cos(angle)
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        xDif = fabs(x_temp - X)
        yDif = fabs(y_temp - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * self.radius + 1:
            return True

    # predict collison between kilobot and borders for Motors movement
    def checkWallCollisionPrediction_Motors(self, resx, resy, fi_temp):
        angle = fi_temp
        xSpeed = sin(angle)
        ySpeed = cos(angle)
        x_temp = self.x + xSpeed
        y_temp = self.y + ySpeed
        if (x_temp < self.radius + 1) | (y_temp < self.radius + 1) | (x_temp > (resx - self.radius + 1)) | (
                y_temp > (resy - self.radius - 55 + 1)):
            return True
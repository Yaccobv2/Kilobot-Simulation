from cmath import sqrt
from math import fabs, pi, sin, cos, degrees, radians, exp

import pygame
import pymunk


def drawKilobots(kilobotArray, screen, promien):
    for it in kilobotArray:
<<<<<<< Updated upstream
        position = (it.x, it.y)
        it.drawKilobot(screen, promien)
=======
        it.drawKilobot(screen)


def drawFoods(kilobotArray, screen):
    for it in kilobotArray:
        it.drawFood(screen)
>>>>>>> Stashed changes


class Kilobot:

    def __init__(self, id, x, y, r, g, b):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
<<<<<<< Updated upstream

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
=======
        self.fi = fi
        self.xMovement = 0
        self.yMovement = 0
        self.radius = radius
        self.inIRRangeKilobotID = []
        self.inIRRangeFoodID = []
        self.front_x = x
        self.front_y = y + radius - 2
        self.front_radius = radius - 13
        self.front_r = 0
        self.front_g = 0
        self.front_b = 255
        self.V = 0.5
        self.spin = 1
        self.speedTowardsTarget = 0
        self.lastSpeedTowardsTarget = 0
        self.targetBotID = self.id
        self.foodID_last = []
        self.distanceToTarget = 0
        self.followed = 0
        self.body = pymunk.Body()
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.found = 0
        self.shape.friction = 10

    removed = 0
    collision = False
    infraredRadius = 70
    radius = 0
    front_y_conf_val = 2
    moves = 0

    def drawKilobot(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (self.front_r, self.front_g, self.front_b), (int(self.front_x), int(self.front_y)),
                           self.front_radius)

    def drawFood(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)

    def refreshCoord(self):
        self.x = self.body.position[0]
        self.y = self.body.position[1]

    def setPositon(self, x, y):
        self.x = x
        self.y = y

        self.front_x = x
        self.front_y = y + self.front_y_conf_val

    def changeColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def changeColorKilobot(self, r, g, b):
        self.r = (255 / 7) * r
        self.g = (255 / 7) * g
        self.b = (255 / 7) * b

    def rotateKilobot(self, spinAngle):
        self.fi = self.fi + spinAngle

    def MotorsMoveKilobot(self, M1, M2, v):
        M_temp = M1 - M2

        self.fi = self.fi + M_temp * 0.015
        xSpeed = 55 * sin(radians(self.fi)) * v
        ySpeed = 55 * cos(radians(self.fi)) * v
        self.body.angular_velocity = M_temp
        self.body.velocity = (xSpeed, ySpeed)

        self.front_x = self.x + 0.5 * xSpeed
        self.front_y = self.y + 0.5 * ySpeed
>>>>>>> Stashed changes

    def calculateSpeedXY(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        return xSpeed, ySpeed

<<<<<<< Updated upstream
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
=======
    # predict collison between two kilobots for Motors movement
    def checkCollisionPrediction_Motors(self, X, Y, fi_temp, precison):
        return False

    def checkCollisionPrediction(self, X, Y, kilobot1, kilobot2):
        return False

    # predict collison between kilobot and borders for Motors movement
    def checkWallCollisionPrediction_Motors(self, resx, resy, fi_temp, precison):
        return False

    def isIdPresent(self, inID):
        for itr in self.inIRRangeKilobotID:
            if itr == inID:
                return True
        else:
            return False

    def isFoodIdPresent(self, inID):
        for itr in self.inIRRangeFoodID:
            if itr == inID:
                return True
        else:
            return False

    def detectKilobotsInIRRange(self, kilobotArray):
        for botItr in kilobotArray:
            xDif = fabs(self.front_x - botItr.x)
            yDif = fabs(self.front_y - botItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if botItr.id == self.id:
                continue
            elif Dif.real < 2 * self.infraredRadius:
                if not botItr.isFoodIdPresent(botItr.id):
                    IDandDistance = [botItr.id, round(Dif.real, 2)]
                    self.inIRRangeKilobotID.append(IDandDistance)

    def detectFoodsInIRRange(self, FoodsArray):
        for foodItr in FoodsArray:
            xDif = fabs(self.front_x - foodItr.x)
            yDif = fabs(self.front_y - foodItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < 2 * self.infraredRadius:
                if not foodItr.isIdPresent(foodItr.id):
                    IDandDistance = [foodItr.id, round(Dif.real, 2)]
                    self.inIRRangeFoodID.append(IDandDistance)

    def findClosestFood(self):
        if len(self.foodID_last) != 0:
            closest = self.foodID_last[0][1]
            closest_id = 0

            for food in range(0, len(self.foodID_last)):
                if self.foodID_last[food][1] < closest:
                    closest = self.foodID_last[food][1]
                    closest_id = food
            return closest_id
        else:
            return None

    def findLowerIDBot(self):
        for botID1 in self.inIRRangeKilobotID:
            if int(botID1[0]) < int(self.id):
                self.targetBotID = botID1[0]
                print(str(self.id) + "now follows" + str(self.targetBotID))
>>>>>>> Stashed changes

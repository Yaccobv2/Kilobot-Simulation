from cmath import sqrt
from math import fabs, pi, sin, cos, degrees, radians, exp
import pymunk

import pygame


def drawKilobots(kilobotArray, screen):
    for it in kilobotArray:
        it.drawKilobot(screen)


def drawFoods(kilobotArray, screen):
    for it in kilobotArray:
        it.drawFood(screen)


class Kilobot:

    def __init__(self, id, x, y, fi, r, g, b, radius):
        self.id = id
        self.index = id
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.fi = fi
        self.radius = radius
        ############################
        # detection of other kilobots
        self.inIRRangeKilobotID = []
        self.inIRRangeFoodID = []
        ############################
        # #front head
        self.front_x = x
        self.front_y = y + radius - 2
        self.front_radius = radius - 13
        self.front_r = 0
        self.front_g = 0
        self.front_b = 255
        ############################
        self.V = 0.5
        self.Fitness = 0
        ############################
        # PID
        self.pam = 0.0
        self.pamUchyb = 0.0
        self.P = 0
        self.I = 0
        self.D = 0
        self.avg_error = 0
        ############################
        #   physics engine
        self.body = pymunk.Body()
        self.body.position = (self.x, self.y)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.found = 0
        self.shape.friction = 10
        ############################
        
    removed = 0
    collision = False
    infraredRadius = 100
    radius = 0
    foodID_last = []
    front_y_conf_val = 2
    moves = 0
    bounced = False
    M1Motor_val = 0
    M2Motor_val = 0
    last_closestfood=0

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def StoreMotorsValue(self, M1, M2):
        self.M1Motor_val = M1
        self.M2Motor_val = M2

    def GetMotorsValue(self):
        return self.M1Motor_val, self.M2Motor_val

    def SetNewMotorsValue(self, M1, M2):
        self.M1Motor_val = M1
        self.M2Motor_val = M2

    def drawKilobot(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (self.front_r, self.front_g, self.front_b), (int(self.front_x), int(self.front_y)),
                           self.front_radius)

    def drawFood(self, screen):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x), int(self.y)), self.radius)

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

    def moveKilobot(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        self.x = self.x + xSpeed
        self.y = self.y + ySpeed

        self.front_x = self.front_x + xSpeed
        self.front_y = self.front_y + self.front_y_conf_val + ySpeed

    def rotateKilobot(self, spinAngle):
        self.fi = self.fi + spinAngle

    def createStticBody(self):
        self.body.position = (self.x, self.y)


    # def MotorsMoveKilobot(self, M1, M2, V):
    #     self.V = V
    #     M_temp = M1 - M2
    #     self.fi = self.fi + M_temp * 0.01
    #     xSpeed = sin(radians(self.fi))
    #     ySpeed = cos(radians(self.fi))
    #     self.x = self.x + xSpeed * self.V
    #     self.y = self.y + ySpeed * self.V
    #
    #     if M_temp != 0:
    #         self.front_x = self.x + xSpeed * 13
    #         self.front_y = self.y + ySpeed * 13
    #     else:
    #         self.front_x = self.front_x + xSpeed * V
    #         self.front_y = self.front_y + ySpeed * V
    def MotorsMoveKilobot(self, M1, M2, v):
        M_temp = M1 - M2

        self.fi = self.fi + M_temp * 0.01
        xSpeed = 55 * sin(radians(self.fi)) * v
        ySpeed = 55 * cos(radians(self.fi)) * v
        self.body.angular_velocity = M_temp
        self.body.velocity = (xSpeed, ySpeed)


        self.front_x = self.x + 0.5 * xSpeed
        self.front_y = self.y + 0.5 * ySpeed


    def refreshCoord(self):
        self.x = self.body.position[0]
        self.y = self.body.position[1]



    def simple_move(self, x, y):

        self.x = self.x + x
        self.y = self.y + y

        self.front_x = self.front_x + x
        self.front_y = self.front_y + y

    def calculateSpeedXY(self, speed):
        angle = self.fi * pi / 180
        xSpeed = sin(angle) * speed
        ySpeed = cos(angle) * speed
        return xSpeed, ySpeed

    # # predict collison between two kilobots for simple movement
    # def checkSingleCollisionPrediction(self, self_X, self_Y, X, Y):
    #     xSpeed, ySpeed = self.calculateSpeedXY(1)
    #     xDif = fabs(self_X - X)
    #     yDif = fabs(self_Y - Y)
    #     Dif = sqrt(xDif ** 2 + yDif ** 2)
    #     if Dif.real < 2 * self.radius + 1:
    #         return True
    #
    # # predict collison between kilobot and borders for simple movement
    # def checkWallCollisionPrediction(self, self_X, self_Y, resx, resy):
    #     if (self_X < self.radius + 1) | (self_Y < self.radius + 1) | (self_X > (resx - self.radius + 1)) | (
    #             self_Y > (resy - self.radius - 55 + 1)):
    #         return True
    #
    # # predict collison between two kilobots for rotation movement
    # def checkCollisionPrediction_Rotaton(self, X, Y, speed, fi_temp):
    #     fi_temp = self.fi + fi_temp
    #     angle = fi_temp * pi / 180
    #     xSpeed = sin(angle) * speed
    #     ySpeed = cos(angle) * speed
    #     x_temp = self.x + xSpeed
    #     y_temp = self.y + ySpeed
    #     xDif = fabs(x_temp - X)
    #     yDif = fabs(y_temp - Y)
    #     Dif = sqrt(xDif ** 2 + yDif ** 2)
    #     if Dif.real < 2 * self.radius + 1:
    #         return True
    #
    # # predict collison between kilobot and borders for rotation movement
    # def checkWallCollisionPrediction_Rotaton(self, resx, resy, speed, fi_temp):
    #     fi_temp = self.fi + fi_temp
    #     angle = fi_temp * pi / 180
    #     xSpeed = sin(angle) * speed
    #     ySpeed = cos(angle) * speed
    #     x_temp = self.x + xSpeed
    #     y_temp = self.y + ySpeed
    #     if (x_temp < self.radius + 1) | (y_temp < self.radius + 1) | (x_temp > (resx - self.radius + 1)) | (
    #             y_temp > (resy - self.radius - 55 + 1)):
    #         return True

    # chceck wall colisson
    def checkWallCollision(self, resx, resy):
        if (self.x < self.radius) | (self.y < self.radius) | (self.x > (resx - self.radius)) | (
                self.y > (resy - self.radius - 55)):
            return True

    def BounceIfWallCollision(self, resx, resy):
        if self.x < self.radius:
            self.x = self.x + 5
            self.front_x = self.front_x + 5
        if self.y < self.radius:
            self.y = self.y + 5
            self.front_y = self.front_y + 5
        if self.x > (resx - self.radius):
            self.x = self.x - 5
            self.front_x = self.front_x - 5
        if self.y > (resy - self.radius - 55):
            self.y = self.y - 5
            self.front_y = self.front_y - 5
        self.bounced = True

    def checkCollisionbetweenKilobots(self, X, Y):
        xDif = fabs(self.x - X)
        yDif = fabs(self.y - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * self.radius:
            return True

    # predict collison between two kilobots for Motors movement
    def checkCollisionPrediction_Motors(self, X, Y, fi_temp, precison):
        angle = self.fi + fi_temp
        xSpeed = sin(angle)
        ySpeed = cos(angle)
        x_temp = self.x + xSpeed * self.V
        y_temp = self.y + ySpeed * self.V
        xDif = fabs(x_temp - X)
        yDif = fabs(y_temp - Y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif.real < 2 * self.radius + precison:
            return True

    # predict collison between kilobot and borders for Motors movement
    def checkWallCollisionPrediction_Motors(self, resx, resy, fi_temp, precison):
        angle = self.fi + fi_temp
        xSpeed = sin(angle)
        ySpeed = cos(angle)
        x_temp = self.x + xSpeed * self.V
        y_temp = self.y + ySpeed * self.V
        if (x_temp < self.radius + precison) | (y_temp < self.radius + precison) | (
                x_temp > (resx - self.radius - precison)) | (
                y_temp > (resy - self.radius - 55 - precison)):
            return True

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
                    self.inIRRangeKilobotID.append(botItr.id)

    def detectFoodsInIRRange(self, FoodsArray):
        for foodItr in FoodsArray:
            xDif = fabs(self.x - foodItr.x)
            yDif = fabs(self.y - foodItr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif.real < 2 * self.infraredRadius:
                if not foodItr.isFoodIdPresent(foodItr.id):
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

    def calcPID(self, ref, meas, KP, KI, KD, ogrP, ogrN, delta):
        global pam
        uchyb = (ref - meas)
        wyP = uchyb * KP
        wyI = uchyb * KI * delta + self.pam
        if delta != 0:
            wyD = ((uchyb - self.pamUchyb) / delta) * KD
        else:
            wyD = ((uchyb - self.pamUchyb) / 1) * KD

        if wyI > ogrP:
            wyI = ogrP
        if wyI < ogrN:
            wyI = ogrN

        wy = wyP + wyI + wyD

        if wy > ogrP:
            wy = ogrP
        if wy < ogrN:
            wy = ogrN

        self.pam = wyI
        self.pamUchyb = uchyb

        return wy

    def calcPI(self, ref, meas, KP, KI, ogrP, ogrN, delta):
        global pam
        uchyb = (ref - meas)
        wyP = uchyb * KP
        wyI = uchyb * KI * delta + self.pam

        if wyI > ogrP:
            wyI = ogrP
        if wyI < ogrN:
            wyI = ogrN

        wy = wyP + wyI

        if wy > ogrP:
            wy = ogrP
        if wy < ogrN:
            wy = ogrN

        self.pam = wyI

        return wy

    def setPID(self, P, I, D):
        self.P = P
        self.I = I
        self.D = D

    def getPID(self):
        return self.P, self.I, self.D

    def savePID(self):
        f = open("PID_val.txt", "w")
        text = str(round(self.P, 2)) + "," + str(round(self.I, 2)) + "," + str(round(self.D, 2))
        f.write(str(text))
        f.close()

    def loadPID(self, idx):
        f = open("PID_val.txt", "r")
        text = f.readline()

        # conver to the list
        text = text.split(",")

        # convert each element as integers
        values = []
        for i in text:
            values.append(float(i))

        # if idx != 0:
        if idx>15:
            self.P = values[0]/idx
            self.I = values[1]/idx
            self.D = values[2]/idx
        else:
            self.P = values[0] + idx
            self.I = values[1] + idx
            self.D = values[2] + idx
        # else:
        #     self.P = values[0]
        #     self.I = values[1]
        #     self.D = values[2]



from math import fabs, sqrt
import random2
import pygame
import CreatingShapesAlgorithm
import kilobotClass
import pymunk
import invisibleWall
import numpy as np
import matplotlib.pyplot as plt
from timer import Timer
import math
import numpy as np
import Shapes

radiusInput = 15

resx = 1200
resy = 800


def gaussian(x, alpha, r):
    """
        Calculate gaussian function
        :param: x: input
        :param: alpha: expected value μ
        :param: r: variance σ2
        :return: output of gaussian function
    """
    return 1. / (math.sqrt(alpha ** math.pi)) * np.exp(-alpha * np.power((x - r), 2.))


def GetGenerationNumber():
    f = open("generation_num.txt", "r")
    gen = f.readline()
    f.close()
    return int(gen)


def SaveGenerationNumber(gen):
    f = open("generation_num.txt", "w")
    f.write(str(gen))
    f.close()


def clearPIDfile():
    open('PID_val.txt', 'w').close()


def checkPlacementCollision(array, X, Y):
    """
        Checks for collisions when placing a Kilobot
        :param: X: X coordinate of placed Kilobot
        :param: Y: Y coordinate of placed Kilobot
        :return: True/False
    """
    if len(array) == 0:
        return False
    else:
        for itr in array:
            xDif = fabs(X - itr.x)
            yDif = fabs(Y - itr.y)
            Dif = sqrt(xDif ** 2 + yDif ** 2)
            if Dif < 30:
                return True
        return False


def checkPlacementCollisionAndTagForRemoval(array, X, Y):
    """
        Checks for collisions when placing a Kilobot, tags collided ones for removal
        :param: array: Array of Kilobots
        :param: X: X coordinate of placed Kilobot
        :param: Y: Y coordinate of placed Kilobot
        :return: True/False
    """
    for itr in array:
        xDif = fabs(X - itr.x)
        yDif = fabs(Y - itr.y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif < 30:
            itr.removed = 1
            return True
    return False


def isIdPresent(inID, IDIRArray):
    for itr in IDIRArray:
        if itr == inID:
            return True
    else:
        return False


# detect kilobots in range
def detectKilobotsInIRRange(kilobotArray):
    """
        Detects Kilobots in IR Range
        :param: kilobotArray: Array of Kilobots
        :return: none
    """
    for i1 in kilobotArray:
        i1.detectKilobotsInIRRange(kilobotArray)


# detect food in range
def detectFoodsInIRRange(kilobotArray, FoodArray):
    """
        Detects Food in IR Range
        :param: kilobotArray: Array of Kilobots
        :param: FoodArray: Array of Food
        :return: none
    """
    for i1 in kilobotArray:
        i1.detectFoodsInIRRange(FoodArray)


# copy range list to check if kilobot is getting closer
def FoodsInIRRange_last(kilobotArray):
    """
        Copies list of static kilobots in range to check if kilobot is getting closer to Food
        :param: kilobotArray: Array of static Kilobots
        :return: none
    """
    for i1 in kilobotArray:
        i1.foodID_last = i1.inIRRangeFoodID.copy()


# copy range list to check if kilobot is getting closer
def KilobotsInIRRange_last(kilobotArray):
    """
        Copies list of kilobots in range to check if kilobot is getting closer to Food
        :param: kilobotArray: Array of Kilobots
        :return: none
    """
    for i1 in kilobotArray:
        i1.kilobotID_last = i1.inIRRangeKilobotID.copy()


# get random int number between 0 and 100
def getRandSpin():
    """
        Generates random value in range 0-100
        :param: none
        :return: Random value in range 0-100
    """
    return random2.randint(0, 100)


# get random int number between 0 and 255
def getRandColor():
    """
        Generates random value in range 0-255
        :param: none
        :return: Random value in range 0-255
    """
    return random2.randint(0, 255)


def getRandBool():
    """
        Generates random bool value
        :param: none
        :return: Random bool value
    """
    return random2.randint(0, 1)


def reddrawWindow(screen):
    screen.fill((255, 255, 255))
    return screen


def getRandX():
    """
        Generates random X coordinate in range 400-1000
        :param: none
        :return: Random X coordinate in range 400-1000
    """
    return random2.randint(400, 1000)


def getRandY():
    """
        Generates random Y coordinate in range 400-700
        :param: none
        :return: Random Y coordinate in range 400-700
    """
    return random2.randint(400, 700)


def addShapeEvent(pos, radius):
    """
        Creates shape object for createshapesalgorithm
        :param: radius: radius of this shape
        :return: shape: returns created object
    """
    shape = Shapes.Shape(1, pos[0], pos[1], 255, 124, 150, radius)
    return shape


def addKilobotEvent(pos, kilobots, kilobotID, kilobotsNumber, space):
    """
        Creates kilobot and adds it to workspace
        :param: pos: x-y coordinates
        :param: kilobots: Array of existing Kilobots
        :param: kilobotID: Kilobots ID
        :param: kilobotsNumber: Kilobots count
        :param: space: Physical space
        :return: kilobots: Array of existing Kilobots
        :return: kilobotID: Kilobots ID
        :return: kilobotsNumber: Kilobots count
        :return: space: Physical space

    """
    if not checkPlacementCollision(kilobots, pos[0], pos[1]):
        kilobot = kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput)
        space.add(kilobot.body, kilobot.shape)
        kilobots.append(kilobot)

        kilobotID += 1
        kilobotsNumber += 1
    return kilobots, kilobotID, kilobotsNumber, space


def addKilobotEventAI(pos, kilobots, kilobotID, kilobotsNumber, space):
    """
        Creates kilobot for AI algorithm and adds it to workspace
        :param: pos: x-y coordinates
        :param: kilobots: Array of existing Kilobots
        :param: kilobotID: Kilobots ID
        :param: kilobotsNumber: Kilobots count
        :param: space: Physical space
        :return: kilobots: Array of existing Kilobots
        :return: kilobotID: Kilobots ID
        :return: kilobotsNumber: Kilobots count
        :return: space: Physical space
    """
    kilobot = kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput)
    space.add(kilobot.body, kilobot.shape)
    kilobots.append(kilobot)

    kilobotID += 1
    kilobotsNumber += 1
    return kilobots, kilobotID, kilobotsNumber, space


def addFoodEventAI(pos, FoodArray, FoodID, r, g, b, space):
    """
        Adds food for AI algorithm
        :param: pos: x-y coordinates
        :param: FoodArray: Array of existing Kilobots
        :param: FoodID: Kilobots ID
        :param: r: RGB r value
        :param: g: RGB g value
        :param: b: RGB b value
        :param: space: Physical space
        :return: FoodArray: Array of existing foods
        :return: space: Physical space
    """
    food = kilobotClass.Kilobot(FoodID, pos[0], pos[1], r, g, b, 0, radiusInput)
    space.add(food.body, food.shape)
    food.createStticBody()
    FoodArray.append(food)
    return FoodArray, space


def removeKilobotEvent(pos, kilobots, kilobotID, kilobotsNumber):
    """
        Removes kilobots from workspace
        :param: pos: x-y coordinates
        :param: kilobots: Array of existing Kilobots
        :param: kilobotID: Kilobots ID
        :param: kilobotsNumber: Kilobots count
        :return: kilobots: Array of existing Kilobots
        :return: kilobotsNumber: Array of existing Kilobotss
    """
    for x in range(len(kilobots)):
        if kilobots[x].removed == 1:
            print("Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(
                kilobots[x].y))
            kilobots.pop(x)
            kilobotsNumber -= 1
            return kilobots, kilobotsNumber
            break


def addFoodEvent(pos, FoodArray, FoodID, FoodNumber, r, g, b, space):
    """
        Adds food to workspace
        :param: pos: x-y coordinates
        :param: FoodArray: Array of existing Foods
        :param: FoodID: Food ID
        :param: FoodNumber: Foods count
        :param: r: RGB r value
        :param: g: RGB g value
        :param: b: RGB b value
        :param: space: Physical space
        :return: FoodArray: Array of existing Foods
        :return: FoodID: Food ID
        :return: FoodNumber: Foods count
        :return: space: Physical space
    """
    if not checkPlacementCollision(FoodArray, pos[0], pos[1]):
        food = kilobotClass.Kilobot(FoodID, pos[0], pos[1], r, g, b, 0, radiusInput)
        space.add(food.body, food.shape)
        food.createStticBody()
        FoodArray.append(food)

    FoodID += 1
    FoodNumber += 1
    return FoodArray, FoodID, FoodNumber, space


def resetEvent(kilobots, FoodArray, t, t_pause):
    print('clicked reset button')
    """
        Resets simulation after clicking reset button
        :param: kilobots: Array of existing Kilobots
        :param: FoodArray: Array of existing Foods
        :param: t: Objects which contains simulation time
        :param: t_pause: Objects which contains pause time 
        :return: t: Objects which contains simulation time
        :return: enable: Flag enabling movement
        :return: t_pause: Objects which contains pause time 
        :return: kilobots: Array of existing Kilobots
        :return: FoodArray: Array of existing Foods
        :return: space: Physical space
        :return: kilobotID: Kilobots ID
        :return: kilobotsNumber: Kilobots count
        :return: buildWalls: If = 0 then walls are built
    """
    kilobots.clear()
    FoodArray.clear()
    space = pymunk.Space()
    kilobotID = 0
    kilobotsNumber = 0
    SpecialkilobotID = 0
    SpecialkilobotsNumber = 0
    buildWalls = 0
    enable = False
    if t.state():
        t.stop()
        return t, enable, t_pause, kilobots, FoodArray, space, kilobotID, kilobotsNumber, buildWalls

    if t_pause.state():
        t_pause.stop()
        return t, enable, t_pause, kilobots, FoodArray, space, kilobotID, kilobotsNumber, buildWalls


def startEvent(t, t_pause):
    """
        Starts simulation after clicking Start button
        :param: t: Objects which contains simulation time
        :param: t_pause: Objects which contains pause time
        :return: t: Objects which contains simulation time
        :return: enable: Flag enabling movement
        :return: t_pause: Objects which contains pause time
    """
    print('Clicked start button')
    enable = True
    if not t_pause.state() and not t.state():
        t.start()
        return t, enable, t_pause
    else:
        if t_pause.state():
            t_pause.stop()
            return t, enable, t_pause


def startEventmanual(t, t_pause):
    enable = True
    if not t_pause.state() and not t.state():
        t.start()
        return t, enable, t_pause
    else:
        if t_pause.state():
            t_pause.stop()
            return t, enable, t_pause


def pauseEvent(pos, t_pause):
    print('Clicked start button')
    enable = False
    if not t_pause.state():
        t_pause.start()
        return enable, t_pause


def pasueTimer(t_pause, t):
    if t_pause.state():
        t.pause(t_pause.read_time())
        return t


def inputEventHandler(t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, startButton,
                      pauseButton, resetButton, space, currentAlghoritm, buildWalls):
    global running
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()

                if (mousepos[0] > radiusInput) & (mousepos[1] > radiusInput) & (mousepos[0] < (resx - radiusInput)) & (
                        mousepos[1] < (resy - radiusInput - 55)):
                    kilobots, kilobotID, kilobotsNumber, space = addKilobotEvent(mousepos, kilobots, kilobotID,
                                                                                 kilobotsNumber, space)
                    # kilobots, kilobotID, kilobotsNumber,space = addKilobotEvent((550, 450), kilobots, kilobotID, kilobotsNumber,space)
                    # kilobots, kilobotID, kilobotsNumber, space = addKilobotEvent((370, 400), kilobots, kilobotID,
                    # kilobotsNumber, space)

                if resetButton.isOver(mousepos):
                    try:
                        t, enable, t_pause, kilobots, Foods, space, kilobotID, kilobotsNumber, buildWalls = resetEvent(
                            kilobots, Foods, t, t_pause)
                    except:
                        print("error")

                if startButton.isOver(mousepos):
                    try:
                        t, enable, t_pause = startEvent(t, t_pause)
                    except:
                        print("error")

                if pauseButton.isOver(mousepos):
                    try:
                        enable, t_pause = pauseEvent(mousepos, t_pause)
                    except:
                        print("error")

            if event.button == 3:
                mousepos = pygame.mouse.get_pos()

                if checkPlacementCollisionAndTagForRemoval(kilobots, mousepos[0], mousepos[1]):
                    kilobots, kilobotsNumber = removeKilobotEvent(mousepos, kilobots, kilobotID, kilobotsNumber)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mousepos = pygame.mouse.get_pos()

                if (mousepos[0] > radiusInput) & (mousepos[1] > radiusInput) & (mousepos[0] < (resx - radiusInput)) & (
                        mousepos[1] < (resy - radiusInput - 55)):
                    Foods, FoodID, FoodNumber, space = addFoodEvent(mousepos, Foods, FoodID, FoodNumber, 0, 128, 0,
                                                                    space)
            if event.key == pygame.K_0:
                currentAlghoritm = 0
            if event.key == pygame.K_1:
                currentAlghoritm = 1
            if event.key == pygame.K_2:
                currentAlghoritm = 2

    return t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, space, currentAlghoritm, buildWalls


def BuildWall(x, y, xSize, ySize, space):
    wallTemp = invisibleWall.InvisibleWall(x, y, xSize, ySize)
    space.add(wallTemp.body, wallTemp.shape)
    return space


def buildWalls(screen, resx, resy, space):
    space = BuildWall(0, 0, resx * 2, 10, space)
    space = BuildWall(0, resy - 27, resx * 2, 50, space)
    space = BuildWall(0, 0, 20, resy * 2, space)
    space = BuildWall(resx, 0, 20, resy * 2, space)
    return space


def drawWalls(screen, resx, resy):
    pygame.draw.rect(screen, (255, 255, 255), [0, 0, resx, 1])
    pygame.draw.rect(screen, (255, 255, 255), [0, resy - 50, resx, 50])
    pygame.draw.rect(screen, (255, 255, 255), [0, 0, 10, resy])
    pygame.draw.rect(screen, (255, 255, 255), [resx - 10, 0, 10, resy])

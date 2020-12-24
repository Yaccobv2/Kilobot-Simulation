from math import fabs, sqrt
import random2
import pygame
import neat
import os
import time

from button import button
import kilobotClass
from timer import Timer
import Movement


radiusInput = 15

resx = 1200
resy = 800


def checkPlacementCollision(array, X, Y):
    for itr in array:
        xDif = fabs(X - itr.x)
        yDif = fabs(Y - itr.y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif < 30:
            return True
    return False


def checkPlacementCollisionAndTagForRemoval(array, X, Y):
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
    for i1 in kilobotArray:
        i1.detectKilobotsInIRRange(kilobotArray)


# detect food in range
def detectFoodsInIRRange(kilobotArray, FoodArray):
    for i1 in kilobotArray:
        i1.detectFoodsInIRRange(FoodArray)


# copy range list to check if kilobot is getting closer
def FoodsInIRRange_last(kilobotArray):
    for i1 in kilobotArray:
        i1.foodID_last = i1.inIRRangeFoodID.copy()


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(0, 100)


# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


def getRandBool():
    return random2.randint(0, 1)


def reddrawWindow(screen):
    screen.fill((255, 255, 255))
    return screen


def addKilobotEvent(pos, kilobots, kilobotID):
    # print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    # if (pos[0] > radiusInput) & (pos[1] > radiusInput) & (pos[0] < (resx - radiusInput)) & (
    #         pos[1] < (resy - radiusInput - 55)):
    #     if not checkPlacementCollision(kilobots, pos[0], pos[1]):
    # kilobots.append(kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput))
    # print("Drew kilobot " + str(kilobotID) + " in x: " + str(pos[0]) + " y: " + str(pos[1]))
    kilobot_tmp = kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput)
    # kilobotID = kilobotID + 1
    # kilobotsNumber = kilobotsNumber + 1
    return kilobot_tmp


def removeKilobotEvent(pos, kilobots):
    global kilobotsNumber, kilobotID
    print("Right mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if checkPlacementCollisionAndTagForRemoval(kilobots, pos[0], pos[1]):
        for x in range(len(kilobots)):
            if kilobots[x].removed == 1:
                print("Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(
                    kilobots[x].y))
                kilobots.pop(x)
                kilobotsNumber = kilobotsNumber - 1
                break


def addSpecialKilobotEvent(pos, FoodArray, kilobotID, r, g, b):
    # print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    # if (pos[0] > radiusInput) & (pos[1] > radiusInput) & (pos[0] < (resx - radiusInput)) & (
    #         pos[1] < (resy - radiusInput - 55)):
    #     if not checkPlacementCollision(FoodArray, pos[0], pos[1]):
    # FoodArray.append(kilobotClass.Kilobot(SpecialkilobotID, pos[0], pos[1], 0, 0, 128, 0, radiusInput))
    # print("Drew kilobot " + str(SpecialkilobotID) + " in x: " + str(pos[0]) + " y: " + str(pos[1]))
    food_tmp = kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, r, g, b, radiusInput)
    # SpecialkilobotID = SpecialkilobotID + 1
    # SpecialkilobotsNumber = SpecialkilobotsNumber + 1
    return food_tmp


def resetEvent(pos, kilobots, FoodArray, t, t_pause):
    global kilobotID, kilobotsNumber, enable, resetButton, SpecialkilobotID, SpecialkilobotsNumber
    global pause
    if resetButton.isOver(pos):
        print('clicked reset button')
        kilobots.clear()
        FoodArray.clear()
        kilobotID = 0
        kilobotsNumber = 0
        SpecialkilobotID = 0
        SpecialkilobotsNumber = 0
        enable = False
        if t.state():
            t.stop()
            return t, enable, t_pause, kilobots, FoodArray

        if t_pause.state():
            t_pause.stop()
            return t, enable, t_pause, kilobots, FoodArray


def startEvent(pos, startButton, t, t_pause):
    global enable
    global pause
    if startButton.isOver(pos):
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


def pauseEvent(pos, t_pause, pauseButton):
    if pauseButton.isOver(pos):
        print('Clicked start button')
        enable = False
        if not t_pause.state():
            t_pause.start()
            return enable, t_pause


def pasueTimer(t_pause, t):
    if t_pause.state():
        t.pause(t_pause.read_time())
        return t


def inputEventHandler():
    global running
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()
                addKilobotEvent(mousepos)

                resetEvent(mousepos)

                startEvent(mousepos)

                pauseEvent(mousepos)

            if event.button == 3:
                mousepos = pygame.mouse.get_pos()
                removeKilobotEvent(mousepos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mousepos = pygame.mouse.get_pos()
                addSpecialKilobotEvent(mousepos)


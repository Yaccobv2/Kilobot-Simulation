from math import fabs, sqrt
import random2
import pygame

from button import button
import kilobotClass
from timer import Timer
import Movement

# inicjalizacja biblioteki
pygame.init()
radiusInput = 15

resx = 600
resy = 655


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
    return random2.randint(-1, 1)


# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


def getRandBool():
    return random2.randint(0, 1)


def reddrawWindow():
    screen.fill((255, 255, 255))


# tworzenie ekranu
screen = pygame.display.set_mode((resx, resy))

# deklaracja tablicy kilobotow
kilobotsMaxAmount = 100
kilobots = []
kilobotID = 0
kilobotsNumber = 0
SpecialkilobotID, SpecialkilobotsNumber = 0, 0
startTime = 0
enable = False
Specialkolobot = []


def addKilobotEvent(pos):
    global kilobotID, kilobotsNumber
    print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if (pos[0] > radiusInput) & (pos[1] > radiusInput) & (pos[0] < (resx - radiusInput)) & (
            pos[1] < (resy - radiusInput - 55)):
        if not checkPlacementCollision(kilobots, pos[0], pos[1]):
            kilobots.append(kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput))
            print("Drew kilobot " + str(kilobotID) + " in x: " + str(pos[0]) + " y: " + str(pos[1]))
            kilobotID = kilobotID + 1
            kilobotsNumber = kilobotsNumber + 1


def removeKilobotEvent(pos):
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


def addSpecialKilobotEvent(pos):
    global SpecialkilobotID, SpecialkilobotsNumber
    print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if (pos[0] > radiusInput) & (pos[1] > radiusInput) & (pos[0] < (resx - radiusInput)) & (
            pos[1] < (resy - radiusInput - 55)):
        if not checkPlacementCollision(Specialkolobot, pos[0], pos[1]):
            Specialkolobot.append(kilobotClass.Kilobot(SpecialkilobotID, pos[0], pos[1], 0, 0, 128, 0, radiusInput))
            print("Drew kilobot " + str(SpecialkilobotID) + " in x: " + str(pos[0]) + " y: " + str(pos[1]))
            SpecialkilobotID = SpecialkilobotID + 1
            SpecialkilobotsNumber = SpecialkilobotsNumber + 1


def resetEvent(pos):
    global kilobotID, kilobotsNumber, enable, resetButton, SpecialkilobotID, SpecialkilobotsNumber
    global pause
    if resetButton.isOver(pos):
        print('clicked reset button')
        kilobots.clear()
        Specialkolobot.clear()
        kilobotID = 0
        kilobotsNumber = 0
        SpecialkilobotID = 0
        SpecialkilobotsNumber = 0

        if t.state():
            t.stop()

        if t_pause.state():
            t_pause.stop()

        enable = False


def startEvent(pos):
    global enable
    global pause
    if startButton.isOver(pos):
        print('Clicked start button')

        if not t_pause.state() and not t.state():
            t.start()
        else:
            if t_pause.state():
                t_pause.stop()

        enable = True


def pauseEvent(pos):
    global enable
    global pause
    if pauseButton.isOver(pos):
        print('Clicked start button')

        if not t_pause.state():
            t_pause.start()

        enable = False


def pasueTimer():
    if t_pause.state():
        t.pause(t_pause.read_time())


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


# tworzenie przycisku reset
resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

# glowna pętla
running = True
t = Timer()
t_pause = Timer()
while running:
    screen.fill((255, 255, 255))
    # random movement
    inputEventHandler()

    # update list of food in range
    for itr in kilobots:
        itr.inIRRangeKilobotID.clear()
        itr.inIRRangeFoodID.clear()

    detectFoodsInIRRange(kilobots, Specialkolobot)
    detectKilobotsInIRRange(kilobots)

    for itr in kilobots:
        print(str(itr.id) + ":" + str(itr.inIRRangeFoodID))
        print(str(itr.id) + ":" + str(itr.inIRRangeKilobotID))

    Movement.kilobotsMovement(enable, kilobots, resx, resy, screen)

    FoodsInIRRange_last(kilobots)
    kilobotClass.drawKilobots(kilobots, screen)
    kilobotClass.drawKilobots(Specialkolobot, screen)

    pasueTimer()

    numberView.text = str(kilobotsNumber)
    timeView.text = str(t.read_time())
    resetButton.draw(screen)
    startButton.draw(screen)
    pauseButton.draw(screen)
    numberView.draw(screen)
    timeView.draw(screen)

    pygame.display.update()

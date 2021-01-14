from math import fabs, sqrt
import random2
import pygame
<<<<<<< Updated upstream
import kilobotClass
from button import button
=======
import pymunk
import invisibleWall

from button import button
import kilobotClass
from timer import Timer
import Movement
>>>>>>> Stashed changes

# inicjalizacja biblioteki
pygame.init()
promienInput = 15

resx = 1200
resy = 800
walls = []

clock = pygame.time.Clock()



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


<<<<<<< Updated upstream
# check collison between the kilobot and array of kilobots
def checkCollisionLoop(kilobot, kilobots_array_temp, x_temp, y_temp, resx, resy):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkSingleCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, it.x, it.y, promienInput):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
        if kilobot.checkWallCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, resx, resy, promienInput):
            print("Kilobot " + str(it.id) + " collided with a wall")
=======
def isIdPresent(inID, IDIRArray):
    for itr in IDIRArray:
        if itr == inID:
>>>>>>> Stashed changes
            return True


<<<<<<< Updated upstream
def kilobotsMovement(enableTag, kilobotsArray, resx, resy):
    if enableTag:
        for it in kilobotsArray:
            forward = 1
            rotation = 0
            if getRandBool():
                rotation = getRandSpin()

            if not checkCollisionLoop(it, kilobotsArray, forward, rotation, resx, resy):
                it.moveKilobot(forward)
            else:
                it.isStuck = 1
            it.drawKilobot(screen, promienInput)
            it.rotateKilobot(5 * rotation)
=======
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
>>>>>>> Stashed changes


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)


def getRandBool():
    return random2.randint(0, 1)


def reddrawWindow():
    screen.fill((255, 255, 255))


# tworzenie ekranu
screen = pygame.display.set_mode((resx, resy))

# deklaracja tablicy kilobotow
kilobotsMaxAmount = 100;
kilobots = []
<<<<<<< Updated upstream
kilobotID = 0;
kilobotsNumber = 0;
enable = False;
=======
kilobotID = 0
kilobotsNumber = 0
SpecialkilobotID, SpecialkilobotsNumber = 0, 0
startTime = 0
enable = False
FoodArray = []
>>>>>>> Stashed changes


def addKilobotEvent(pos):
    global kilobotID, kilobotsNumber
    print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if (pos[0] > promienInput) & (pos[1] > promienInput) & (pos[0] < (resx - promienInput)) & (
            pos[1] < (resy - promienInput - 55)):
        if not checkPlacementCollision(kilobots, pos[0], pos[1]):
<<<<<<< Updated upstream
            kilobots.append(kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 255, 0, 0))
=======
            botTemp = kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput)
            space.add(botTemp.body, botTemp.shape)
            kilobots.append(botTemp)
>>>>>>> Stashed changes
            print("Drew kilobot " + str(kilobotID) + " in x: " + str(pos[0]) + " y: " + str(pos[1]))
            kilobotID = kilobotID + 1
            kilobotsNumber = kilobotsNumber + 1

<<<<<<< Updated upstream
def removeKilobotEvent(pos):
=======

def BuildWall(x, y, xSize, ySize):
    wallTemp = invisibleWall.InvisibleWall(x, y, xSize, ySize)
    space.add(wallTemp.body, wallTemp.shape)



def buildWalls(screen, resx, resy):
    BuildWall(0, 0, resx*2, 10)
    BuildWall(0, resy-27, resx*2, 50)
    BuildWall(0, 0, 20, resy*2)
    BuildWall(resx, 0, 20, resy*2)


def drawWalls(screen, resx, resy):
    pygame.draw.rect(screen, (255, 0, 122), [0, 0, resx, 1])
    pygame.draw.rect(screen, (255, 0, 122), [0, resy - 50, resx, 50])
    pygame.draw.rect(screen, (255, 0, 122), [0, 0, 10, resy])
    pygame.draw.rect(screen, (255, 0, 122), [resx - 10, 0, 10, resy])


def carryKilobotEvent(pos):
>>>>>>> Stashed changes
    global kilobotsNumber, kilobotID
    print("Right mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if checkPlacementCollisionAndTagForRemoval(kilobots, pos[0], pos[1]):
        for x in range(len(kilobots)):
            if kilobots[x].removed == 1:
                print(
                    "Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(kilobots[x].y))
                kilobots.pop(x)
                kilobotsNumber = kilobotsNumber - 1
                break


<<<<<<< Updated upstream
def resetEvent(pos):
    global kilobotID, kilobotsNumber, enable, resetButton
=======
def removeKilobotEvent(pos):
    global kilobotsNumber, kilobotID
    if checkPlacementCollisionAndTagForRemoval(kilobots, pos[0], pos[1]):
        for x in range(len(kilobots)):
            if kilobots[x].removed == 1:
                print(
                    "Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(kilobots[x].y))
                kilobots.pop(x)
                kilobotsNumber = kilobotsNumber - 1
                break




def resetEvent(pos, physicalSpace):
    global kilobotID, kilobotsNumber, enable, resetButton, SpecialkilobotID, SpecialkilobotsNumber
    global pause
>>>>>>> Stashed changes
    if resetButton.isOver(pos):
        print('clicked reset button')
        space = pymunk.Space()
        kilobots.clear()
        FoodArray.clear()
        kilobotID = 0
        kilobotsNumber = 0
<<<<<<< Updated upstream
        enable = False
=======
        print(len(space.bodies))
        if t.state():
            t.stop()

        if t_pause.state():
            t_pause.stop()
>>>>>>> Stashed changes


def startEvent(pos):
    global enable
    if startButton.isOver(pos):
        print('Clicked start button')
<<<<<<< Updated upstream
=======

        if not t_pause.state() and not t.state():
            t.start()
        else:
            if t_pause.state():
                t_pause.stop()

>>>>>>> Stashed changes
        enable = True


def pauseEvent(pos):
    global enable
    if pauseButton.isOver(pos):
        print('Clicked start button')
        enable = False

<<<<<<< Updated upstream
=======

def pasueTimer():
    if t_pause.state():
        t.pause(t_pause.read_time())


>>>>>>> Stashed changes
def inputEventHandler():
    global running
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()
                addKilobotEvent(mousepos)

                resetEvent(mousepos, space)

                startEvent(mousepos)

                pauseEvent(mousepos)

            if event.button == 3:
                mousepos = pygame.mouse.get_pos()
                removeKilobotEvent(mousepos)


# tworzenie przycisku reset
resetButton = button((255, 0, 0), resx - 100, resy - 50, 100, 50, 'Reset', True)
startButton = button((0, 255, 0), 0, resy - 50, 100, 50, 'Start', True)
pauseButton = button((0, 0, 255), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)

# glowna pętla
running = True
<<<<<<< Updated upstream
while running:

    screen.fill((255, 255, 255))
    # random movement
    kilobotsMovement(enable, kilobots, resx, resy)
    kilobotClass.drawKilobots(kilobots, screen, promienInput)

    inputEventHandler()
=======
t = Timer()
t_pause = Timer()
space = pymunk.Space()
clock = pygame.time.Clock()
countdown = 0
wallsBuilt = 0

while running:
    clock.tick(120)
    screen.fill((255, 255, 255))
    # random movement
    inputEventHandler()

    if wallsBuilt == 0:
        buildWalls(screen, resx, resy)
        wallsBuilt = 1

    drawWalls(screen, resx, resy)

    # update list of food in range
    for itr in kilobots:
        itr.inIRRangeKilobotID.clear()
        itr.inIRRangeFoodID.clear()
        itr.targetBotID = itr.id
        print(str(itr.id) + " " + str(itr.targetBotID))
        itr.refreshCoord()

    detectFoodsInIRRange(kilobots, FoodArray)
    detectKilobotsInIRRange(kilobots)

    Movement.kilobotsMovementSnake(enable, kilobots, FoodArray, resx, resy, screen)

    space.step(1 / 50)
    FoodsInIRRange_last(kilobots)
    clock.tick(120)

    pasueTimer()
>>>>>>> Stashed changes

    kilobotClass.drawKilobots(kilobots, screen)
    kilobotClass.drawFoods(FoodArray, screen)
    numberView.text = str(kilobotsNumber)
    resetButton.draw(screen)
    startButton.draw(screen)
    pauseButton.draw(screen)
    numberView.draw(screen)

    pygame.display.update()

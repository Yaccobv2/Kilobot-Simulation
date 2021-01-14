from math import fabs, sqrt
import random2
import pygame
import CreatingShapesAlgorithm
import kilobotClass
import pymunk
import invisibleWall

radiusInput = 15

resx = 1200
resy = 800





def GetGenerationNumber():
    f = open("generation_num.txt", "r")
    gen=f.readline()
    f.close()
    return int(gen)

def SaveGenerationNumber(gen):
    f = open("generation_num.txt", "w")
    f.write(str(gen))
    f.close()


def checkPlacementCollision(array, X, Y):
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

def getRandX():
    return random2.randint(400, 1000)

def getRandY():
    return random2.randint(400, 700)


def addKilobotEvent(pos, kilobots, kilobotID, kilobotsNumber,space):
    if not checkPlacementCollision(kilobots, pos[0], pos[1]):

        kilobot=kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput)
        space.add(kilobot.body, kilobot.shape)
        kilobots.append(kilobot)

        kilobotID += 1
        kilobotsNumber += 1
    return kilobots, kilobotID, kilobotsNumber,space

def addKilobotEventAI(pos, kilobots, kilobotID, kilobotsNumber):

    kilobots.append(kilobotClass.Kilobot(kilobotID, pos[0], pos[1], 0, 124, 252, 0, radiusInput))

    kilobotID += 1
    kilobotsNumber += 1
    return kilobots, kilobotID, kilobotsNumber

def addFoodEventAI(pos, FoodArray, FoodID, r, g, b):
    FoodArray.append(kilobotClass.Kilobot(FoodID, pos[0], pos[1], r, g, b, 0, radiusInput))
    return FoodArray


def removeKilobotEvent(pos, kilobots, kilobotID, kilobotsNumber):

    for x in range(len(kilobots)):
        if kilobots[x].removed == 1:
            print("Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(
                kilobots[x].y))
            kilobots.pop(x)
            kilobotsNumber -= 1
            return kilobots, kilobotsNumber
            break


def addFoodEvent(pos, FoodArray, FoodID, FoodNumber, r, g, b,space):

    if not checkPlacementCollision(FoodArray, pos[0], pos[1]):
        food = kilobotClass.Kilobot(FoodID, pos[0], pos[1], r, g, b, 0, radiusInput)
        space.add(food.body, food.shape)
        food.createStticBody()
        FoodArray.append(food)

    FoodID += 1
    FoodNumber += 1
    return FoodArray, FoodID, FoodNumber,space


def resetEvent(pos, kilobots, FoodArray, t, t_pause):
    print('clicked reset button')
    kilobots.clear()
    FoodArray.clear()
    space = pymunk.Space()
    kilobotID = 0
    kilobotsNumber = 0
    SpecialkilobotID = 0
    SpecialkilobotsNumber = 0
    enable = False
    if t.state():
        t.stop()
        return t, enable, t_pause, kilobots, FoodArray,space

    if t_pause.state():
        t_pause.stop()
        return t, enable, t_pause, kilobots, FoodArray,space


def startEvent(pos, t, t_pause):
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
                      pauseButton, resetButton,space):
    global running
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mousepos = pygame.mouse.get_pos()

                if (mousepos[0] > radiusInput) & (mousepos[1] > radiusInput) & (mousepos[0] < (resx - radiusInput)) & (
                        mousepos[1] < (resy - radiusInput - 55)):
                    kilobots, kilobotID, kilobotsNumber,space = addKilobotEvent(mousepos, kilobots, kilobotID, kilobotsNumber,space)

                if resetButton.isOver(mousepos):
                    t, enable, t_pause, kilobots, FoodArray,space = resetEvent(mousepos, kilobots, Foods, t, t_pause)

                if startButton.isOver(mousepos):
                    t, enable, t_pause = startEvent(mousepos, t, t_pause)

                if pauseButton.isOver(mousepos):
                    enable, t_pause = pauseEvent(mousepos, t_pause)

            if event.button == 3:
                mousepos = pygame.mouse.get_pos()

                if checkPlacementCollisionAndTagForRemoval(kilobots, mousepos[0], mousepos[1]):
                    kilobots, kilobotsNumber = removeKilobotEvent(mousepos, kilobots, kilobotID, kilobotsNumber)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mousepos = pygame.mouse.get_pos()

                if (mousepos[0] > radiusInput) & (mousepos[1] > radiusInput) & (mousepos[0] < (resx - radiusInput)) & (
                        mousepos[1] < (resy - radiusInput - 55)):
                    Foods, FoodID, FoodNumber,space = addFoodEvent(mousepos, Foods, FoodID, FoodNumber, 0, 128, 0,space)

    return t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber,space


def BuildWall(x, y, xSize, ySize, space):
    wallTemp = invisibleWall.InvisibleWall(x, y, xSize, ySize)
    space.add(wallTemp.body, wallTemp.shape)
    return space



def buildWalls(screen, resx, resy,space):
    space=BuildWall(0, 0, resx*2, 10,space)
    space=BuildWall(0, resy-27, resx*2, 50,space)
    space=BuildWall(0, 0, 20, resy*2,space)
    space=BuildWall(resx, 0, 20, resy*2,space)
    return space


def drawWalls(screen, resx, resy):
    pygame.draw.rect(screen, (255, 0, 122), [0, 0, resx, 1])
    pygame.draw.rect(screen, (255, 0, 122), [0, resy - 50, resx, 50])
    pygame.draw.rect(screen, (255, 0, 122), [0, 0, 10, resy])
    pygame.draw.rect(screen, (255, 0, 122), [resx - 10, 0, 10, resy])
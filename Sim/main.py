from math import fabs, sqrt
import random2
import pygame

from button import button
import kilobotClass
from timer import Timer

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


# check collison between the kilobot and array of kilobots/borders for simple movement
def checkCollisionLoop(kilobot, kilobots_array_temp, resx, resy, x_temp, y_temp, ):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkSingleCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, it.x, it.y):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, resx, resy):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# check collison between the kilobot and array of kilobots/borders for teleport
def checkCollisionLoop_tp(kilobot, kilobots_array_temp, resx, resy, x_tp, y_tp):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkSingleCollisionPrediction(x_tp, y_tp, it.x, it.y):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction(x_tp, y_tp, resx, resy):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")

        return True


def isIdPresent(inID, IDIRArray):
    for itr in IDIRArray:
        if itr == inID:
            return True
    else:
        return False


def detectKilobotsInIRRange(kilobotArray):
    for i1 in range(0, len(kilobotArray), 1):
        for i2 in range(0, len(kilobotArray), 1):
            if not kilobotArray[i1].id == kilobotArray[i2].id:
                xDif = fabs(kilobotArray[i1].x - kilobotArray[i2].x)
                yDif = fabs(kilobotArray[i1].y - kilobotArray[i2].y)
                Dif = sqrt(xDif ** 2 + yDif ** 2)
                if Dif.real < 2 * kilobotArray[i1].infraredRadius + 1:
                    if not isIdPresent(kilobotArray[i2].id, kilobotArray[i1].inIRRangeKilobotID):
                        kilobotArray[i1].inIRRangeKilobotID.append(kilobotArray[i2].id)


# check collison between the kilobot and array of kilobots/borders for rotation movement
def checkCollisionLoop_Rotate(kilobot, kilobots_array_temp, resx, resy, forward, fi_temp):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkCollisionPrediction_Rotaton(it.x, it.y, forward, fi_temp):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction_Rotaton(resx, resy, forward, fi_temp):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True

# check collison between the kilobot and array of kilobots/borders for Motors movement
def checkCollisionLoop_Motors(kilobot, kilobots_array_temp, resx, resy, fi_temp):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkCollisionPrediction_Motors(it.x, it.y, fi_temp):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction_Motors(resx, resy, fi_temp):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# kilobots movement main loop
def kilobotsMovement(enableTag, kilobotsArray, resx, resy):
    if enableTag:
        for it in kilobotsArray:
            forward = 1
            move = getRandSpin()
            M1 = getRandColor()
            M2 = getRandColor()

            #if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, forward, 5 * move):

            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1-M2)*0.001):
                #it.moveKilobot(forward)
                #it.rotateKilobot(5 * move)
                it.MotorsMoveKilobot(M1, M2)

                it.isStuck -= 1
                if it.isStuck == 0:
                    it.changeColor(124, 252, 0)

            else:
                "stuck move backward handler"
                for i in range(0, 3):
                    if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, -forward,5*move):

                        it.rotateKilobot(5 * move)
                        it.moveKilobot(-forward)

                        #it.MotorsMoveKilobot(M1, M2)

                        it.changeColor(255, 0, 0)
                        it.isStuck = 10
                    else:
                        "permanent stuck error handler"
                        it.isStuck += 1
                        if it.isStuck == 1000 and not checkCollisionLoop_tp(it, kilobotsArray, resx, resy, resx / 2,
                                                                            resy / 2):
                            it.setPositon(resx / 2, resy / 2)
                            it.isStuck = 0
                            it.changeColor(124, 252, 0)
            it.drawKilobot(screen)


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
startTime = 0
enable = False



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


def resetEvent(pos):
    global kilobotID, kilobotsNumber, enable, resetButton
    global pause
    if resetButton.isOver(pos):
        print('clicked reset button')
        kilobots.clear()
        kilobotID = 0
        kilobotsNumber = 0

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

        if not t_pause.state():
            t.start()
        else:
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
            mousepos = pygame.mouse.get_pos()
            if event.button == 1:
                addKilobotEvent(mousepos)

                resetEvent(mousepos)

                startEvent(mousepos)

                pauseEvent(mousepos)

            if event.button == 3:
                removeKilobotEvent()


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
    kilobotsMovement(enable, kilobots, resx, resy)
    kilobotClass.drawKilobots(kilobots, screen)

    for itr in kilobots:
        itr.inIRRangeKilobotID.clear()

    detectKilobotsInIRRange(kilobots)

    for itr in kilobots:
        print(itr.id)
        print(itr.inIRRangeKilobotID)

    inputEventHandler()
    pasueTimer()

    numberView.text = str(kilobotsNumber)
    timeView.text = str(t.read_time())
    resetButton.draw(screen)
    startButton.draw(screen)
    pauseButton.draw(screen)
    numberView.draw(screen)
    timeView.draw(screen)

    pygame.display.update()

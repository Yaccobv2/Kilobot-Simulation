from math import fabs, sqrt
import random2
import pygame
import kilobotClass
from button import button

# inicjalizacja biblioteki
pygame.init()
promienInput = 15

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
        if kilobot.checkSingleCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, it.x, it.y, promienInput):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, resx, resy, promienInput):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# check collison between the kilobot and array of kilobots/borders for teleport
def checkCollisionLoop_tp(kilobot, kilobots_array_temp, resx, resy, x_tp, y_tp, ):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkSingleCollisionPrediction(x_tp, y_tp, it.x, it.y, promienInput):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction(x_tp, y_tp, resx, resy, promienInput):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# check collison between the kilobot and array of kilobots/borders for rotation movement
def checkCollisionLoop_Rotate(kilobot, kilobots_array_temp, resx, resy, forward, fi_temp):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkCollisionPrediction_Rotaton(it.x, it.y, promienInput, forward, fi_temp):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction_Rotaton(resx, resy, promienInput, forward, fi_temp):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# kilobots movement main loop
def kilobotsMovement(enableTag, kilobotsArray, resx, resy):
    if enableTag:
        for it in kilobotsArray:
            forward = 1
            move = getRandSpin()
            rotation = 0
            if getRandBool():
                rotation = getRandSpin()

            if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, forward,
                                             5 * rotation):
                it.moveKilobot(forward)
                it.rotateKilobot(10 * move)

                it.isStuck -= 1
                if it.isStuck == 0:
                    it.changeColor(124, 252, 0)

                # if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, move,
                #                 #                                  5 * rotation):
                #                 #     it.rotateKilobot(5 * move)
                #                 #
                #                 #     it.isStuck -= 1
                #                 #     if it.isStuck== 0:
                #                 #         it.changeColor(124, 252, 0)

            else:
                for i in range(0, 2):
                    if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, -forward,
                                                     0):
                        it.moveKilobot(-forward)

                        it.changeColor(255, 0, 0)
                        it.isStuck = 10

                    else:
                        it.isStuck += 1
                        if it.isStuck == 1000 and not checkCollisionLoop_tp(it, kilobotsArray, resx, resy, resx / 2,
                                                                            resy / 2):
                            it.setPositon(resx / 2, resy / 2)
                            it.isStuck = 0
                            it.changeColor(124, 252, 0)
            it.drawKilobot(screen, promienInput)


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
kilobotsMaxAmount = 100;
kilobots = []
kilobotID = 0;
kilobotsNumber = 0;
enable = False;


def addKilobotEvent(pos):
    global kilobotID, kilobotsNumber
    print("Left mouse click at: " + str(pos[0]) + ", " + str(pos[1]))
    if (pos[0] > promienInput) & (pos[1] > promienInput) & (pos[0] < (resx - promienInput)) & (
            pos[1] < (resy - promienInput - 55)):
        if not checkPlacementCollision(kilobots, pos[0], pos[1]):
            kilobots.append(kilobotClass.Kilobot(kilobotID, pos[0], pos[1],0, 124, 252, 0))
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
    if resetButton.isOver(pos):
        print('clicked reset button')
        kilobots.clear()
        kilobotID = 0
        kilobotsNumber = 0
        enable = False


def startEvent(pos):
    global enable
    if startButton.isOver(pos):
        print('Clicked start button')
        enable = True


def pauseEvent(pos):
    global enable
    if pauseButton.isOver(pos):
        print('Clicked start button')
        enable = False


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
resetButton = button((255, 0, 0), resx - 100, resy - 50, 100, 50, 'Reset', True)
startButton = button((0, 255, 0), 0, resy - 50, 100, 50, 'Start', True)
pauseButton = button((0, 0, 255), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)

# glowna pętla
running = True
while running:
    screen.fill((255, 255, 255))
    # random movement
    kilobotsMovement(enable, kilobots, resx, resy)
    kilobotClass.drawKilobots(kilobots, screen, promienInput)

    inputEventHandler()

    numberView.text = str(kilobotsNumber)
    resetButton.draw(screen)
    startButton.draw(screen)
    pauseButton.draw(screen)
    numberView.draw(screen)

    pygame.display.update()

from math import fabs, sqrt
<<<<<<< Updated upstream

=======
import random2
>>>>>>> Stashed changes
import pygame
import kilobotClass
from button import button

# inicjalizacja biblioteki
pygame.init()
promienInput = 15

resx = 600
resy = 655


# rysowanie kółek
def drawCircle(pos, r, g, b, promien):
    pygame.draw.circle(screen, (r, g, b), (int(pos[0]), int(pos[1])), promien)


# rysowanie kółek
def drawCircle(pos, r, g, b):
    pygame.draw.circle(screen, (r, g, b), pos, 20)


def checkPlacementCollision(array, X, Y):

    for itr in array:
<<<<<<< Updated upstream
        xDif = fabs(X-itr.x)
        yDif = fabs(Y-itr.y)
        Dif = sqrt(xDif**2+yDif**2)
        if Dif < 40:
            return True
    return False

def reddrawWindow():
    screen.fill((255,255,255))
    resetButton.draw(screen, (0,0,0))

resx = 800
resy= 600
=======
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
            return True


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)


def getRandBool():
    return random2.randint(0, 1)


def reddrawWindow():
    screen.fill((255, 255, 255))



>>>>>>> Stashed changes
# tworzenie ekranu
screen = pygame.display.set_mode((resx, resy))

# deklaracja tablicy kilobotow
kilobotsMaxAmount = 100;
kilobots = []
kilobotID = 0;
kilobotsNumber = 0;
enable = False;

<<<<<<< Updated upstream
#tworzenie przycisku reset
resetButton = button((0,255,0), 0, 550, 100, 50, 'Reset')
=======
# tworzenie przycisku reset
resetButton = button((255, 0, 0), resx - 100, resy - 50, 100, 50, 'Reset', True)
startButton = button((0, 255, 0), 0, resy - 50, 100, 50, 'Start',  True)
pauseButton = button((0, 0, 255), resx / 2 - 50, resy - 50, 100, 50, 'Pause',  True)
numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber),  False)
>>>>>>> Stashed changes

# glowna pętla
running = True
while running:
<<<<<<< Updated upstream
    reddrawWindow()
    #screen.fill((255, 255, 255))

    for it in kilobots:
        position = (it.x, it.y)
        drawCircle(position, it.r, it.g, it.b)
=======

    screen.fill((255, 255, 255))
    # random movement
    if enable:
        for it in kilobots:
            forward = 1
            rotation = 0
            if getRandBool():
                rotation = getRandSpin()

            if not checkCollisionLoop(it, kilobots, forward, rotation, resx, resy):
                it.moveKilobot(forward)
            else:
                it.isStuck = 1
            it.drawKilobot(screen, promienInput)
            it.rotateKilobot(5 * rotation)

    for it in kilobots:
        position = (it.x, it.y)
        drawCircle(position, it.r, it.g, it.b, promienInput)
>>>>>>> Stashed changes

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
<<<<<<< Updated upstream
        if len(kilobots) <= 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPosX, mPosY = pygame.mouse.get_pos()
                if (mPosX > 20) & (mPosY >20) & (mPosX < (resx - 70)) & (mPosY < (resy -70)):

                    if not checkPlacementCollision(kilobots, mPosX, mPosY):
                        kilobots.append(kilobotClass.Kilobot(mPosX, mPosY, 255, 0, 0))
=======
>>>>>>> Stashed changes

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mPosX, mPosY = pygame.mouse.get_pos()
            if event.button == 1:
                print("Left mouse click at: " + str(mPosX) + ", " + str(mPosY))
                if (mPosX > promienInput) & (mPosY > promienInput) & (mPosX < (resx - promienInput)) & (
                        mPosY < (resy - promienInput - 55)):
                    if not checkPlacementCollision(kilobots, mPosX, mPosY):
                        kilobots.append(kilobotClass.Kilobot(kilobotID, mPosX, mPosY, 255, 0, 0))
                        print("Drew kilobot " + str(kilobotID) + " in x: " + str(mPosX) + " y: " + str(mPosY))
                        kilobotID = kilobotID + 1
                        kilobotsNumber = kilobotsNumber + 1

                if resetButton.isOver(pos):
                    print('clicked reset button')
                    kilobots.clear()
                    kilobotID = 0
                    enable = False

                if startButton.isOver(pos):
                    print('Clicked start button')
                    enable = True

                if pauseButton.isOver(pos):
                    print('Clicked start button')
                    enable = False

            if event.button == 3:
                print("Right mouse click at: " + str(mPosX) + ", " + str(mPosY))
                if checkPlacementCollisionAndTagForRemoval(kilobots, mPosX, mPosY):
                    for x in range(len(kilobots)):
                        if kilobots[x].removed == 1:
                            print("Removed kilobot " + str(kilobotID) + " in x: " + str(kilobots[x].x) + " y: " + str(
                                kilobots[x].y))
                            kilobots.pop(x)
                            kilobotsNumber = kilobotsNumber - 1
                            break

    numberView.text = str(kilobotsNumber)
    resetButton.draw(screen)
    startButton.draw(screen)
    pauseButton.draw(screen)
    numberView.draw(screen)

    pygame.display.update()

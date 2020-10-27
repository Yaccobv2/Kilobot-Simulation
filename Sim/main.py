from math import fabs, sqrt

import pygame
import random2
import kilobotClass
from button import button

# inicjalizacja biblioteki
pygame.init()


def checkPlacementCollision(array, X, Y):
    for itr in array:
        xDif = fabs(X - itr.x)
        yDif = fabs(Y - itr.y)
        Dif = sqrt(xDif ** 2 + yDif ** 2)
        if Dif < 40:
            return True
    return False


# check collison between the kilobot and array of kilobots
def checkCollisionLoop(kilobot, kilobots_array_temp, x_temp, y_temp):
    for it2 in kilobots_array_temp:
        if kilobot == it2:
            continue
        if kilobot.checkSingleCollisionPrediction(it.x + x_temp, it.y + y_temp, it2.x, it2.y):
            return True


# get random int number between -1 and 1
def getRandint():
    return random2.randint(-1, 1)


def reddrawWindow():
    screen.fill((255, 255, 255))
    resetButton.draw(screen, (0, 0, 0))


resx = 800
resy = 600
# tworzenie ekranu
screen = pygame.display.set_mode((resx, resy))

# deklaracja tablicy kilobotow
kilobots = []

# tworzenie przycisku reset
resetButton = button((0, 255, 0), 0, 550, 100, 50, 'Reset')

# glowna pętla
running = True
while running:
    reddrawWindow()

    # random movement
    for it in kilobots:
        x = getRandint()
        y = getRandint()
        if not checkCollisionLoop(it, kilobots, x, y):
            it.move(x, y)
        it.draw(screen)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            running = False
        if len(kilobots) < 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPosX, mPosY = pygame.mouse.get_pos()
                if not checkPlacementCollision(kilobots, mPosX, mPosY):
                    kilobots.append(kilobotClass.Kilobot(mPosX, mPosY, 210, 210, 210))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if resetButton.isOver(pos):
                print('clicked reset button')
                kilobots.clear()

    pygame.display.update()

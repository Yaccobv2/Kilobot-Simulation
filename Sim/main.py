from math import fabs, sqrt

import pygame
import random2

import kilobotClass

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


# tworzenie ekranu
screen = pygame.display.set_mode((800, 600))

# deklaracja tablicy kilobotow
kilobots = []

# glowna pętla
running = True
while running:

    screen.fill((255, 255, 255))

    # random movement
    for it in kilobots:
        x = getRandint()
        y = getRandint()
        if not checkCollisionLoop(it, kilobots, x, y):
            it.move(x, y)
        it.draw(screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if len(kilobots) < 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPosX, mPosY = pygame.mouse.get_pos()
                if not checkPlacementCollision(kilobots, mPosX, mPosY):
                    kilobots.append(kilobotClass.Kilobot(mPosX, mPosY, 210, 210, 210))

    pygame.display.update()

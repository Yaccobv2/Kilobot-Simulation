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


# tworzenie ekranu
screen = pygame.display.set_mode((800, 600))

# deklaracja tablicy kilobotow
kilobots = []

# glowna pętla
running = True
while running:

    screen.fill((255, 255, 255))

    for it in kilobots:
        collision = 0
        x = random2.randint(-1, 1)
        y = random2.randint(-1, 1)

        for it2 in kilobots:
            if it == it2:
                continue
            if it.checkSingleCollision(it2.x, it2.y) and
                collision = 1
                break
        if collision == 0:
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

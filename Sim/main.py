from math import fabs, sqrt

import pygame
import kilobotClass

# inicjalizacja biblioteki
pygame.init()


# rysowanie kółek
def drawCircle(pos, r, g, b):
    pygame.draw.circle(screen, (r, g, b), pos, 20)


def checkPlacementCollision(array, X, Y):

    for itr in array:
        xDif = fabs(X-itr.x)
        yDif = fabs(Y-itr.y)
        Dif = sqrt(xDif**2+yDif**2)
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
        position = (it.x, it.y)
        drawCircle(position, it.r, it.g, it.b)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if len(kilobots) <= 20:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mPosX, mPosY = pygame.mouse.get_pos()
                if not checkPlacementCollision(kilobots, mPosX, mPosY):
                    kilobots.append(kilobotClass.Kilobot(mPosX, mPosY, 255, 0, 0))

    pygame.display.update()

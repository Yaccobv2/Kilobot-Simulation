import kilobotClass
from math import fabs, sqrt
import random2


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)


# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


def getRandBool():
    return random2.randint(0, 1)


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
# def kilobotsMovement(enableTag, kilobotsArray, resx, resy):
#     if enableTag:
#         for it in kilobotsArray:
#             forward = 1
#             move = getRandSpin()
#             M1 = getRandColor()
#             M2 = getRandColor()
#
#             # if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, forward, 5 * move):
#
#             if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.001):
#                 # it.moveKilobot(forward)
#                 # it.rotateKilobot(5 * move)
#                 it.MotorsMoveKilobot(M1, M2)
#
#                 it.isStuck -= 1
#                 if it.isStuck == 0:
#                     it.changeColor(124, 252, 0)
#
#             else:
#                 "stuck move backward handler"
#                 for i in range(0, 3):
#                     if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, -forward, 5 * move):
#
#                         it.rotateKilobot(5 * move)
#                         it.moveKilobot(-forward)
#
#                         # it.MotorsMoveKilobot(M1, M2)
#
#                         it.changeColor(255, 0, 0)
#                         it.isStuck = 10
#                     else:
#                         "permanent stuck error handler"
#                         it.isStuck += 1
#                         if it.isStuck == 1000 and not checkCollisionLoop_tp(it, kilobotsArray, resx, resy, resx / 2,
#                                                                             resy / 2):
#                             it.setPositon(resx / 2, resy / 2)
#                             it.isStuck = 0
#                             it.changeColor(124, 252, 0)
#             it.drawKilobot(screen)

def kilobotsMovement(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
    if enableTag:

        closer = True
        for it in kilobotsArray:
            closestFood = it.findClosestFood()
            forward = 1
            move = getRandSpin()
            M1 = 255
            M2 = 255
            # if not checkCollisionLoop_Rotate(it, kilobotsArray, resx, resy, forward, 5 * move):
            if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                if len(it.foodID_last) > 0:
                    if not checkCollisionLoop_Motors(it, FoodArray, resx, resy, (M1 - M2) * 0.001) and not checkCollisionLoop_Motors(it, FoodArray, resx, resy, M1 * 0.001):
                        if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                            closer = True
                        else:
                            closer = False
                        if closer:
                            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.001):
                                it.MotorsMoveKilobot(M1, M2)

                        else:
                            for k in range(0, 1):
                                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.001):
                                    it.MotorsMoveKilobot(M1, 0)


                    else:
                        it.changeColor(255, 0, 0)
            it.drawKilobot(screen)

import kilobotClass
from math import fabs, sqrt
import random2


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)


# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


# get random int number between 0 and 255
def getRandMotorVal():
    return random2.randint(0, 255)


def getRandBool():
    return random2.randint(0, 1)


def getRandval():
    return random2.randint(0, 100)


# # check collison between the kilobot and array of kilobots/borders for simple movement
# def checkCollisionLoop(kilobot, kilobots_array_temp, resx, resy, x_temp, y_temp, ):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkSingleCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, it.x, it.y):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction(kilobot.x + x_temp, kilobot.y + y_temp, resx, resy):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#         return True
#
#
# # check collison between the kilobot and array of kilobots/borders for teleport
# def checkCollisionLoop_tp(kilobot, kilobots_array_temp, resx, resy, x_tp, y_tp):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkSingleCollisionPrediction(x_tp, y_tp, it.x, it.y):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction(x_tp, y_tp, resx, resy):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#
#         return True
#
#
# # check collison between the kilobot and array of kilobots/borders for rotation movement
# def checkCollisionLoop_Rotate(kilobot, kilobots_array_temp, resx, resy, forward, fi_temp):
#     for it in kilobots_array_temp:
#         if kilobot == it:
#             continue
#         if kilobot.checkCollisionPrediction_Rotaton(it.x, it.y, forward, fi_temp):
#             print("Kilobot " + str(it.id) + " collided with a different robot")
#             return True
#     if kilobot.checkWallCollisionPrediction_Rotaton(resx, resy, forward, fi_temp):
#         print("Kilobot " + str(kilobot.id) + " collided with a wall")
#         return True


# check collison between the kilobot and array of kilobots/borders for Motors movement
def checkCollisionLoop_Motors(kilobot, kilobots_array_temp, resx, resy, fi_temp, precison):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        if kilobot.checkCollisionPrediction_Motors(it.x, it.y, fi_temp, precison):
            print("Kilobot " + str(it.id) + " collided with a different robot")
            return True
    if kilobot.checkWallCollisionPrediction_Motors(resx, resy, fi_temp, precison):
        print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True


# def kilobotsMovement(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
#     if enableTag:
#
#         closer = True
#         for it in kilobotsArray:
#             closestFood = it.findClosestFood()
#             M1 = 255
#             M2 = 255
#             if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
#                 if len(it.foodID_last) > 0:
#                     if not checkCollisionLoop_Motors(it, FoodArray, resx, resy, (M1 - M2) * 0.001) and not checkCollisionLoop_Motors(it, FoodArray, resx, resy, M1 * 0.001):
#                         if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
#                             closer = True
#                         else:
#                             closer = False
#                         if closer:
#                             if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.001):
#                                 it.MotorsMoveKilobot(M1, M2)
#
#                         else:
#                             for k in range(0, 1):
#                                 if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.001):
#                                     it.MotorsMoveKilobot(M1, 0)
#
#
#                     else:
#                         it.changeColor(255, 0, 0)
#             it.drawKilobot(screen)

def kilobotsMovement(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
    if enableTag:

        closer = True

        for it in kilobotsArray:
            closestFood = it.findClosestFood()
            M1 = getRandMotorVal()
            M2 = getRandMotorVal()
            val=getRandBool()
            if closestFood is None:

                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                    it.MotorsMoveKilobot(M1, M2)
                    it.collision= False
                else:
                    it.collision = True
            if it.collision:
                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                    it.MotorsMoveKilobot(M1, 0)




            else:
                M1 = 255
                M2 = 255
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    if len(it.foodID_last) > 0:
                        if not checkCollisionLoop_Motors(it, FoodArray, resx, resy,
                                                         (M1 - M2) * 0.001, 10) and not checkCollisionLoop_Motors(it,
                                                                                                                  FoodArray,
                                                                                                                  resx,
                                                                                                                  resy,
                                                                                                                  M1 * 0.01,
                                                                                                                  10):
                            if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                                closer = True
                            else:
                                closer = False
                            if closer:
                                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                                    it.MotorsMoveKilobot(M1, M2)
                                    print("X: " + str(it.x) + " Y: " + str(it.y))

                            else:
                                for k in range(0, 4):
                                    if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 10):
                                        it.MotorsMoveKilobot(M1, 0)

                                    print("X: " + str(it.x) + " Y: " + str(it.y))

                        else:
                            it.changeColor(255, 0, 0)
            it.drawKilobot(screen)

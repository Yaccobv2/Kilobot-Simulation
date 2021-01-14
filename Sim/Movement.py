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



def checkCollisionPrediction(self, X, Y, kilobot1, kilobot2):
    return False


def kilobotsMovementFoodsearch(enableTag, kilobotsArray, FoodArray, resx, resy, screen, countdown):
    if enableTag:

        closer = True
        it1 = 0
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            closestFood = it.findClosestFood()
            M1 = getRandMotorVal()
            M2 = getRandMotorVal()
            val = getRandBool()
            if closestFood is None:

                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, (M1 - M2) * 0.01, 10):
                    it.MotorsMoveKilobot(M1, M2, 0.5)
                    it.collision = False
                else:
                    it.collision = True
            if it.collision:
                if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                    it.MotorsMoveKilobot(M1, 0, 0.1)

                else:
                    kilobotsArray.pop(it1 - 1)




            # food detected, start moving to food
            else:
                M1 = 255
                M2 = 255
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    if len(it.foodID_last) > 0:
                        # chceck if food was found
                        if not checkCollisionLoop_Motors(it, FoodArray, resx, resy,
                                                         (M1 - M2) * 0.001, 1) and not checkCollisionLoop_Motors(it,
                                                                                                                 FoodArray,
                                                                                                                 resx,
                                                                                                                 resy,
                                                                                                                 M1 * 0.01,
                                                                                                                 1):

                            it.speedTowardsTarget = it.foodID_last[closestFood][1] - it.inIRRangeFoodID[closestFood][1]
                            if it.speedTowardsTarget < it.lastSpeedTowardsTarget:
                                it.spin = -it.spin
                            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                                if it.spin == -1:
                                    it.MotorsMoveKilobot(M2, 0, 0.3)
                                else:
                                    it.MotorsMoveKilobot(0, M1, 0.3)
                                it.collision = False
                            else:
                                it.collision = True
                                print("X: " + str(it.x) + " Y: " + str(it.y))

                            if it.collision:
                                kilobotsArray.pop(it1 - 1)
                            it.lastSpeedTowardsTarget = it.speedTowardsTarget
                        # if food was found change color
                        else:
                            it.changeColor(255, 0, 0)
            it.drawKilobot(screen)


def kilobotsMovementSnake(enableTag, kilobotsArray, FoodArray, resx, resy, screen):
    if enableTag:

        it1 = 0
        for it in kilobotsArray:
            it1 = it1 + 1
            # find closest food in range
            it.targetBotID = it.id
            it.findLowerIDBot()
            M1 = 1 * getRandMotorVal()
            M2 = 1 * getRandMotorVal()

            if len(it.inIRRangeKilobotID) is 0 or it.targetBotID == it.id:
                it.found = 0
                if len(it.inIRRangeKilobotID) is not 0:
                    it.MotorsMoveKilobot(M1, M2, 0.2)
                    it.collision = False
                elif len(it.inIRRangeKilobotID) is 0:
                    it.MotorsMoveKilobot(M1, M2, 0.5)
                    it.collision = False
                else:
                    it.collision = True


            # food detected, start moving to food
            else:
                for itr2 in it.inIRRangeKilobotID:
                    if itr2[0] == it.targetBotID:
                        it.found = 1
                        break
                    else:
                        it.found = 0
                M1 = 255
                M2 = 255
                if len(it.inIRRangeKilobotID) != 0 and it.targetBotID is not it.id:
                    if not checkCollisionLoop_Motors(it, FoodArray, resx, resy,
                                                     (M1 - M2) * 0.001, 1) and not checkCollisionLoop_Motors(it,
                                                                                                             FoodArray,
                                                                                                             resx,
                                                                                                             resy,
                                                                                                             M1 * 0.01,
                                                                                                             1):
                        speedModifier = distanceAndSpeedFuzzyLogic(it.distanceToTarget)
                        if it.found == 1:
                            for itr2 in it.inIRRangeKilobotID:
                                if itr2[0] == it.targetBotID:
                                    it.speedTowardsTarget = it.distanceToTarget - itr2[1]
                            if it.speedTowardsTarget < it.lastSpeedTowardsTarget:
                                it.spin = -it.spin
                            if not checkCollisionLoop_Motors(it, kilobotsArray, resx, resy, M1 * 0.01, 0.01):
                                if it.spin == -1:
                                    it.MotorsMoveKilobot(M2, 0, speedModifier * 0.5)
                                else:
                                    it.MotorsMoveKilobot(0, M1, speedModifier * 0.5)
                            it.lastSpeedTowardsTarget = it.speedTowardsTarget
                        for itr2 in it.inIRRangeKilobotID:
                            if itr2[0] == it.targetBotID:
                                it.distanceToTarget = itr2[1]

                    # if food was found change color
                    else:
                        it.changeColor(255, 0, 0)
                        it.drawKilobot(screen)


def distanceAndSpeedFuzzyLogic(distance):
    if distance > 100:
        Modifier = 1
    elif distance < 35:
        Modifier = 0
    else:
        Modifier = distance / 100 - 0.2
    return Modifier

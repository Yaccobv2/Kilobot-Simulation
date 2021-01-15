import kilobotClass
from math import fabs, sqrt
import random2
import BasicFunc


# get random int number between -1 and 1
def getRandSpin():
    return random2.randint(-1, 1)


# get random int number between 0 and 255
def getRandColor():
    return random2.randint(0, 255)


# get random int number between 0 and 255
def getRandMotorVal():
    return random2.randint(0, 255)


# get random int number between 0 and 255
def getRandMotorValHalf():
    return random2.randint(0, 127)


def getRandBool():
    return random2.randint(0, 1)


def getRandval():
    return random2.randint(0, 100)




# check collison between the kilobot and array of kilobots/borders for Motors movement
def checkCollisionLoop_Motors(kilobot, kilobots_array_temp, resx, resy, fi_temp, precison):
    for it in kilobots_array_temp:
        if kilobot == it:
            continue
        # if kilobot.checkCollisionPrediction_Motors(it.x, it.y, fi_temp, precison):
        #     print("Kilobot " + str(it.id) + " collided with a different robot")
        #     return True
    if kilobot.checkWallCollisionPrediction_Motors(resx, resy, fi_temp, precison):
        # print("Kilobot " + str(kilobot.id) + " collided with a wall")
        return True






def AIrotateleft(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, 0, 0.5)
        # kilobotsArray[id].rotateKilobot(20)
        # kilobotsArray[id].drawKilobot(screen)


def AIrotateleftHalf(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, M2 / 3, 0.5)
        # kilobotsArray[id].rotateKilobot(20)
        # kilobotsArray[id].drawKilobot(screen)


def AIrotateright(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(0, M2, 0.5)
        # kilobotsArray[id].rotateKilobot(-20)
        # kilobotsArray[id].drawKilobot(screen)


def AIrotaterightHalf(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1 / 3, M2, 0.5)
        # kilobotsArray[id].rotateKilobot(-20)
        # kilobotsArray[id].drawKilobot(screen)


def AIMoveFront(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 255
        M2 = 255
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 0.5)
        # kilobotsArray[id].drawKilobot(screen)


def AIMoveStop(enableTag, kilobotsArray, id, screen):
    if enableTag:
        M1 = 0
        M2 = 0
        kilobotsArray[id].MotorsMoveKilobot(M1, M2, 2)
        # kilobotsArray[id].drawKilobot(screen)


def RandomMovement(enableTag, kilobotsArray, resx, resy):
    if enableTag:

        it1 = 0
        for it in kilobotsArray:

            M1 = getRandMotorVal()
            M2 = getRandMotorVal()

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
            it1 += 1


def kilobotPIDmovement(enableTag, kilobotsArray, screen):
    if enableTag:

        for it, kilobot in enumerate(kilobotsArray):

            closestFood = kilobot.findClosestFood()

            if closestFood is not ValueError and len(kilobot.inIRRangeFoodID) > 0 and len(kilobot.foodID_last) >0:

                PIDval = kilobot.calcPI(80, kilobot.inIRRangeFoodID[closestFood][1], 5.2,5.71, 100000, -100000,
                                         kilobot.inIRRangeFoodID[closestFood][1] - kilobot.foodID_last[closestFood][1])
                # P,I,D=kilobot.getPID()
                # PIDval = kilobot.calcPI(80, kilobot.inIRRangeFoodID[closestFood][1], P, I, 1000, -1000,
                #                          kilobot.inIRRangeFoodID[closestFood][1] - kilobot.foodID_last[closestFood][1])

                if PIDval >= 60:
                    AIrotaterightHalf(enableTag, kilobotsArray, it, screen)

                if 60 > PIDval >= 10:
                    AIrotateright(enableTag, kilobotsArray, it, screen)

                if PIDval <= -40:
                    AIrotateleftHalf(enableTag, kilobotsArray, it, screen)

                if -5 >= PIDval >= -60:
                    AIrotateleft(enableTag, kilobotsArray, it, screen)

                if 10 > PIDval > -5:
                    AIMoveFront(enableTag, kilobotsArray, it, screen)

                # print(PIDval)
                kilobot.drawKilobot(screen)


########################################################################################################################
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


def kilobotsFoodFindingMovement(enableTag, kilobotsArray, screen):
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
                it.MotorsMoveKilobot(M1, M2, 0.5)
                





            # food detected, start moving to food
            else:
                M1 = 255
                M2 = 255
                if closestFood is not ValueError and len(it.inIRRangeFoodID) == len(it.foodID_last):
                    # chceck if food was found
                    # if not
                    if len(it.foodID_last) > 0 and not it.inIRRangeFoodID[closestFood][1] < 35:
                        it.changeColor(124, 252, 0)

                        # check if kilobot is getting closer to food
                        if it.foodID_last[closestFood][1] >= it.inIRRangeFoodID[closestFood][1]:
                            closer = True
                        else:
                            closer = False

                        # move forward if getting closer
                        if closer:
                            it.MotorsMoveKilobot(M1, M2, 0.5)


                        # rotate if getting closer
                        else:
                            for k in range(0, 4):
                                it.MotorsMoveKilobot(M1, 0, 0.1)

                        # if food was found change color
                    else:
                        it.changeColor(255, 0, 0)
                        it.body.velocity = (0, 0)
            it.drawKilobot(screen)


def distanceAndSpeedFuzzyLogic(distance):
    if distance > 100:
        Modifier = 1
    elif distance < 35:
        Modifier = 0
    else:
        Modifier = distance / 100 - 0.2
    return Modifier

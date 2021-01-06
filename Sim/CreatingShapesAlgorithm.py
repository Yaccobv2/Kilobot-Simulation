import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc

resx = 1200
resy = 800

screen = pygame.display.set_mode((resx, resy))




def PIDcontrol():
    global FoodID, kilobotID, kilobotsNumber, FoodNumber
    # creating config data
    kilobotsMaxAmount = 100
    kilobots = []
    Foods = []
    kilobots.clear()
    kilobotID = 0
    kilobotsNumber = 0
    FoodID, FoodNumber = 0, 0
    startTime = 0
    enable = False

    # creating buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timeers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()
    clock = pygame.time.Clock()

    # main loop
    while running:
        clock.tick(240)
        screen.fill((255, 255, 255))
        # random movement
        t, enable, t_pause, kilobots, Foods,kilobotID,kilobotsNumber,FoodID, FoodNumber = BasicFunc.inputEventHandler(t, enable, t_pause, kilobots, Foods, kilobotID,kilobotsNumber,FoodID, FoodNumber,startButton,pauseButton,resetButton)

        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()

        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        for itr in kilobots:
            print(str(itr.id) + ":" + str(itr.inIRRangeFoodID))
            print(str(itr.id) + ":" + str(itr.inIRRangeKilobotID))

        Movement.kilobotsMovement(enable, kilobots, Foods, resx, resy, screen)

        BasicFunc.FoodsInIRRange_last(kilobots)
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # t = BasicFunc.pasueTimer(t_pause, t)

        numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()

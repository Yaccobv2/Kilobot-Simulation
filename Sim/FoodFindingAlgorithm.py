import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc
import pymunk
import invisibleWall

resx = 1200
resy = 800

screen = pygame.display.set_mode((resx, resy))


def FindingFood():
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
    wallsBuilt = 0

    # creating buttons
    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    # timers and loop config
    running = True
    t = Timer()
    t_pause = Timer()
    t.set_default()
    t_pause.set_default()

    # creating physics space
    space = pymunk.Space()
    # creating fps clock
    clock = pygame.time.Clock()

    # main loop
    while running:

        clock.tick(30)
        screen.fill((255, 255, 255))

        # building walls
        if wallsBuilt == 0:
            space=BasicFunc.buildWalls(screen, resx, resy,space)
            wallsBuilt = 1

        # mouse input handler
        t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, space = BasicFunc.inputEventHandler(
            t, enable, t_pause, kilobots, Foods, kilobotID, kilobotsNumber, FoodID, FoodNumber, startButton,
            pauseButton, resetButton, space)

        # update list of food in range
        for itr in kilobots:
            itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()
            itr.refreshCoord()

        for itr in Foods:
            itr.body.velocity=(0,0)
            itr.refreshCoord()

        BasicFunc.detectFoodsInIRRange(kilobots, Foods)
        BasicFunc.detectKilobotsInIRRange(kilobots)

        # pid movment of kilobots
        Movement.kilobotsFoodFindingMovement(True, kilobots, screen)

        BasicFunc.FoodsInIRRange_last(kilobots)

        # drawing kilobots
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawKilobots(Foods, screen)

        # update physics engine
        space.step(1 / 50)

        # t = BasicFunc.pasueTimer(t_pause, t)

        # setting number of kilobots in simulation
        numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())

        # drawing other objects
        BasicFunc.drawWalls(screen, resx, resy)
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)


        pygame.display.update()

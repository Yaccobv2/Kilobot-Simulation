import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc

resx = 1200
resy = 800

# def ai_basic_start():
#     x = 200
#     for a_i in range(0, 1):
#         position = [x, 200]
#         x = x + 100
#         BasicFunc.addKilobotEvent(position)
#         BasicFunc.addSpecialKilobotEvent([500, 300])


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(ai, 500)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))



def ai(genomes, config):
    screen = pygame.display.set_mode((resx, resy))

    # deklaracja tablicy kilobotow
    kilobotsMaxAmount = 100
    kilobots = []
    kilobots.clear()
    kilobotID = 0
    kilobotsNumber = 0
    SpecialkilobotID, SpecialkilobotsNumber = 0, 0
    startTime = 0
    enable = False
    FoodArray = []

    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(kilobotsNumber), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    t = Timer()
    t_pause = Timer()

    t.set_default()
    t_pause.set_default()

    clock = pygame.time.Clock()
    running = True

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    # kilobots = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        x_t = 200
        position = [x_t, 200]
        x_t = x_t + 100
        kilobots.append(BasicFunc.addKilobotEvent(position, kilobots, kilobotID))
        kilobotID += 1
        ge.append(genome)
    x = 800
    y = 600
    kilobotID = 0
    position2 = [x, y + 100]
    FoodArray.append(BasicFunc.addSpecialKilobotEvent(position2, FoodArray, kilobotID, 255, 10, 100))
    for i in range(0, 3):
        kilobotID += 1
        x = x - 80
        position2 = [x, y]
        FoodArray.append(BasicFunc.addSpecialKilobotEvent(position2, FoodArray, kilobotID, 0, 128, 0))
        kilobotID += 1
        x = x - 80

        position2 = [x, y]
        FoodArray.append(BasicFunc.addSpecialKilobotEvent(position2, FoodArray, kilobotID, 0, 128, 0))
        x = x - 100
        y = y - 100

    t, enable, t_pause = BasicFunc.startEventmanual(t, t_pause)
    while running and len(kilobots) > 0:
        clock.tick(240)
        screen.fill((255, 255, 255))
        # random movement
        # inputEventHandler()

        for i1 in kilobots:
            i1.detectFoodsInIRRange(FoodArray)
        # update list of food in range
        for itr in kilobots:
            # itr.inIRRangeKilobotID.clear()
            itr.inIRRangeFoodID.clear()

        # detectFoodsInIRRange(kilobots, FoodArray)
        # detectKilobotsInIRRange(kilobots)
        for i1 in kilobots:
            i1.detectFoodsInIRRange(FoodArray)

        # for itr in kilobots:
        #     print(str(itr.id) + ":" + str(itr.inIRRangeFoodID))
        #     print(str(itr.id) + ":" + str(itr.inIRRangeKilobotID))

        time = t.read_time()
        for x, kilobot in enumerate(kilobots):  # give each kilobot a fitness of distance to food
            if len(kilobot.foodID_last) > 0:
                if kilobot.foodID_last[0][1] > kilobot.inIRRangeFoodID[0][1]:
                    closer = True
                else:
                    closer = False
                if closer and time > 0:
                    ge[x].fitness += 1 / kilobot.inIRRangeFoodID[0][1] * 100 / (time * 10)
                else:
                    ge[x].fitness -= 1 / kilobot.inIRRangeFoodID[0][1] * 0.01
            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[kilobots.index(kilobot)].activate((kilobot.inIRRangeFoodID[0][1],
                                                             kilobot.inIRRangeFoodID[1][1],
                                                             kilobot.inIRRangeFoodID[2][1],
                                                             kilobot.inIRRangeFoodID[3][1],
                                                             kilobot.inIRRangeFoodID[4][1],
                                                             kilobot.inIRRangeFoodID[5][1],
                                                             kilobot.inIRRangeFoodID[6][1]))

            if kilobot.inIRRangeFoodID[0][1] < 30:
                print("winner")
                kilobot.changeColor(255, 0, 0)
                ge[x].fitness = ge[x].fitness + 100 - time * 10
                nets.pop(kilobots.index(kilobot))
                ge.pop(kilobots.index(kilobot))
                kilobots.pop(kilobots.index(kilobot))
            else:
                if not kilobot.checkWallCollision(resx, resy):
                    #     ge[kilobots.index(kilobot)].fitness -= 0.01

                    # else:
                    if output[
                        0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                        Movement.AIMoveFront(enable, kilobots, kilobots.index(kilobot), screen)
                    if output[
                        1] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                        Movement.AIrotateleft(enable, kilobots, kilobots.index(kilobot), screen)
                    if output[
                        2] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                        Movement.AIrotateright(enable, kilobots, kilobots.index(kilobot), screen)

        for kilobot in kilobots:
            # if kilobot.checkWallCollision(resx, resy):
            #     ge[kilobots.index(kilobot)].fitness -= 1
            #     nets.pop(kilobots.index(kilobot))
            #     ge.pop(kilobots.index(kilobot))
            #     kilobots.pop(kilobots.index(kilobot))
            # if len(kilobot.foodID_last) > 0:
            #     if kilobot.foodID_last[0][1] == kilobot.inIRRangeFoodID[0][1]:
            #         ge[kilobots.index(kilobot)].fitness -= 0.1
            # if kilobot.inIRRangeFoodID[0][1]<100:
            #     ge[kilobots.index(kilobot)].fitness +=0.2
            for food in FoodArray:
                if FoodArray.index(food) != 0:
                    if kilobot.checkCollisionbetweenKilobots(food.x, food.y):
                        ge[kilobots.index(kilobot)].fitness -= 1
                        nets.pop(kilobots.index(kilobot))
                        ge.pop(kilobots.index(kilobot))
                        kilobots.pop(kilobots.index(kilobot))

        # Movement.kilobotsMovement(enable, kilobots, FoodArray, resx, resy, screen)

        for x, kilobot in enumerate(kilobots):
            if time > 6:
                # if 2 > ge[x].fitness > -2:
                #     ge[kilobots.index(kilobot)].fitness -= 1
                ge[kilobots.index(kilobot)].fitness -= 1
                nets.pop(kilobots.index(kilobot))
                ge.pop(kilobots.index(kilobot))
                kilobots.pop(kilobots.index(kilobot))

        BasicFunc.FoodsInIRRange_last(kilobots)
        kilobotClass.drawKilobots(kilobots, screen)
        kilobotClass.drawFoods(FoodArray, screen)
        # t=pasueTimer(t_pause,t)

        numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()

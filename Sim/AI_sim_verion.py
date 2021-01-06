import pygame
from button import button
from timer import Timer
import neat
import Movement
import kilobotClass
import BasicFunc
import pickle
import gzip

resx = 1200
resy = 800



# def ai_basic_start():
#     x = 200
#     for a_i in range(0, 1):
#         position = [x, 200]
#         x = x + 100
#         BasicFunc.addKilobotEvent(position)
#         BasicFunc.addSpecialKilobotEvent([500, 300])


def run(config_file, genome_path="network.pkl"):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    global gen
    gen = BasicFunc.GetGenerationNumber()

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-89')

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # collect data to save
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # set number of data to save
    p.add_reporter(neat.Checkpointer(10, None))

    # Run for up to x generations.
    winner = p.run(ai_food_finding, 200)

    # save data to file
    stats.save()
    # save generation number
    BasicFunc.SaveGenerationNumber(gen)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

    p.remove_reporter(stats)

    # save results
    with open("network.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


def run_results(config_file, genome_path="network.pkl"):
    # Load requried NEAT config
    global gen
    gen = BasicFunc.GetGenerationNumber()

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_file)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    ai_food_finding(genomes, config)


def ai_food_finding(genomes, config):
    global gen, x_food, y_food
    gen += 1
    screen = pygame.display.set_mode((resx, resy))

    # deklaracja tablicy kilobotow
    kilobotsMaxAmount = 100
    kilobots = []
    kilobots.clear()
    kilobotID, FoodID, kilobotsNumber, FoodNumber = 0, 0, 0, 0
    startTime = 0
    enable = False
    FoodArray = []

    resetButton = button((220, 220, 220), resx - 100, resy - 50, 100, 50, 'Reset', True)
    startButton = button((220, 220, 220), 0, resy - 50, 100, 50, 'Start', True)
    pauseButton = button((220, 220, 220), resx / 2 - 50, resy - 50, 100, 50, 'Pause', True)
    numberView = button((255, 255, 255), resx / 2 - 50, 50, 100, 50, str(gen), False)
    timeView = button((255, 255, 255), resx - 50, 0, 50, 50, str(startTime), False)

    t = Timer()
    t_pause = Timer()

    t.set_default()
    t_pause.set_default()

    clock = pygame.time.Clock()
    running = True

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # kilobot object that uses that network to play
    nets = []
    # kilobots = []
    ge = []
    x_t = 100
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

        x_t = x_t + 100
        position = [150, 150]
        kilobots,kilobotID, kilobotNumber = BasicFunc.addKilobotEventAI(position, kilobots, kilobotID, kilobotsNumber)
        ge.append(genome)

    # creating food in random place every 50 generations
    if gen % 30 == 0 or gen == 1:
        x_food = BasicFunc.getRandX()
        y_food = BasicFunc.getRandY()
    # creating food
    kilobotID = 0
    position2 = [800, 300]
    FoodArray, FoodID, FoodNumber = BasicFunc.addSpecialKilobotEvent(position2, FoodArray, FoodID, FoodNumber, 255, 10, 100)

    x = 300
    y = 100
    # creating obstacles
    # for i_y in range(0, 7):
    #     for i in range(0, 3):
    #         kilobotID += 1
    #
    #         position2 = [x, y]
    #         FoodArray.append(BasicFunc.addSpecialKilobotEvent(position2, FoodArray, kilobotID, 0, 128, 0))
    #         kilobotID += 1
    #         x = x + 200
    #
    #     y = y + 100
    #     x = 300

    t, enable, t_pause = BasicFunc.startEventmanual(t, t_pause)
    closer=False
    while running and len(kilobots) > 0:
        clock.tick(400)
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
                    ge[x].fitness += 3 / kilobot.inIRRangeFoodID[0][1]
                #     ge[x].fitness += 1 / kilobot.inIRRangeFoodID[0][1] * 100 / (time * 10)
                # else:
                #     ge[x].fitness -= 1 / kilobot.inIRRangeFoodID[0][1] * 0.01
                ge[x].fitness -= 2 / kilobot.inIRRangeFoodID[0][1]
            # send kilobot position and decide to move or rotate
            # output = nets[kilobots.index(kilobot)].activate((kilobot.inIRRangeFoodID[0][1],
            #                                                  kilobot.inIRRangeFoodID[1][1],
            #                                                  kilobot.inIRRangeFoodID[2][1],
            #                                                  kilobot.inIRRangeFoodID[3][1],
            #                                                  kilobot.inIRRangeFoodID[4][1],
            #                                                  kilobot.inIRRangeFoodID[5][1],
            #                                                  kilobot.inIRRangeFoodID[6][1],
            #                                                  kilobot.inIRRangeFoodID[7][1],
            #                                                  kilobot.inIRRangeFoodID[8][1],
            #                                                  kilobot.inIRRangeFoodID[9][1],
            #                                                  kilobot.inIRRangeFoodID[10][1],
            #                                                  kilobot.inIRRangeFoodID[11][1],
            #                                                  kilobot.inIRRangeFoodID[12][1],
            #                                                  kilobot.inIRRangeFoodID[13][1],
            #                                                  kilobot.inIRRangeFoodID[14][1],
            #                                                  kilobot.inIRRangeFoodID[15][1],
            #                                                  kilobot.inIRRangeFoodID[16][1],
            #                                                  kilobot.inIRRangeFoodID[17][1],
            #                                                  kilobot.inIRRangeFoodID[18][1],
            #                                                  kilobot.inIRRangeFoodID[19][1],
            #                                                  kilobot.inIRRangeFoodID[20][1],
            #                                                  kilobot.inIRRangeFoodID[21][1]))
            output = nets[x].activate([kilobot.inIRRangeFoodID[0][1],closer])


            #give fitness if closer
            if kilobot.inIRRangeFoodID[0][1] < 150:
                ge[x].fitness += 1 / kilobot.inIRRangeFoodID[0][1]


           #give fitness if reach goal
            if kilobot.inIRRangeFoodID[0][1] < 30:
                print("winner")
                kilobot.changeColor(255, 0, 0)
                ge[x].fitness = ge[x].fitness + 10
                nets.pop(kilobots.index(kilobot))
                ge.pop(kilobots.index(kilobot))
                kilobots.pop(kilobots.index(kilobot))
            else:
                # if not kilobot.checkWallCollision(resx, resy):
                #     ge[kilobots.index(kilobot)].fitness -= 0.01

                # finding the highiest value in outputs
                max_value = max(output)
                max_index = output.index(max_value)

                if max_index == 0 and output[max_index] > 0.5:
                    Movement.AIMoveFront(enable, kilobots, kilobots.index(kilobot), screen)
                if max_index == 1 and output[max_index] > 0.5:
                    Movement.AIrotateleft(enable, kilobots, kilobots.index(kilobot), screen)
                if max_index == 2 and output[max_index] > 0.5:
                    Movement.AIrotateright(enable, kilobots, kilobots.index(kilobot), screen)


        for x,kilobot in enumerate(kilobots):
            if kilobot.checkWallCollision(resx, resy):
                kilobot.BounceIfWallCollision(resx,resy)
                ge[x].fitness += 3 / kilobot.inIRRangeFoodID[0][1]
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
                    if food.index == 0:
                        continue
                    else:
                        if kilobot.checkCollisionbetweenKilobots(food.x, food.y):
                            ge[kilobots.index(kilobot)].fitness -= 2
                            nets.pop(kilobots.index(kilobot))
                            ge.pop(kilobots.index(kilobot))
                            kilobots.pop(kilobots.index(kilobot))

        # Movement.kilobotsMovement(enable, kilobots, FoodArray, resx, resy, screen)

        for x, kilobot in enumerate(kilobots):
            if time > 3:
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

        # numberView.text = str(kilobotsNumber)
        timeView.text = str(t.read_time())
        resetButton.draw(screen)
        startButton.draw(screen)
        pauseButton.draw(screen)
        numberView.draw(screen)
        timeView.draw(screen)

        pygame.display.update()



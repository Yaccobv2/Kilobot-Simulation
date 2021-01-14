import pygame
import os
import AI_sim_verion
import CreatingShapesAlgorithm

# inicjalizacja biblioteki
pygame.init()

CreatingShapesAlgorithm.PIDcontrol()

# if __name__ == '__main__':
#     # Determine path to configuration file. This path manipulation is
#     # here so that the script will run successfully regardless of the
#     # current working directory.
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, 'config_neat.txt')
#     AI_sim_verion.run(config_path)

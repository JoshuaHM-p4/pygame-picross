import pygame

pygame.init()
from gamelib.picross import GameState

clock = pygame.time.Clock()
############################### < MAIN GAME LOOP > ####################################
def run():
    game_state = GameState()
    while True:
        game_state.state_manager()
        clock.tick(120)
#######################################################################################

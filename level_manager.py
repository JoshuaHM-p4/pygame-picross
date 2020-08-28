import pygame
import numpy as np
import os

location = os.path.join(os.path.dirname(__file__), 'levels')
# print(location)
def save_level(grid):
    print('Saving')
    try:
        np.save(os.path.join(location, 'Test'), grid, allow_pickle = True)
    except:
        os.mkdir(location)
        np.save(os.path.join(location, 'Test'), grid, allow_pickle = True)
    print('Successfully Saved!')

def load_level():
    print('Loading')
    file = np.load(os.path.join(location, 'Test.npy'), allow_pickle = True)
    print('Successfully Loaded')
    return file

def show_list():
    for _ in os.listdir(location):
        pygame.draw.rect()
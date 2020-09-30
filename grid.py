import pygame
import numpy as np
import os

from pixel import Pixel
class Grid:
    screen = None
    font = pygame.font.Font(os.path.join(os.getcwd(),'resources','04B_19.TTF'),30)
    number_color = (94, 170, 167)

    def __init__(self, grid_size = (5,5)):
        self.columns, self.rows = grid_size
        self.CreateGrid()

    def CreateGrid(self):
        self.grid = np.array([np.array([Pixel((x, y)) for x in range(self.columns)]) for y in range(self.rows)])

    # def LoadFromArray(self, array):
    #     """ Loads a grid from a 2d array (only used from inside the code for testing purposes) """
    #     self.grid = np.array([np.array([Pixel((x,y),state = num) for x,num in enumerate(column)]) for y,column in enumerate(array)])
    #     self.columns = self.grid.shape[0]
    #     self.rows = self.grid.shape[1]

    def load_grid(self, npy_grid, is_resized):
        self.change_size(npy_grid.shape == (10,10), is_resized)
        self.grid = npy_grid

    def change_pixel(self, cursor_pos, interaction):    
        for row in self.grid:
            for pixel in row:
                if pixel.pixel_rect.collidepoint(cursor_pos):
                    if interaction == 'empty':
                        pixel.empty()
                    elif interaction == 'fill':
                        pixel.fill()
                    elif interaction == 'cross':
                        pixel.cross()
                    elif interaction == 'uncross':
                        pixel.uncross()

    def draw(self):
        for row in self.grid:
            for pix in row:
                pix.render()

    def change_size(self, is_ten, is_resized): 
        if is_ten:
            self.rows, self.columns = (10,10)
            Pixel.size = 50 if is_resized else 25
        else:
            self.rows, self.columns = (5,5)
            Pixel.size = 76 if is_resized else 50

    def reposition_grid(self):
        ## This function is used to reposition grid when resized ## 
        for row in self.grid:
            for pix in row:
                grid_size = 10 if (self.columns,self.rows) == (10,10) else 5
                pix.align_pos(grid_size)

    def drawNumbers(self, rows:str, columns: str): # Takes an array of strings (that are: '3 2') and renders onto the screen beside or above the pixels
        for row,num in enumerate(rows):
            pixel_pos = self.grid[row][0].pointlocation
            text_pos = (                               # Sets the text position horizontally
                pixel_pos[0] - len(num.strip()),      
                pixel_pos[1] + self.grid[0][0].size//2
            )            
            num_surface = self.font.render(str(num), True, self.number_color)
            num_rect = num_surface.get_rect(midright = text_pos)
            Grid.screen.blit(num_surface, num_rect)

        for column,num in enumerate(columns):
            pixel_pos = self.grid[0][column].pointlocation
            vertical_text = num.strip()
            if vertical_text != '10':
                for y,num in enumerate(vertical_text): # Sets the numbers vertically
                    text_pos = (                                                  
                        pixel_pos[0] + self.grid[0][0].size//2,                   
                        pixel_pos[1] - int(-y * 15) - int(len(vertical_text)*15) 
                    )
                    num_surface = self.font.render(str(num), True, self.number_color)
                    num_rect = num_surface.get_rect(center = text_pos)
                    Grid.screen.blit(num_surface, num_rect)
            else:
                text_pos = (pixel_pos[0] + self.grid[0][0].size//2, pixel_pos[1] - 15)
                num_surface = self.font.render(str(num), True, self.number_color)
                num_rect = num_surface.get_rect(center = text_pos)
                Grid.screen.blit(num_surface, num_rect)


    @staticmethod
    def groupNum(line):
        """ This will group 1s from an line (array) into a form of discrete tomography.\n
        Input: >>> list = [1,1,0,1,1,1]\n
        Ouput: >>> '2 3' """
        #Turn into string
        str_line = ''.join(map(str, line))
        # Find length of ones
        ones = list(filter(None, str_line.split('0')))
        ones = list(map(len, ones))
        # Turn back into string ###
        group_line = ' '.join(map(str,ones))
        if not group_line: return '0'
        return group_line

    def getNumbers(self) -> str:
        rows = [self.groupNum(self.grid[y,:]) for y in range(len(self.grid))]
        columns = [self.groupNum(self.grid[:,x]) for x in range(len(self.grid[0]))]
        return rows, columns

    def grid_states(self):
        """ Grid array in pixel-state form (1s and 0s)  """
        return(np.array([[pixel.state for pixel in row] for row in self.grid]))

    def __eq__(self, second_grid): 
        comparison = [p == h for pgrid,hgrid in zip(self.grid, second_grid.grid) for p,h in zip(pgrid,hgrid)]
        return np.array(comparison, dtype = object)

    def compare(self, second_grid):
        self.grid 

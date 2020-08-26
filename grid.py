import pygame
import numpy as np
from pixel import Pixel
class Grid:
    font = pygame.font.Font('mypicross/04B_19.TTF',30)
    def __init__(self, screen, columns = 5, rows = 5, creating = True):
        self.screen = screen
        self.columns = columns
        self.rows = rows
        self.creating = creating

        if creating:
            self.MakeGrid()
        else:
            self.MakeGrid()
            # self.loadGrid()

    def toggle_creative(self):
        if self.create == False:
            self.create = True
        else:
            self.create = False

    def MakeGrid(self):
        self.grid = np.array([np.array([Pixel(self.screen, x, y) for x in range(self.columns)]) for y in range(self.rows)],dtype = object)

    def LoadGrid(self):
        pass

    def draw(self):
        for row in self.grid:
            for pix in row:
                pix.render()

    def check_collision(self, pos, mbutton):
        for row in self.grid:
            for pixel in row:
                if pixel.pixel_rect.collidepoint(pos):
                    if mbutton == 'button1':
                        pixel.fill()
                    elif mbutton == 'button2' and self.creating:
                        pixel.empty()
                    elif mbutton == 'button2' and self.creating == False:
                        pixel.cross()

    # def print2dArray(grid):
    #    print([pixel for pixel in row] for row in self.grid])

    def drawNumbers(self, rows, columns):
        for i,n in enumerate(rows):
            pixel_pos = self.grid[i][0].pointlocation
            text_pos = (pixel_pos[0] - len(n.strip()), pixel_pos[1] + Pixel.SIZE//2)
            
            num_surface = self.font.render(str(n), True, (94, 170, 167))
            num_rect = num_surface.get_rect(midright = text_pos)
            self.screen.blit(num_surface, num_rect)

        for i,n in enumerate(columns):
            pixel_pos = self.grid[0][i].pointlocation
            vertical_text = n.strip()
            for y,num in enumerate(vertical_text):
                w = Pixel.SIZE
                text_pos = (pixel_pos[0] + Pixel.SIZE//2, 
                pixel_pos[1] - (-y * w *0.3) - (len(vertical_text)* (w * 0.3)) 
                )
                num_surface = self.font.render(str(num), True, (94, 170, 167))
                num_rect = num_surface.get_rect(center = text_pos)
                self.screen.blit(num_surface, num_rect)

    @staticmethod
    def groupNum(line):
        """ This will group 1s into a form of discrete tomography.\n
        Input: >>> list = [0,1,1,0,0,1,1,1]\n
        Ouput: >>> [2,3]
        """
        ### Turn into string ###
        str_line = ''.join(map(str, line))
        ### Find length of ones ###
        ones = list(filter(None, str_line.split('0')))
        ones = list(map(len, ones))
        ### Turn back into string ###
        group_line = ' '.join(map(str,ones))
        if not group_line: return '0'
        return group_line

    def getNumbers(self):
        ######### ROWS #########
        rows = []
        for y in range(len(self.grid)):
            row = self.grid[y,:]
            str_row = self.groupNum(row)
            rows.append(str_row)    
        ######## COLUMNS ########
        columns = []
        for x in range(len(self.grid[0])):
            column = self.grid[:,x]
            str_column = self.groupNum(column)
            columns.append(str_column)
        return rows, columns
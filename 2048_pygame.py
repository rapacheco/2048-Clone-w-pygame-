"""
Author: Rafael Pacheco Ribeiro
Clone of 2048 game.
Part of this code was written by me as an assignment in the Coursera class Principles of Computing (Part 1)
This implementation takes the code written in that class, which runs with simplegui, to run with pygame
"""

import pygame
from pygame.locals import *
import os, sys
import random

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Directions constants
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Graphicals constants
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 50
BORDER = 15
WHITE = (255,255,255)
BLACK = (0, 0, 0)
FONT = (119, 110, 101)
FONT2 = (249, 246, 242)
BACK = (187, 173, 160)
BACKFIN = (237, 223, 210)
COLOR_DICT = {0 : (205, 193, 180), 2 : (238, 228, 218), 4 : (237, 224, 200), 8 : (242, 177, 121), 16 : (245, 149, 99), \
                   32 : (246, 124, 95), 64 : (246, 94, 59), 128 : (237, 207, 114), 256 : (237, 204, 97), 512 : (237, 200, 80), \
                   1024 : (236, 196, 64), 2048 : (236, 77, 88)}

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = [0 for dummy_tile in range(len(line))]
    count = 0
    for idx in range(len(line)):
        if line[idx] != 0:
            result[count] = line[idx]
            count += 1
    
    for idx in range(len(result)-1):
        if result[idx] == result[idx + 1]:
            result[idx] *= 2
            result[idx + 1] = 0
            
    for dummy_time in range(len(result)):
        for idx in range(len(result)-1):
            if result[idx] == 0 and result[idx + 1] != 0:
                result[idx] = result[idx + 1]
                result[idx + 1] = 0
    
    return result

def convert_back(game, direction, opposite, lenght, tiles):
    """
    Takes the merged tiles and implements the grid
    """
    same = True
    initial = game.get_initial()
    board = game.get_grid()
    for tile in opposite:
        for step in lenght:
            row = initial[direction][tile][0] + OFFSETS[direction][0] * step 
            col = initial[direction][tile][1] + OFFSETS[direction][1] * step
            if direction == 1:
                if board[row][col] != tiles[col][row]:
                    same = False
                board[row][col] = tiles[col][row]
            elif direction == 2:
                if board[row][col] != tiles[col][game.get_grid_height() - 1 - row]:
                    same = False
                board[row][col] = tiles[col][game.get_grid_height() - 1 - row]
            elif direction == 3:
                if board[row][col] != tiles[row][col]:
                    same = False
                board[row][col] = tiles[row][col]
            else:
                if board[row][col] != tiles[row][game.get_grid_width() - 1 - col]:
                    same = False
                board[row][col] = tiles[row][game.get_grid_width() - 1 - col]
    return board, same
    
def check_lose(game):
    """
    Checks if there are legal possibles movements left. 
    If there are not, the player has lost the game.
    """
    test = game.clone()
    lose = True
    for direction in OFFSETS.keys():
        test.move(direction)
        if game.get_grid() != test.get_grid():
            lose = False
    return lose    
    
def test(game):
    for direction in OFFSETS.keys():
        game.move(direction)

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        self._initial = {UP : [(0, 0 + col) for col in range(self._width)], 
                         DOWN : [(self._height - 1, 0 + col) for col in range(self._width)],
                         LEFT : [(0 + row, 0) for row in range(self._height)], 
                         RIGHT : [(0 + row, self._width - 1) for row in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_row in range(self._width)] for dummy_col in range(self._height)]        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width
    
    def get_initial(self):
        """
        Get the initial grid.
        """
        return self._initial
    
    def get_grid(self):
        """
        Get the actual grid of the game.
        """
        return self._grid

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction == 1 or direction == 2:
            lenght, opposite = range(self._height), range(self._width)
        else:
            lenght, opposite = range(self._width), range(self._height)
        
        lsts = [[self.get_tile(self._initial[direction][tile][0] + OFFSETS[direction][0] * step,
                               self._initial[direction][tile][1] + OFFSETS[direction][1] * step)
                for step in lenght] for tile in opposite]
        for idx in range(len(lsts)):
            lsts[idx] = merge(lsts[idx])
            
        self._grid, same = convert_back(self, direction, opposite, lenght, lsts)

        if not same: 
            self.new_tile()
                    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        done = False
        while not done:
            row = random.choice(range(self._height))
            col = random.choice(range(self._width))
            if self._grid[row][col] == 0:
                done = True
        if random.random() >= 0.9:
            digit = 4
        else:
            digit = 2
        self._grid[row][col] = digit

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
        
    def clone(self):
        """
        Returns a object clone of the current game
        """
        height = self.get_grid_height()
        width = self.get_grid_width()
        clone = TwentyFortyEight(height, width)
        for col in range(height):
            for row in range(width):
                value = self.get_tile(row, col)
                clone.set_tile(row, col, value)
        return clone
        
class Graphics:
    """
    Object for running the GUI for the game
    """
    
    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._dimensions = (BORDER + self._cols * (BORDER + TILE_SIZE), BORDER + self._rows * (BORDER + TILE_SIZE))
        self._screen = pygame.display.set_mode(self._dimensions)
        self._screen.fill(BACK)
        pygame.display.set_caption("2048 - Pygame")
        pygame.display.flip()
        
        self._font = pygame.font.SysFont("Arial", 50)
        self._font_small = pygame.font.SysFont("Arial", 40)
        self._font_winlose = pygame.font.SysFont("Arial", 80)
        
        self._clock = pygame.time.Clock()
        self._game = game
                
    def draw(self):
        """
        Draws the game into the canvas
        """
        global win, lose
        # Checks if there are legal movements left
        if check_lose(game):
            lose = True
        
        for row in range(self._rows):
            for col in range(self._cols):
                num = self._game.get_tile(row, col)
                if num == 2048:
                    win = True
                    
                color = COLOR_DICT[num]
                tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
                tile.fill(color)
                top = BORDER + row * (TILE_SIZE + BORDER)
                left = BORDER + col * (TILE_SIZE + BORDER)
                self._screen.blit(tile, (top, left))
                tile.convert()
                
                if num != 0:
                    offset = 0
                    if num in [2, 4]:
                        label = self._font.render(str(num), True, FONT)
                    elif num in [1024, 2048]:
                        label = self._font_small.render(str(num), True, FONT2)
                        offset = BORDER * 2 / 3
                    else:
                        label = self._font.render(str(num), True, FONT2)
                    label_size = self._font.size(str(num))
                    self._screen.blit(label, (top + (TILE_SIZE - label_size[0]) / 2+ offset, left + (TILE_SIZE - label_size[1]) / 2))
                    label.convert()
                    
        if win or lose:
            # tells the user if he/she won or lost
            if win:
                mes = "YOU WIN!"
            elif lose:
                mes = "YOU LOSE!"
            message = self._font_winlose.render(mes, True, BLACK)
            message_size = self._font_winlose.size(mes)
            mark = ((self._dimensions[0] - message_size[0]) / 2, (self._dimensions[1] - message_size[1]) / 2)
            self._screen.blit(message, mark)
            
            # prompts user for a new game
            prompt = self._font_small.render("New Game? (Y/N)", True, BLACK)
            prompt_size = self._font_small.size("New Game? (Y/N)")
            self._screen.blit(prompt, (mark[0] + (message_size[0] - prompt_size[0]) / 2, mark[1] + message_size[1] + BORDER))
         
    # def erase(self):
        # self._screen.fill(BACK)
        # black = pygame.Surface(self._screen.get_size())
        # black = black.convert()
        # black.fill(BLACK)
        # self._screen.blit(black, (0, 0))
    
    def animate(self):
        """
        Provides the animation of the sliding tiles
        """
        pass
    
    def tick(self):
        self._clock.tick(60)
        
# initializes pygame
pygame.init()

game = TwentyFortyEight(4, 4)
run = Graphics(game)
pygame.time.set_timer(USEREVENT+1, 50)

# main loop with the game's logic
done = False
win = False
lose = False
animate = False
while not done:
    run.tick()
    
    # Comment out to play the game!!!!
    # test(game)
    #game.set_tile(0, 0, 2048)
    #game.set_tile(1, 1, 1024)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move(LEFT)
            elif event.key == pygame.K_DOWN:
                game.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                game.move(UP)
            elif event.key == pygame.K_RIGHT:
                game.move(DOWN)
            elif (win or lose) and event.key == pygame.K_y: # Restarting the game does not restart the drawing
                win, lose = False, False
                game.reset()
                run = Graphics(game)
            elif (win or lose) and event.key == pygame.K_n:
                done = True
                
        elif event.type == USEREVENT+1 and animate:
            run.animate()
            
    run.draw()
    # run.erase()
        
    pygame.display.flip()   

pygame.quit()
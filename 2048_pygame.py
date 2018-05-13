"""
Author: Rafael Pacheco Ribeiro
Clone of 2048 game.
Part of this code was written by me as an assignment in the Coursera class Principles of Computing (Part 1)
This implementation takes the code written in that class to run with pygame
"""

import pygame
from pygame.locals import *
import os, sys
import random

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# Directions constants
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Graphicals constants
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 50
BORDER = 15
BOARD_SIZE = BORDER * 5 + TILE_SIZE * 4
WHITE = (255,255,255)
FONT = (119, 110, 101)
FONT2 = (249, 246, 242)
BACK = (187, 173, 160)
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

    def clone(self):
        """
        Returns a 2048 clone of the current object
        """
        temp = TwentyFortyEight(4, 4)
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                temp.set_tile(row, col, self._grid[row][col])
        return temp

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

        return same

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
        self.set_tile(row, col, digit)

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

    def check(self):
        """
        Checks for win or lose conditions
        """
        return self.check_win() or self.check_lose()

    def check_win(self):
        """
        Checks for win conditions
        """
        result = False
        for row in range(len(self._grid)):
            for col in range(len(self._grid[row])):
                if self.get_tile(row, col) == 2048:
                    result = True
        return result

    def check_lose(self):
        """
        Checks for lose conditions
        """
        temp = self.clone()
        lose = True
        for i in range(1, 5):
            if not temp.move(i):
                lose = False
        return lose

class Graphics(pygame.sprite.Sprite):
    """
    Class to run the GUI for the game
    """

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._screen = pygame.display.set_mode((BORDER + self._cols * (BORDER + TILE_SIZE), BORDER + self._rows * (BORDER + TILE_SIZE)))
        self._font = pygame.font.SysFont("Arial", 50)
        self._font_s = pygame.font.SysFont("Arial", 30)
        self._clock = pygame.time.Clock()
        self._game = game
        pygame.display.set_caption("2048 - Pygame")
        self.fill_back()

    def fill_back(self):
        """
        Paints the background of the game
        """
        self._screen.fill(BACK)

    def draw(self):
        """
        Draws the game into the canvas
        """
        for row in range(self._rows):
            for col in range(self._cols):
                num = self._game.get_tile(row, col)
                color = COLOR_DICT[num]
                tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
                tile.fill(color)

                top = BORDER + row * (TILE_SIZE + BORDER)
                left = BORDER + col * (TILE_SIZE + BORDER)
                self._screen.blit(tile, (top, left))

                if num != 0:
                    if num in [2, 4]:
                        label = self._font.render(str(num), True, FONT)
                    else:
                        label = self._font.render(str(num), True, FONT2)
                    label_size = self._font.size(str(num))
                    offset = BORDER / 2 - 2
                    self._screen.blit(label, (top + (TILE_SIZE - label_size[0]) / 2, left - offset + (TILE_SIZE - label_size[1]) / 2 + offset / 2))

    def draw_end(self, phrase):
        """
        Draws an end condition on the screen
        """
        screen_phrase = self._font.render(phrase, True, (0,0,0))
        phrase_size = self._font.size(phrase)
        self._screen.blit(screen_phrase, ((BOARD_SIZE - phrase_size[0]) / 2, BOARD_SIZE / 5))

        new_game = self._font_s.render("(N)ew Game?", True, (0,0,0))
        new_game_size = self._font_s.size("(N)ew Game?")
        self._screen.blit(new_game, ((BOARD_SIZE - new_game_size[0]) / 2, BOARD_SIZE / 3))

        quit = self._font_s.render("(Q)uit?", True, (0,0,0))
        quit_size = self._font_s.size("(Q)uit?")
        self._screen.blit(quit, ((BOARD_SIZE - quit_size[0]) / 2, BOARD_SIZE / 2.5))

    def tick(self):
        """
        Runs the clock
        """
        self._clock.tick(60)

# initializes pygame and create a frame
pygame.init()

game = TwentyFortyEight(4, 4)
game.set_tile(1, 1, 1024)
game.set_tile(1, 2, 1024)
run = Graphics(game)

# main loop with the game's logic
done, end, win, lose = False, False, False, False

while not done:
    run.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN and not end:
            if event.key == pygame.K_UP:
                game.move(LEFT)
            elif event.key == pygame.K_DOWN:
                game.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                game.move(UP)
            elif event.key == pygame.K_RIGHT:
                game.move(DOWN)
            # checks if game end/lose conditions are met
            if game.check_win():
                end, win = True, True
            elif game.check_lose():
                end, lose = True, True

        elif event.type == pygame.KEYDOWN and end:
            if event.key == pygame.K_n:
                run.fill_back()
                game.reset()
                end, win, lose = False, False, False
            elif event.key == pygame.K_q:
                done = True

    run.draw()

    if end and win:
        run.draw_end("YOU WIN!!!")
    elif end and lose:
        run.draw_end("YOU LOSE!!")

    pygame.display.flip()

pygame.quit()

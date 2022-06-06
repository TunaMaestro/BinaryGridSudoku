import pygame
import random
import pygame.locals
import sys
import pprint

import binaryPuzzle

pygame.init()

# Basic App Stuff
FPS = 144
fpsClock = pygame.time.Clock()
pygame.display.set_caption('The Legendary Binary Puzzle Generator™')

# Colours
BLACK = (0, 0, 0)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
CYAN = (42, 121, 144)
RED = (255, 87, 87)
GREEN = (187, 255, 51)

# create window
WIDTH = 1000
HEIGHT = 800
ROWS = 12
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 60, 60
_VARS = {'surf': False}


def get_grid(path):
    with open(path) as f:
        g = []
        for line in f:
            line = line.strip().split(',')
            g.append([bool(int(x)) if x.isnumeric() else None for x in line])
    return g


class Board:
    def __init__(self, grid):
        self.grid = grid.copy()
        self.preexisting = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if not grid[row][col] is None:
                    self.preexisting.append((row, col))
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))

        self.font = pygame.font.SysFont("system", 120)


        self.selected = None  # Coordinates of the currently selected tile

        self.strikes = 0

    def __str__(self):
        return pprint.pformat(self.grid)

    def main(self):
        looping = True
        strikeText = None
        # Main Game Loop
        while looping:
            self.draw_grid()
            # Recieve inputs
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    # print("LOL")
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    mouseCoords = pygame.mouse.get_pos()
                    loc = self.canvas_coords_to_grid_coords(mouseCoords)

                    # print(f'Mouse Coords: {mouseCoords}. Translated loc: {loc}')
                    if 0 <= loc[0] <= 5 and 0 <= loc[1] <= 5:
                        self.selected = loc
                    else:
                        self.selected = None

                if event.type == pygame.KEYDOWN:
                    if self.selected:
                        match event.key:
                            case pygame.K_0:
                                self.grid[self.selected[0]][self.selected[1]] = False
                            case pygame.K_1:
                                self.grid[self.selected[0]][self.selected[1]] = True
                    if event.key == pygame.K_RETURN:
                        finished = self.check()
                        strikeText = self.draw_check(finished)

                    if event.key in [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]:
                        self.move_selection(event.key)

            self.draw_select()
            self.draw_cell_values()
            if strikeText:
                self.window.blit(strikeText, self.grid_coords_to_canvas_coords((6, 0)))

            pygame.display.update()
            fpsClock.tick(FPS)

    @staticmethod
    def canvas_coords_to_grid_coords(coords):
        x, y = coords

        row, col = (y - 100) * 6 // 600, (x - 200) * 6 // 600

        return row, col

    @staticmethod
    def grid_coords_to_canvas_coords(loc, offset=(0, 0)):
        """
        :param loc: row, col location
        :param offset: x, y offset
        :return: x, y coordinates on canvas
        """
        row, col = loc

        y, x = row * 100 + 100 + offset[1], col * 100 + 200 + offset[0]  # Offset is (x, y), so index has to be reversed

        return x, y

    def draw_grid(self):
        self.window.fill(WHITE)

        for row in range(6):
            for col in range(6):
                r = pygame.rect.Rect(self.grid_coords_to_canvas_coords((row, col)), (100, 100))
                pygame.draw.rect(self.window, BLACK, r, 4)
        gridBorder = pygame.rect.Rect((200, 100), (600, 600))
        gridBorder = gridBorder.inflate(8, 8)
        pygame.draw.rect(self.window, BLACK, gridBorder, 4)
        # TODO: make not hardcoded

    def draw_cell_values(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell is None:
                    text = ""
                else:
                    text = str(int(cell))
                colour = BLACK if (i, j) in self.preexisting else GREY

                text = self.font.render(text, True, colour)
                self.window.blit(text, self.grid_coords_to_canvas_coords((i, j), offset=(25, 10)))

    def draw_select(self):
        if self.selected:
            colour = GREY if self.selected in self.preexisting else RED
            pygame.draw.rect(self.window, colour, (*self.grid_coords_to_canvas_coords(self.selected), 100, 100), 4)

    def move_selection(self, key):
        move = 0, 0
        match key:
            case pygame.K_LEFT:
                move = 0, -1
            case pygame.K_UP:
                move = -1, 0
            case pygame.K_RIGHT:
                move = 0, 1
            case pygame.K_DOWN:
                move = 1, 0

        if 0 <= self.selected[0] + move[0] < 6:
            self.selected = self.selected[0] + move[0], self.selected[1]

        if 0 <= self.selected[1] + move[1] < 6:
            self.selected = self.selected[0], self.selected[1] + move[1]

    def check(self):
        self.strikes += 1
        tupleGrid = tuple(tuple(x) for x in self.grid)
        result = binaryPuzzle.check(tupleGrid)
        self.draw_check(result)
        return result

    def draw_check(self, valid):

        text = self.font.render("x" * self.strikes, True, RED)
        return text



board = Board(get_grid('grid.csv'))

print(board)

board.main()

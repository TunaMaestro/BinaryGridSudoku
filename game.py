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

        self.selected = None  # Coordinates of the currently selected tile

    def __str__(self):
        return pprint.pformat(self.grid)

    def main(self):
        looping = True

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
                        tupleGrid = tuple(tuple(x) for x in self.grid)
                        # pprint.pprint(tupleGrid)
                        # print()
                        print(binaryPuzzle.check(tupleGrid))

            self.draw_select()
            self.draw_cell_values()
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
        font = pygame.font.SysFont("system", 120)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                if cell is None:
                    text = ""
                else:
                    text = str(int(cell))
                colour = BLACK if (i, j) in self.preexisting else GREY

                text = font.render(text, True, colour)
                self.window.blit(text, self.grid_coords_to_canvas_coords((i, j), offset=(25, 10)))

    def draw_select(self):
        if self.selected:
            pygame.draw.rect(self.window, RED, (*self.grid_coords_to_canvas_coords(self.selected), 100, 100), 4)

    def check(self):
        pass


board = Board(get_grid('grid.csv'))

print(board)

board.main()

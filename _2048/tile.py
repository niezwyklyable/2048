
import pygame
from .constants import RADIUS, GAP, MARGIN, HEIGHT, WIDTH

# colors
from .constants import ALMOST_WHITE, GREY, CREAMY, WHITE, LIGHT_ORANGE, \
    ORANGE, DARK_ORANGE, RED, LIGHT_YELLOW, YELLOW, DARK_YELLOW, ALMOST_GOLD, GOLD

class Tile():
    VEL = 60
    dR = 15 # for self.create_visualization() in Game class
    dR2 = 2 # for self.merge_visualization() in Game class

    def __init__(self, row, col, size, value):
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.dx = 0 # zaleza od self.VEL i od dir
        self.dy = 0
        self.dest_x = 0 # zaleza od step i od dir
        self.dest_y = 0
        self.size = size
        self.value = value
        self.calc_pos()

    def draw(self, win):
        bg_color, num_color = self.get_color()
        pygame.draw.rect(win, bg_color, (self.x, self.y, self.size, self.size), border_radius = RADIUS)
        font = pygame.font.SysFont('comicsans', 50)
        number = font.render(str(self.value), 1, num_color)
        win.blit(number, (int(self.x + self.size / 2 - number.get_width() / 2), \
            int(self.y + self.size / 2 - number.get_height() / 2)))

    def get_color(self):
        if self.value == 2:
            return (ALMOST_WHITE, GREY)
        elif self.value == 4:
            return (CREAMY, GREY)
        elif self.value == 8:
            return (LIGHT_ORANGE, WHITE)
        elif self.value == 16:
            return (ORANGE, WHITE)
        elif self.value == 32:
            return (DARK_ORANGE, WHITE)
        elif self.value == 64:
            return (RED, WHITE)
        elif self.value == 128:
            return (LIGHT_YELLOW, WHITE)
        elif self.value == 256:
            return (YELLOW, WHITE)
        elif self.value == 512:
            return (DARK_YELLOW, WHITE)
        elif self.value == 1024:
            return (ALMOST_GOLD, WHITE)
        elif self.value == 2048:
            return (GOLD, WHITE)

    def move(self, dir, step):
        if dir == 'left':
            self.col -= step
        elif dir == 'right':
            self.col += step
        elif dir == 'up':
            self.row -= step
        elif dir == 'down':
            self.row += step

        self.calc_pos()

    def calc_pos(self):
        self.x = MARGIN + GAP + self.col * (self.size + GAP)
        self.y = HEIGHT - WIDTH + MARGIN + GAP + self.row * (self.size + GAP)

    def calc_dest(self, dir, step):
        if step == 0:
            self.dx = 0
            self.dy = 0
            self.dest_x = MARGIN + GAP + self.col * (self.size + GAP)
            self.dest_y = HEIGHT - WIDTH + MARGIN + GAP + self.row * (self.size + GAP)
            return

        if dir == 'left':
            self.dx = -1 * self.VEL
            self.dy = 0
            self.dest_x = MARGIN + GAP + (self.col - step) * (self.size + GAP)
            self.dest_y = HEIGHT - WIDTH + MARGIN + GAP + self.row * (self.size + GAP)
        elif dir == 'right':
            self.dx = 1 * self.VEL
            self.dy = 0
            self.dest_x = MARGIN + GAP + (self.col + step) * (self.size + GAP)
            self.dest_y = HEIGHT - WIDTH + MARGIN + GAP + self.row * (self.size + GAP)
        elif dir == 'up':
            self.dx = 0
            self.dy = -1 * self.VEL
            self.dest_x = MARGIN + GAP + self.col * (self.size + GAP)
            self.dest_y = HEIGHT - WIDTH + MARGIN + GAP + (self.row - step) * (self.size + GAP)
        elif dir == 'down':
            self.dx = 0
            self.dy = 1 * self.VEL
            self.dest_x = MARGIN + GAP + self.col * (self.size + GAP)
            self.dest_y = HEIGHT - WIDTH + MARGIN + GAP + (self.row + step) * (self.size + GAP)
        
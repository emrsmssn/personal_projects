import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

#RGB colors
RED = (204, 35, 22)
BLACK = (0,0,0,)
WHITE = (240,240,240)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown1.png'), (40, 40))

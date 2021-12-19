import pygame

WIDTH = 800
HEIGHT = 600
sc = pygame.display.set_mode((WIDTH, HEIGHT))

cash = 1000
BLUE = (39, 40, 91)
LIGHT_BLUE = (106, 139, 197)

FPS = 60

pygame.init()
FONT = pygame.font.SysFont('century gothic', 30, bold=True)
FONT_small = pygame.font.SysFont('century gothic', 24, bold=True)

pygame.font.init()

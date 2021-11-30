import pygame
from draw_menu import *
from change_screen import *
from draw_missions import *
from draw_constructor import *
pygame.init()
WIDTH, HEIGHT = 800, 600
draw_screen = "menu"
spare_part = "nothing"
mouse_position_x = 0
mouse_position_y = 0
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_position_x = event.pos[0]
            mouse_position_y = event.pos[1]
        if event.type == pygame.MOUSEBUTTONUP:
            draw_screen = show_screen(draw_screen, mouse_position_x, mouse_position_y)
            spare_part = recognise_modules(draw_screen, mouse_position_x, mouse_position_y)

    if draw_screen == "menu":
        draw_menu(mouse_position_x, mouse_position_y)
    elif draw_screen == "list_of_missions":
        draw_missions()
    elif draw_screen == "constructor":
        draw_constructor()
    show_modules(spare_part)
    pygame.display.update()

import pygame
from draw_menu import *
from change_screen import*
# надо добавить импорты реальных функций
pygame.init()

WIDTH, HEIGHT = 800, 600
draw_screen = "menu"
mouse_position_x = 0
mouse_position_y = 0
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60
finished = False

while not finished:
    # FIXME вставить отображение фона
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_position_x = event.pos[0]
            mouse_position_y = event.pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_screen = show_screen(draw_screen, mouse_position_x, mouse_position_y)
    if draw_screen == "menu":
        draw_menu(mouse_position_x, mouse_position_y)
    elif draw_screen == "list_of_missions":
        circle(sc, (0, 0, 0), (400, 400), 50)
    elif draw_screen == 3:
        draw_constructor()
    # FIXME вставить кнопку ненаведённую
    # FIXME вставить кнупку наведённую
    pygame.display.update()

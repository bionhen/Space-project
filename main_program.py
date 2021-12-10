from pygame.draw import *
from draw_menu import *
from change_screen import *
from draw_missions import *
from draw_constructor import *
pygame.init()
WIDTH, HEIGHT = 800, 600
draw_screen = "menu"
mouse_click = [-1, -1, -1, -1, -1]
mouse_position_x = 0
mouse_position_y = 0
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))
click = [-1, -1, -1, -1, -1]
rocket_list = []
rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
flag1 = False
flag2 = False
k = -1
j = -1
clock = pygame.time.Clock()
FPS = 60
finished = False

while not finished:
    clock.tick(FPS)
    happen = "nothing"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_position_x = event.pos[0]
            mouse_position_y = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            happen = "mouse_button_up"

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_screen = show_screen(draw_screen, mouse_position_x, mouse_position_y)
            happen = "mouse_button_down"

    if draw_screen == "menu":
        draw_menu(mouse_position_x, mouse_position_y)
    elif draw_screen == "list_of_missions":
        draw_missions()
    elif draw_screen == "constructor":
        click, rocket_list, rocket_surface, flag1, flag2, k, j = draw_constructor_foo(
            happen, click, rocket_list, rocket_surface, flag1, flag2, k, j)
    elif draw_screen == "flying":
        circle(sc, (0, 0, 0), (400, 300), 300)
    show_modules(mouse_click)
    pygame.display.update()

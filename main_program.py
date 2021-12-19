from constants import *
from draw_menu import *
from change_screen import *
from draw_missions import *
from draw_constructor import *
from draw_flight import *
pygame.init()
draw_screen = "menu"
mouse_click = [-1, -1, -1, -1, -1]
mouse_position_x = 0
rocket_fuel_max = 10
mouse_position_y = 0
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))
click = [-1, -1, -1, -1, -1]
rocket = Rocket()
flag_activation = True
flag1 = False
flag2 = False
flag_dif = False
flag_rock = False
flag_right, flag_left, flag_forward = False, False, False
happens = ["nothing", "nothing"]
time_step = fire_big_step = fire_small_step = 0
moved_module = Module()
k = j = -1
clock = pygame.time.Clock()
FPS = 60
finished = False

while not finished:
    clock.tick(FPS)
    happen = "nothing"
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and draw_screen == "flying_prepared" and event.key == pygame.K_UP:
            happens = "key_down"
            flag_forward = True
        if event.type == pygame.KEYDOWN and draw_screen == "flying_prepared" and event.key == pygame.K_LEFT:
            happens = "key_down"
            flag_left = True
        if event.type == pygame.KEYDOWN and draw_screen == "flying_prepared" and event.key == pygame.K_RIGHT:
            happens = "key_down"
            flag_right = True
        if event.type == pygame.KEYUP and draw_screen == "flying_prepared" and event.key == pygame.K_UP:
            happens = "key_up"
            flag_forward = False
        if event.type == pygame.KEYUP and draw_screen == "flying_prepared" and event.key == pygame.K_LEFT:
            happens = "key_up"
            flag_left = False
        if event.type == pygame.KEYUP and draw_screen == "flying_prepared" and event.key == pygame.K_RIGHT:
            happens = "key_up"
            flag_right = False
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


    print(flag_right)
    if draw_screen == "menu":
        draw_menu_foo()
    elif draw_screen == "list_of_missions":
        draw_missions_foo()
    elif draw_screen == "constructor":
        print(flag_right)
        click, rocket, moved_module, flag1, flag2, flag_dif, flag_rock, k, j, cash = draw_constructor_foo(
            happen, click, rocket, moved_module, flag1, flag2, flag_dif, flag_rock, k, j, cash)
    elif draw_screen == "flying_unprepared":
        #rocket = Rocket()
        #rocket.list = rocket_list
        #rocket.h = 6400000
        #fuel_calc(rocket)
        #rocket_fuel_max = rocket.fuel
        #y_bottom, y_top, x_left, x_right = find_max_coord(rocket_list)
        #rocket.surface = render_rocket_surface(rocket_surface_width, rocket_surface_height, x_left, y_top, rocket)
        draw_screen = "flying_prepared"
    elif draw_screen == "flying_prepared":
        if flag_activation:
            rocket.find_max_coord()
            rocket.find_center_mass()
            rocket.find_rocket_width_and_height()
            rocket.render_rocket_surface()
            rocket.find_engines()
        draw_flight_foo(rocket, happens, flag_forward, flag_left, rocket_fuel_max, time_step,
                            fire_big_step, fire_small_step)
        if flag_activation:
            flag_activation = False

    show_modules(mouse_click)
    pygame.display.update()

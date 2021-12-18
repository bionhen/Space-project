import pygame
from draw_constructor import rocket_list
from starship_modules import *


class Rocket:

    """
    класс ракеты
    surface - поверхность ракеты
    list - список элементов ракеты
    h - расстояние до цента Земли в км
    angle - угол поворота ракеты
    vx, vy - скорости по осям x и y
    omega -  угловая скорость
    """
    surface = pygame.Surface((0, 0))
    list = ()
    h = 6400
    x = 0
    angle = 0
    vx = 0
    vy = 0
    omega = 0
    fuel = 0


module0 = Module()
module0.type = 'tank'
module0.m = 100
module0.fuel = 1000
module0.price = 0
module0.resistance = 100
module0.force = 100
module0.image = 'fuel_1x1'
module0.a = 50
module0.b = 50
module0.x = 50
module0.y = 200
module0.surface = pygame.image.load("images/constructor/modules/fuel_1x1.png")
module0.surface = pygame.transform.scale(module0.surface, (module0.b, module0.a))

module1 = Module()
module1.type = 'engine'
module1.m = 100
module1.fuel = 0
module1.price = 0
module1.resistance = 100
module1.force = 100
module1.image = 'engine_2x1'
module1.a = 50
module1.b = 50
module1.x = 50
module1.y = 250
module1.surface = pygame.image.load("images/constructor/modules/engine_1x1.png")
module1.surface = pygame.transform.scale(module1.surface, (module1.b, module1.a))

module2 = Module()
module2.type = 'engine_r'
module2.m = 100
module2.fuel = 0
module2.price = 0
module2.resistance = 100
module2.force = 200
module2.image = 'engine_2x1'
module2.a = 100
module2.b = 50
module2.x = 100
module2.y = 200
module2.surface = pygame.image.load("images/constructor/modules/engine_right_2x1.png")
module2.surface = pygame.transform.scale(module2.surface, (module2.b, module2.a))

module3 = Module()
module3.type = 'engine_l'
module3.m = 100
module3.fuel = 0
module3.price = 0
module3.resistance = 100
module3.force = 200
module3.image = 'engine_2x1'
module3.a = 100
module3.b = 50
module3.x = 0
module3.y = 200
module3.surface = pygame.image.load("images/constructor/modules/engine_left_2x1.png")
module3.surface = pygame.transform.scale(module3.surface, (module3.b, module3.a))

module4 = Module()
module4.type = 'block'
module4.m = 100
module4.fuel = 0
module4.price = 0
module4.resistance = 100
module4.force = 200
module4.image = 'module_2x1'
module4.a = 100
module4.b = 50
module4.x = 50
module4.y = 100
module4.surface = pygame.image.load("images/constructor/modules/block_2x1.png")
module4.surface = pygame.transform.scale(module4.surface, (module4.b, module4.a))

module5 = Module()
module5.type = 'fairing'
module5.m = 100
module5.fuel = 0
module5.price = 0
module5.resistance = 100
module5.force = 200
module5.image = 'fairing_2x1'
module5.a = 100
module5.b = 50
module5.x = 50
module5.y = 0
module5.surface = pygame.image.load("images/constructor/modules/fairing_2x1.png")
module5.surface = pygame.transform.scale(module5.surface, (module5.b, module5.a))

#rocket_list = [module0, module1, module2, module3, module4, module5]


def find_max_coord(rocket_list_arg):
    """Функция находит наиболее близкий элемент к земле."""
    print('aaaa', rocket_list_arg)
    rocket_modules_y_bottom = []
    rocket_modules_y_top = []
    rocket_modules_x_left = []
    rocket_modules_x_right = []
    y_bottom_arg = 0
    y_top_arg = 0
    x_left_arg = 0
    x_right_arg = 0
    for rocket_module in rocket_list_arg:
        rocket_modules_y_bottom.append(rocket_module.y + rocket_module.a) #- 50)
        rocket_modules_y_top.append(rocket_module.y) #- 50)
        rocket_modules_x_left.append(rocket_module.x) #- 200)
        rocket_modules_x_right.append(rocket_module.x + rocket_module.b) #- 200)
    if rocket_modules_y_top != [] and rocket_modules_y_bottom != []:
        y_bottom_arg = max(rocket_modules_y_bottom)
        y_top_arg = min(rocket_modules_y_top)

    if rocket_modules_x_left != [] and rocket_modules_x_right != []:
        x_left_arg = min(rocket_modules_x_left)
        x_right_arg = max(rocket_modules_x_right)

    if x_left_arg == x_right_arg:
        x_left_arg = 0

    if y_top_arg == y_bottom_arg:
        y_top_arg = 0

    return y_bottom_arg, y_top_arg, x_left_arg, x_right_arg


def render_rocket_surface(rocket_surface_width_arg, rocket_surface_height_arg, x_left, y_top, rocket):
    rocket.surface = pygame.Surface((rocket_surface_width_arg, rocket_surface_height_arg), pygame.SRCALPHA)
    for rocket_module in rocket.list:
        rocket_module.x = rocket_module.x - x_left
        rocket_module.y = rocket_module.y - y_top
        rocket.surface.blit(rocket_module.surface, (rocket_module.x, rocket_module.y))
    return rocket.surface


def find_center_mass(rocket_arg):
    m = 0
    mx = 0
    my = 0
    for module in rocket_arg.list:
        m += module.m
        my += module.m * (module.y + module.a / 2)
        mx += module.m * (module.x + module.b / 2)
    if m == 0:
        m = 100
    y_center_mass = my / m
    x_center_mass = mx / m

    return x_center_mass, y_center_mass

def find_engines(rocket):
    engines_cord = []
    engines_left_cord = []
    engines_right_cord = []
    for rocket_module in rocket.list:
        if rocket_module.type == 'engine':
            engines_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
        if rocket_module.type == 'engine_l':
            engines_left_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
        if rocket_module.type == 'engine_r':
            engines_right_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
    return engines_cord, engines_left_cord, engines_right_cord


def render_rocket(rocket_list):
    rocket = Rocket()
    rocket.list = rocket_list
    rocket.h = 6400000

    return rocket

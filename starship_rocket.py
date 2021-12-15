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
module0.y = 50
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
module1.y = 100
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
module2.y = 50
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
module3.y = 50
module3.surface = pygame.image.load("images/constructor/modules/engine_left_2x1.png")
module3.surface = pygame.transform.scale(module3.surface, (module3.b, module3.a))

rocket_list = [module0, module1, module2, module3]

def find_max_coord(rocket_list):
    """Функция находит наиболее близкий элемент к земле."""
    rocket_modules_y_bottom = []
    rocket_modules_y_top = []
    rocket_modules_x_left = []
    rocket_modules_x_right = []
    y_bottom = 0
    y_top = 0
    x_left = 0
    x_right = 0
    for rocket_module in rocket_list:
        rocket_modules_y_bottom.append(rocket_module.y + rocket_module.a) #- 50)
        rocket_modules_y_top.append(rocket_module.y) #- 50)
        rocket_modules_x_left.append(rocket_module.x) #- 200)
        rocket_modules_x_right.append(rocket_module.x + rocket_module.b) #- 200)
    if rocket_modules_y_top != [] and rocket_modules_y_bottom != []:
        y_bottom = max(rocket_modules_y_bottom)
        y_top = min(rocket_modules_y_top)

    if rocket_modules_x_left != [] and rocket_modules_x_right != []:
        x_left = min(rocket_modules_x_left)
        x_right = max(rocket_modules_x_right)

    if x_left == x_right:
        x_left = 0

    if y_top == y_bottom:
        y_top = 0

    return y_bottom, y_top, x_left, x_right


def render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket):
    rocket.surface = pygame.Surface((rocket_surface_widht, rocket_surface_height), pygame.SRCALPHA)
    for rocket_module in rocket.list:
        rocket_module.x = rocket_module.x - x_left
        rocket_module.y = rocket_module.y - y_top
        rocket.surface.blit(rocket_module.surface, (rocket_module.x, rocket_module.y))
    return rocket.surface


def find_center_mass(rocket):
    m = 0
    mx = 0
    my = 0
    for module in rocket.list:
        m += module.m
        my += module.m * (module.y + module.a / 2)
        mx += module.m * (module.x + module.b / 2)
    y_center_mass = my / m
    x_center_mass = mx / m

    return x_center_mass, y_center_mass

def find_engines(rocket):
    engines_cord = []
    for rocket_module in rocket.list:
        if rocket_module.type == 'engine':
            engines_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
    return engines_cord

y_bottom, y_top, x_left, x_right = find_max_coord(rocket_list)
rocket_surface_height, rocket_surface_widht = y_bottom - y_top + 50, x_right - x_left

rocket = Rocket()
rocket.list = rocket_list
#rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
rocket.h = 6400000
engines_cord = find_engines(rocket)


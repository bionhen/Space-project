import pygame
from draw_constructor import rocket_list
from starship_modules import *

class Rocket:

    """
    класс ракеты
    surf - поверхность ракеты
    list - список элементов ракеты
    h - расстояние до цента Земли в км
    angle - угол поворота ракеты
    vx, vy - скорости по осям x и y
    omega -  угловая скорость
    """
    surf = pygame.Surface((0, 0))
    list = ()
    h = 6400
    x = 0
    angle = 0
    vx = 0
    vy = 0
    omega = 0
    fuel = 0

module0 = Module()
module0.type = 'engine'
module0.m = 100
module0.fuel = 100
module0.price = 0
module0.resistance = 100
module0.force = 100
module0.image = 'engine_2x1'
module0.a = 50
module0.b = 50
module0.x = 50
module0.y = 50
module0.surface = pygame.image.load("images/constructor/modules/fuel_1x1.png")
module0.surface = pygame.transform.scale(module0.surface, (module0.b, module0.a))

module1 = Module()
module1.type = 'engine'
module1.m = 100
module1.fuel = 100
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

rocket_list = [module0, module1]

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
        print(rocket_module.x)
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
    print(rocket.surface)
    return rocket.surface

y_bottom, y_top, x_left, x_right = find_max_coord(rocket_list)
rocket_surface_height, rocket_surface_widht = y_bottom - y_top, x_right - x_left

print(y_bottom, y_top, x_left, x_right)

rocket = Rocket()
rocket.list = rocket_list
rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)



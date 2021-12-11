import pygame
from draw_constructor import rocket_list

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
        rocket_modules_y_bottom.append(rocket_module.y + rocket_module.a - 50)
        rocket_modules_y_top.append(rocket_module.y - 50)
        rocket_modules_x_left.append(rocket_module.x - 200)
        rocket_modules_x_right.append(rocket_module.x + rocket_module.b - 200)

    if rocket_modules_y_top != [] and rocket_modules_y_bottom != []:
        y_bottom = max(rocket_modules_y_bottom)
        y_top = min(rocket_modules_y_top)

    if rocket_modules_x_left != [] and rocket_modules_x_right != []:
        x_left = min(rocket_modules_x_left)
        x_right = max(rocket_modules_x_right)

    return y_bottom, y_top, x_left, x_right


def render_rocket_surface():
    rocket.surface = pygame.Surface((rocket_surface_widht, rocket_surface_heigth))
    for rocket_module in rocket.list:
        rocket_module.x = rocket_module.x - x_left
        rocket_module.y = rocket_module.y - y_top
        rocket.surface.blit(rocket_module, (rocket_module.x, rocket_module.y))

    return rocket.surface

y_bottom, y_top, x_left, x_right = find_max_coord(rocket_list)
rocket_surface_heigth, rocket_surface_widht = y_bottom-y_top, x_right-x_left

rocket = Rocket()
rocket.list = rocket_list
rocket.surface = render_rocket_surface()



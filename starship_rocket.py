import pygame
from draw_constructor import rocket_list, rocket_surface

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
    angle = 0
    vx = 0
    vy = 0
    omega = 0


rocket = Rocket()
rocket.list = rocket_list
rocket.surface = rocket_surface

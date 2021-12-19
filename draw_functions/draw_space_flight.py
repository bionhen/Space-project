from draw_functions.space_flight import *
from draw_functions.space_obj import *
from draw_functions.starship_rocket import *

pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

BLUE = (39, 40, 91)
LIGHT_BLUE = (106, 139, 197)

clock = pygame.time.Clock()
FPS = 30

FONT = pygame.font.SysFont('century gothic', 30, bold=True)
FONT_small = pygame.font.SysFont('century gothic', 24, bold=True)
pygame.font.init()

time_step_space = 0
e = 0
m = 0


def render_bg():
    """Функция генерирует составляющие фона.
    :returns: bg_constructor_surf_arg - поверхность заднего фона
    """
    bg_space_flight_surf_arg = pygame.Surface((800, 600))
    bg_space_flight_surf_arg.fill((30, 33, 61))
    return bg_space_flight_surf_arg


def draw_objects(space_objects_arg, bg_space_flight_surf_arg):
    """
    Функция рисует все объекты на поверхности заднего фона
    :param space_objects_arg: - лист космических объектов
    :param bg_space_flight_surf_arg: - поверхность заднего фона
    """
    for object_arg in space_objects_arg:
        if object_arg != Rocket_Obj:
            bg_space_flight_surf_arg.blit(object_arg.image, ((object_arg.x - object_arg.R) / 10 ** 6,
                                                             (object_arg.y - object_arg.R) / 10 ** 6))


def draw_rotate(bg_space_flight_surf_arg, rocket_arg):
    """
    Функция поворачивает ракету и рисует ее
    :param bg_space_flight_surf_arg: - поверхность заднего фона
    :param rocket_arg: - сама ракета
    """
    pos_rocket = 2.5, 5
    center_rocket = (rocket_arg.x/10**6, rocket_arg.y/10**6)
    rocket1 = Rocket_Obj.image
    w_rocket, h_rocket = rocket1.get_size()
    rocket2 = pygame.Surface((2 * w_rocket, 2 * h_rocket), pygame.SRCALPHA)
    rocket2.blit(rocket1, (w_rocket - pos_rocket[0], h_rocket - pos_rocket[1]))
    rocket_rotated = pygame.transform.rotate(rocket2, rocket_arg.angle)
    rect_rocket = rocket_rotated.get_rect()
    rect_rocket.center = center_rocket

    bg_space_flight_surf_arg.blit(rocket_rotated, rect_rocket)


def draw_fuel(bg_flight_surf_arg, rocket_arg, rocket_fuel_max_arg):
    """Функция рисует текущее состояние топлива.
    :param bg_flight_surf_arg - поверхность, на которой рисуется состояние
    :param rocket_arg - ракета, элемент класса Rocket
    :param rocket_fuel_max_arg - максимальный уровень топлива ракеты (в начале)"""
    fuel_bar_height = 200
    fuel_bar_width = 50
    fuel_bar_pos_x = 50
    fuel_bar_pos_y = 310
    fuel_per = rocket_arg.fuel * (100 / rocket_fuel_max_arg)
    fuel_per_height = (fuel_bar_height / 100 * fuel_per)
    fuel_image = pygame.Surface((fuel_bar_width, fuel_per_height))
    fuel_max_image = pygame.Surface((fuel_bar_width, fuel_bar_height))
    fuel_max_image.fill(LIGHT_BLUE)
    if 75 < fuel_per:
        fuel_image.fill('aquamarine4')
    if 50 < fuel_per <= 75:
        fuel_image.fill('yellow')
    elif 25 < fuel_per <= 50:
        fuel_image.fill('orange')
    elif 0 < fuel_per <= 25:
        fuel_image.fill('tomato')

    if rocket_arg.fuel > 0:
        fuel_quantity = round(rocket_arg.fuel, 1)
    else:
        fuel_quantity = 0

    fuel_text = FONT_small.render('fuel: ' + str(fuel_quantity) + 'kg', True, LIGHT_BLUE)

    bg_flight_surf_arg.blit(fuel_max_image, (fuel_bar_pos_x, fuel_bar_pos_y))
    bg_flight_surf_arg.blit(fuel_image, (fuel_bar_pos_x, fuel_bar_pos_y + 100 + (100 - fuel_per_height)))
    bg_flight_surf_arg.blit(fuel_text, (fuel_bar_pos_x - 25, fuel_bar_pos_y + 200))


Earth = Object()
Earth.type = 'planet'
Earth.m = 6 * 10 ** 24
Earth.x = 300 * 10 ** 6
Earth.y = 300 * 10 ** 6
Earth.Vx = 0
Earth.Vy = 0
Earth.Fx = 0
Earth.Fy = 0
Earth.R = 15 * 10 ** 6
Earth.image = pygame.image.load("images/space_flight/earth_above.png")
Earth.image = pygame.transform.scale(Earth.image, (30, 30))
Earth.angle = 0
Earth.omega = 0

Moon = Object()
Moon.type = 'planet'
Moon.m = 7.35 * 10 ** 22
Moon.x = 562 * 10 ** 6
Moon.y = 300 * 10 ** 6
Moon.Vx = 0
Moon.Vy = -1020
Moon.Fx = 0
Moon.Fy = 0
Moon.R = 10 * 10 ** 6
Moon.image = pygame.image.load("images/space_flight/moon_1.png")
Moon.image = pygame.transform.scale(Moon.image, (20, 20))
Moon.angle = 0
Moon.omega = 0

Rocket_Obj = Object()
Rocket_Obj.type = 'rocket'
Rocket_Obj.m = 0
Rocket_Obj.x = 320 * 10 ** 6
Rocket_Obj.y = 300 * 10 ** 6
Rocket_Obj.Vx = 0
Rocket_Obj.Vy = (G * Earth.m / (20 * 10 ** 6)) ** 0.5
Rocket_Obj.Fx = 0
Rocket_Obj.Fy = 0
Rocket_Obj.R = 0
Rocket_Obj.image = pygame.Surface((10, 10), pygame.SRCALPHA)
pygame.draw.polygon(Rocket_Obj.image, 'tomato', ((0, 10), (5, 0), (10, 10)))
Rocket_Obj.angle = 0
Rocket_Obj.omega = 0
Rocket_Obj.fuel = calculate_m_fuel(Rocket_Obj)
space_objects = [Earth, Moon, Rocket_Obj]


def draw_space_flight_foo(rocket_arg, flag_forward_arg, flag_left_arg, flag_right_arg, space_objects_arg):
    m_arg = 0
    Rocket_Obj.fuel = rocket_arg.fuel
    Rocket_Obj.list = rocket_arg.list
    bg_space_flight_surf_arg = render_bg()
    for module in rocket_arg.list:
        m_arg += module.m
    Rocket_Obj.m = m_arg
    draw_objects(space_objects_arg, bg_space_flight_surf_arg)
    recalculate_space_objects_positions(space_objects_arg, 200, flag_forward_arg, flag_left_arg, flag_right_arg)
    calc_list_arg = calculation_orbit(Rocket_Obj, space_objects, 100)
    draw_rotate(bg_space_flight_surf_arg, Rocket_Obj)
    for i_arg in range(len(calc_list_arg)):
        if i_arg + 1 < len(calc_list_arg):
            pygame.draw.line(bg_space_flight_surf_arg, (255, 255, 255), calc_list_arg[i_arg], calc_list_arg[i_arg + 1])
    sc.blit(bg_space_flight_surf_arg, (0, 0))
    calc_list_1 = calculation_orbit(Moon, space_objects_arg, 1000)
    for i_arg in range(len(calc_list_1)):
        if i_arg + 1 < len(calc_list_1):
            pygame.draw.line(bg_space_flight_surf_arg, (255, 255, 255),  calc_list_1[i_arg], calc_list_1[i_arg + 1])
    rocket_arg.fuel = Rocket_Obj.fuel


if __name__ == '__main__':
    print("This module is not for a direct call!")

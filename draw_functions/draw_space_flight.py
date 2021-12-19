import pygame
from draw_functions.space_flight import *
from draw_functions.space_obj import *
from draw_functions.starship_rocket import *
#from draw_flight import rocket_fuel_max

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
    :returns
    bg_flight_surf - поверхность данного слайда игры
    cosmodrom - изображение космодрома
    ground - изображение земли
    earth - изображение Земли на панели сбоку
    space - изображение космоса на панели сбоку"""
    bg_space_flight_surf = pygame.Surface((800, 600))
    bg_space_flight_surf.fill((30, 33, 61))
    return bg_space_flight_surf  # , cosmodrom, ground, earth, space


"""def render_earth():
    earth_images = []
    for n in range(1, 13):
        earth = pygame.image.load('images/space_flight/earth_'+str(n)+'.png')
        earth = pygame.transform.scale(earth, (100, 100))
        earth_images.append(earth)
    return earth_images"""

"""def render_moon():
    moon_images = []
    for n in range(1, 20):
        moon = pygame.image.load('images/space_flight/moon_'+str(n)+'.png')
        moon = pygame.transform.scale(moon, (30, 30))
        moon_images.append(moon)
    return moon_images"""


def draw_objects(space_objects, bg_space_flight_surf):
    for object in space_objects:
        if object != Rocket_Obj:
            bg_space_flight_surf.blit(object.image, ((object.x - object.R) / 10 ** 6, (object.y - object.R) / 10 ** 6))
        #if object == Earth:
            #print('coord', (object.x - object.R) / 10 ** 6, (object.y - object.R) / 10 ** 6)


"""def draw_earth(bg_space_flight_surf, earth_images):
    global e
    global time_step_space
    if time_step_space % 5 == 0:
        e += 1
    if e % 12 == 0:
        e = 0
    bg_space_flight_surf.blit(earth_images[e], (200, 250))"""

"""def draw_moon(bg_space_flight_surf, moon_images):
    global m
    global time_step_space
    if time_step_space % 3 == 0:
        m += 1
    if m % 19 == 0:
        m = 0
    bg_space_flight_surf.blit(moon_images[m], (500, 250))"""


def draw_rotate(bg_space_flight_surf, rocket):
    pos_rocket = 2.5, 5
    center_rocket = (rocket.x/10**6, rocket.y/10**6)
    rocket1 = Rocket_Obj.image
    #rocket1 = pygame.transform.scale(rocket1, (25, 50))
    w_rocket, h_rocket = rocket1.get_size()
    rocket2 = pygame.Surface((2 * w_rocket, 2 * h_rocket), pygame.SRCALPHA)
    rocket2.blit(rocket1, (w_rocket - pos_rocket[0], h_rocket - pos_rocket[1]))
    rocket_rotated = pygame.transform.rotate(rocket2, rocket.angle)
    rect_rocket = rocket_rotated.get_rect()
    rect_rocket.center = center_rocket

    bg_space_flight_surf.blit(rocket_rotated, rect_rocket)

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


def draw_space_flight_foo(rocket, flag_forward, flag_left, flag_right, space_objects):
    m = 0
    Rocket_Obj.fuel = rocket.fuel
    Rocket_Obj.list = rocket.list
    bg_space_flight_surf = render_bg()
    for module in rocket.list:
        print(rocket.list)
        m += module.m
    print(m)
    Rocket_Obj.m = m
    draw_objects(space_objects, bg_space_flight_surf)
    print('2', flag_forward, flag_left, flag_right)
    recalculate_space_objects_positions(space_objects, 200, flag_forward, flag_left, flag_right)
    calc_list = calculation_orbit(Rocket_Obj, space_objects, 100)
    draw_rotate(bg_space_flight_surf, Rocket_Obj)
    for i in range(len(calc_list)):
        if i + 1 < len(calc_list):
            pygame.draw.line(bg_space_flight_surf, (255, 255, 255), calc_list[i], calc_list[i + 1])
    sc.blit(bg_space_flight_surf, (0, 0))
    calc_list_1 = calculation_orbit(Moon, space_objects, 1000)
    print(calc_list_1)
    for i in range(len(calc_list_1)):
        if i + 1 < len(calc_list_1):
            pygame.draw.line(bg_space_flight_surf, (255, 255, 255),  calc_list_1[i], calc_list_1[i + 1])
    rocket.fuel = Rocket_Obj.fuel



if __name__ == '__main__':
    flag_left = flag_right = False
    flag_forward = False
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
    Rocket_Obj.image = pygame.Surface((5, 10), pygame.SRCALPHA)
    pygame.draw.polygon(Rocket_Obj.image, 'tomato', ((0, 10), (2.5, 0), (5, 10)))
    Rocket_Obj.list = rocket.list
    Rocket_Obj.angle = 0
    Rocket_Obj.omega = 0
    Rocket_Obj.fuel = calculate_m_fuel(Rocket_Obj)
    space_objects = [Earth, Moon, Rocket_Obj]

    rocket_fuel_max = Rocket_Obj.fuel
    while True:
        Earth.Vx = Earth.Vy = 0
        bg_space_flight_surf = render_bg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    flag_forward = True
                if event.key == pygame.K_LEFT:
                    flag_left = True
                if event.key == pygame.K_RIGHT:
                    flag_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    flag_forward = False
                if event.key == pygame.K_LEFT:
                    flag_left = False
                if event.key == pygame.K_RIGHT:
                    flag_right = False
        draw_objects(space_objects, bg_space_flight_surf)

        recalculate_space_objects_positions(space_objects, 200, flag_forward, flag_left, flag_right)
        # draw_earth(bg_space_flight_surf, earth_images)
        # draw_moon(bg_space_flight_surf, moon_images)

        calc_list = calculation_orbit(Rocket_Obj, space_objects, 100)
        for i in range(len(calc_list)):
            if i + 1 < len(calc_list):
                pygame.draw.line(bg_space_flight_surf, (255, 255, 255),
                                 calc_list[i],
                                 calc_list[i + 1])
                print(calc_list[i])
        sc.blit(bg_space_flight_surf, (0, 0))

        calc_list = calculation_orbit(Moon, space_objects, 1000)
        for i in range(len(calc_list)):
            if i + 1 < len(calc_list):
                pygame.draw.line(bg_space_flight_surf, (255, 255, 255),
                                 calc_list[i],
                                 calc_list[i + 1])
                print(calc_list[i])

        draw_fuel(bg_space_flight_surf, Rocket_Obj, rocket_fuel_max)
        draw_roctate(bg_space_flight_surf, Rocket_Obj)
        sc.blit(bg_space_flight_surf, (0, 0))
        #print(calc_list)

        pygame.display.update()

        clock.tick(FPS)

        time_step_space += 1
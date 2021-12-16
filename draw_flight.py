import pygame
from starship_rocket import *
from starship_flight import *

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

time_step = 0
i = 0
j = 0

def render_bg():
    """Функция генерирует составляющие фона.
    :returns
    bg_flight_surf - поверхность данного слайда игры
    cosmodrom - изображение космодрома
    ground - изображение земли
    earth - изображение Земли на панели сбоку
    space - изображение космоса на панели сбоку"""
    bg_flight_surf = pygame.Surface((800, 600))
    cosmodrom = pygame.image.load(("images/flight/cosmodrom.png")).convert_alpha()
    cosmodrom = pygame.transform.scale(cosmodrom, (300, 375))
    ground = pygame.image.load(("images/flight/ground.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (800, 80))
    earth = pygame.image.load(("images/flight/earth.png")).convert_alpha()
    earth = pygame.transform.scale(earth, (20, 20))
    space = pygame.image.load(("images/flight/space.png")).convert_alpha()
    space = pygame.transform.scale(space, (20, 20))

    return bg_flight_surf, cosmodrom, ground, earth, space

def draw_bg(bg_flight_surf, cosmodrom, ground):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_flight_surf.blit(cosmodrom, (250, 200 + (h - 6400000) * 15))
    bg_flight_surf.blit(ground, (0, 525 + (h - 6400000) * 15))
    #sc.blit(bg_flight_surf, (0, 0))


def render_fire():
    """Функция генерирует массивыы изображений огней.
    :returns
    fire_big - огни для центральных двигателей
    fire_small - огни для боковых двигателей"""
    fire_big = [pygame.image.load('images/flight/fire/fire1.png'), pygame.image.load('images/flight/fire/fire2.png'),
                pygame.image.load('images/flight/fire/fire3.png'), pygame.image.load('images/flight/fire/fire4.png'),
                pygame.image.load('images/flight/fire/fire5.png')]
    fire_small = [pygame.image.load('images/flight/fire/fire9.png'), pygame.image.load('images/flight/fire/fire8.png'),
                pygame.image.load('images/flight/fire/fire7.png'), pygame.image.load('images/flight/fire/fire6.png')]
    return fire_big, fire_small


def draw_fire(img, fire_big, fire_small,
              flag_forward, flag_left, flag_right, engines_cord, engines_left_cord, engines_right_cord):
    """Функция рисует огни у ракеты.
    :param img - повернхность, на которой отображается огонь
    :param fire_big - массив огней для центральных двигателей
    :param fire_small - массив огней для центральных двигателей
    :param flag_forward - флаг движения вперёд
    :param flag_left - флаг движения налево
    :param flag_right - флаг движения направо
    :param engines_cord - массив кординат центральных двигателей
    :param engines_left_cord - массив кординат левых двигателей
    :param engines_right_cord - массив кординат правых двигателей"""
    global i
    global j
    global time_step
    if flag_forward:
        if time_step % 2 == 0:
            i += 1
        if i % 5 == 0:
            i = 0
        for k in range(len(engines_cord)):
            img.blit(fire_big[i], (engines_cord[k][0], engines_cord[k][1] + engines_cord[k][2]))
    if flag_left:
        if time_step % 2 == 0:
            j += 1
        if j % 4 == 0:
            j = 0
        for k in range(len(engines_left_cord)):
            img.blit(fire_small[j], (engines_left_cord[k][0], engines_left_cord[k][1] + engines_left_cord[k][2]))
    if flag_right:
        if time_step % 2 == 0:
            j += 1
        if j % 4 == 0:
            j = 0
        for k in range(len(engines_right_cord)):
            img.blit(fire_small[j], (engines_right_cord[k][0], engines_right_cord[k][1] + engines_right_cord[k][2]))

def draw_rotate(rocket, fire_big, fire_small, flag_forward, flag_left, flag_right, engines_cord, engines_left_cord, engines_right_cord):
    """Эта функция поворачивает картинку на заданный угол относительно заданного центра вращения
    :param rocket: ракета, элемент класса Rocket
    :param pos: координаты центра вращения на изображении
    :param center: координаты центра поверхности на экране
    :param angle: тот самый заданный угол поворота
    :returns: повернутое изображение и координаты точки, где его надо нарисовать"""

    x_center_mass, y_center_mass = find_center_mass(rocket)
    angle = rocket.angle
    pos = x_center_mass, y_center_mass
    center = (400, 520 - rocket_surface_height + 50 + y_center_mass)
    w, h = rocket_surface_widht, rocket_surface_height
    if rocket.fuel > 0:
        draw_fire(rocket.surface, fire_big, fire_small, flag_forward, flag_left, flag_right, engines_cord, engines_left_cord, engines_right_cord)
    img2 = pygame.Surface((2*w, 2*h), pygame.SRCALPHA)
    img2.blit(rocket.surface, (w - pos[0], h - pos[1]))
    img4 = pygame.transform.rotate(img2, angle)
    rect = img4.get_rect()
    rect.center = center

    return img4, rect


def draw_rocket(img4, rect, bg_flight_surf):
    """Функция рисует ракету.
    :param img4 - обновлённое изображение ракеты
    :param rect - координаты, где нужно рисовать ракету
    :param bg_flight_surf - поверхность, на которой рисуется ракета"""
    bg_flight_surf.blit(img4, rect)


def draw_fuel(bg_flight_surf, rocket, rocket_fuel_max):
    """Функция рисует текущее состояние топлива.
    :param bg_flight_surf - поверхность, на которой рисуется состояние
    :param rocket - ракета, элемент класса Rocket
    :param rocket_fuel_max - максимальный уровень топлива ракеты (в начале)"""
    #FIXME сделать всплывающую плашку "закончилось топливо"
    fuel_per = rocket.fuel*(100/rocket_fuel_max)
    fuel_per_height = (200 / 100 * fuel_per)
    fuel_status_image = pygame.Surface((50, fuel_per_height))
    fuel_max_image = pygame.Surface((50, 200))
    fuel_max_image.fill(LIGHT_BLUE)
    if 75 < fuel_per:
        fuel_status_image.fill('aquamarine4')
    if 50 < fuel_per <= 75:
        fuel_status_image.fill('yellow')
    elif 25 < fuel_per <= 50:
        fuel_status_image.fill('orange')
    elif 0 < fuel_per <= 25:
        fuel_status_image.fill('tomato')
    if rocket.h < 20000 + 6400000 and rocket.fuel > 0:
        fuel_text = FONT_small.render('fuel: '+str(round(rocket.fuel, 1))+' kg', True, BLUE)
    if rocket.h >= 20000 + 6400000 and rocket.fuel > 0:
        fuel_text = FONT_small.render('fuel: '+str(round(rocket.fuel, 1))+' kg', True, LIGHT_BLUE)
    if rocket.h < 20000 + 6400000 and rocket.fuel <= 0:
        fuel_text = FONT_small.render('fuel: '+str(0)+' kg', True, BLUE)
    if rocket.h >= 20000 + 6400000 and rocket.fuel <= 0:
        fuel_text = FONT_small.render('fuel: '+str(0)+' kg', True, LIGHT_BLUE)
    bg_flight_surf.blit(fuel_max_image, (50, 310))
    bg_flight_surf.blit(fuel_status_image, (50, 410+(100 - fuel_per_height)))
    bg_flight_surf.blit(fuel_text, (50 - 25, 510))


def draw_height(bg_flight_surf, rocket, earth, space):
    """Функция рисует текущую высоту ракеты.
    :param bg_flight_surf - поверхность, на которой рисуется состояние
    :param rocket - ракета, элемент класса Rocket
    :param earth - картинка земли
    :param - space - картинка космоса
    """
    # FIXME сделать всплывающую плашку "вы достигли космоса"
    cosmos_height_per = 100 * (rocket.h - 6400000) / 100000
    cosmos_height_stick = pygame.Surface((5, 300))
    cosmos_height_roll = pygame.Surface((15, 5))
    cosmos_height_stick.fill('white')
    cosmos_height_roll.fill(BLUE)
    bg_flight_surf.blit(cosmos_height_stick, (750, 160))
    if rocket.h < 20000 + 6400000:
        cosmos_text = FONT_small.render('height: ' + str(abs(round((rocket.h - 6400000)/1000, 1))) + ' km', True, BLUE)
    if rocket.h >= 20000 + 6400000:
        cosmos_text = FONT_small.render('height: ' + str(abs(round((rocket.h - 6400000)/1000, 1))) + ' km', True, LIGHT_BLUE)

    if cosmos_height_per < 100:
        bg_flight_surf.blit(cosmos_height_roll, (750 - 5, 160 + 300 - (300 / 100 * cosmos_height_per)))
    else:
            bg_flight_surf.blit(cosmos_height_roll, (750 - 5, 160))
    bg_flight_surf.blit(earth, (743, 470))
    bg_flight_surf.blit(space, (743, 130))
    bg_flight_surf.blit(cosmos_text, (610, 510))


def draw_speed(bg_flight_surf, rocket):
    """Функция рисует текущую скорость ракеты.
    :param bg_flight_surf - поверхность, на которой рисуется состояние
    :param rocket - ракета, элемент класса Rocket"""
    # FIXME сделать всплывающую плашку "вы достигли первой комической скорости"
    speed = (rocket.vx**2 + rocket.vy**2)**0.5
    #v_1 = 6.67 * 10**(-11) * 6 * 10**24 / rocket.h
    speed_per = speed*(100/7910)
    speed_per_height = (200 / 100 * speed_per)
    speed_image = pygame.Surface((50, speed_per_height))
    speed_image_max = pygame.Surface((50, 200))
    speed_image_max.fill(LIGHT_BLUE)
    speed_image.fill('tomato')
    if rocket.h < 20000 + 6400000:
        speed_text = FONT_small.render('speed: ' + str(round(speed, 1)) + ' m/c', True, BLUE)
        speed_vx_text = FONT_small.render('speed vx: ' + str(abs(round(rocket.vx, 1))) + ' m/c', True, BLUE)
        speed_vy_text = FONT_small.render('speed vy: ' + str(round(rocket.vy, 1)) + ' m/c', True, BLUE)
    if rocket.h >= 20000 + 6400000:
        speed_text = FONT_small.render('speed: ' + str(round(speed, 1)), True, LIGHT_BLUE)
        speed_vx_text = FONT_small.render('speed vx: ' + str(abs(round(rocket.vx, 1)))  + ' m/c', True, LIGHT_BLUE)
        speed_vy_text = FONT_small.render('speed vy: ' + str(abs(round(rocket.vy, 1))) + ' m/c', True, LIGHT_BLUE)
    bg_flight_surf.blit(speed_image_max, (50, 90))
    if speed_per < 100:
        bg_flight_surf.blit(speed_image, (50, 90+(200 - speed_per_height)))
    else:
        speed_image = pygame.Surface((50, 200))
        speed_image.fill('tomato')
        bg_flight_surf.blit(speed_image, (50, 90))

    bg_flight_surf.blit(speed_text, (25, 55))
    bg_flight_surf.blit(speed_vx_text, (25, 10))
    bg_flight_surf.blit(speed_vy_text, (25, 30))

def draw_angle(bg_flight_surf, rocket):
    """Функция рисует текущий угол ракеты.
    :param bg_flight_surf - поверхность, на которой рисуется состояние
    :param rocket - ракета, элемент класса Rocket"""
    #FIXME поправить периодичность угла
    if rocket.h <= 6400000 + 100000:
        angle_ideal = - 180 / (2 * 100000) * (rocket.h - 6400000)
    else:
        angle_ideal = - 90
    angle_difference = angle_ideal - rocket.angle
    pos_angle = 25, 50
    center_angle = (760, 110)
    angle1 = pygame.image.load("images/flight/angle.png")
    angle1 = pygame.transform.scale(angle1, (25, 50))
    w_angle, h_angle = angle1.get_size()
    angle2 = pygame.Surface((2*w_angle, 2*h_angle), pygame.SRCALPHA)
    angle2.blit(angle1, (w_angle - pos_angle[0], h_angle - pos_angle[1]))
    angle4 = pygame.transform.rotate(angle2, angle_ideal)
    rect_angle = angle4.get_rect()
    rect_angle.center = center_angle
    if rocket.h < 20000 + 6400000:
        angle_text = FONT_small.render('deviation: ' + str(abs(round(angle_difference, 1))), True, BLUE)
    if rocket.h >= 20000 + 6400000:
        angle_text = FONT_small.render('deviation: ' + str(abs(round(angle_difference, 1))), True, LIGHT_BLUE)

    bg_flight_surf.blit(angle4, rect_angle)
    bg_flight_surf.blit(angle_text, (615, 20))


def fill_gradient(bg_flight_surf, h):
    """Функция рисует градиентный фон в зависимости от высоты.
    :param bg_flight_surf - поверхность, на которой рисуется состояние
    :param h - высота ракеты"""
    if h <= 6400000 + 30000:
        color1 = int(127 - (127-30)/30000 * (h-6400000))
        color2 = int(199 - (199-33)/30000 * (h-6400000))
        color3 = int(255 - (255-61)/30000 * (h-6400000))
        bg_flight_surf.fill((color1, color2, color3))
    else:
        bg_flight_surf.fill((30, 33, 61))


def draw_flight_foo(rocket, events, flag_forward, flag_left, flag_right, rocket_fuel_max):
    bg_flight_surf, cosmodrom, ground, earth, space = render_bg()
    fire_big = render_fire()
    if events[0] == "key_down" and events[1] == "forward":
        flag_forward = True
    if events[0] == "key_down" and events[1] == "left":
        flag_left = True
    if events[0] == "key_down" and events[1] == "right":
        flag_right = True
    if events[0] == "key_up" and events[1] == "forward":
        flag_forward = False
    if events[0] == "key_up" and events[1] == "left":
        flag_left = False
    if events[0] == "key_up" and events[1] == "right":
        flag_right = False
    h = rocket.h
    rocket_move(rocket, flag_left, flag_right, flag_forward)
    fill_gradient(bg_flight_surf, h)
    draw_fuel(bg_flight_surf, rocket, rocket_fuel_max)
    draw_height(bg_flight_surf, rocket, earth, space)
    draw_speed(bg_flight_surf, rocket)
    draw_angle(bg_flight_surf, rocket)
    draw_bg(bg_flight_surf, cosmodrom, ground)
    draw_fire(rocket, fire_big, flag_forward)
    draw_rocket(rocket, bg_flight_surf)
    sc.blit(bg_flight_surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
    # time_step += 1
    return rocket, flag_forward, flag_left, flag_right, rocket_fuel_max


h = 6400000
flag_left = flag_right = False
flag_forward = False

if __name__ == '__main__':
    fuel_calc(rocket)
    bg_flight_surf, cosmodrom, ground, earth, space = render_bg()
    rocket_fuel_max = rocket.fuel
    fire_big, fire_small = render_fire()

    while True:
        y_bottom, y_top, x_left, x_right = find_max_coord(rocket.list)
        rocket_surface_height, rocket_surface_widht = y_bottom - y_top + 50, x_right - x_left
        rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, x_left, y_top, rocket)
        img4, rect = draw_rotate(rocket, fire_big, fire_small, flag_forward, flag_left, flag_right, engines_cord,
                                 engines_left_cord, engines_right_cord)

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

        h = rocket.h

        rocket_move(rocket, flag_left, flag_right, flag_forward)

        fill_gradient(bg_flight_surf, h)

        draw_fuel(bg_flight_surf, rocket, rocket_fuel_max)
        draw_height(bg_flight_surf, rocket, earth, space)
        draw_speed(bg_flight_surf, rocket)
        draw_angle(bg_flight_surf, rocket)

        draw_bg(bg_flight_surf, cosmodrom, ground)

        draw_rocket(img4, rect, bg_flight_surf)

        sc.blit(bg_flight_surf, (0, 0))
        pygame.display.update()

        clock.tick(FPS)
        time_step += 1
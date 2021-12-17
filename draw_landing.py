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


def render_moon_plate():
    """Функция генерирует составляющие фона.
    :returns
    bg_flight_surf - поверхность данного слайда игры
    cosmodrom - изображение космодрома
    ground - изображение земли
    moon - изображение Земли на панели сбоку
    space - изображение космоса на панели сбоку"""
    x = 0
    moon_coords = []
    while x <= 2400:
        y = randint(250, 350)
        moon_coords.append((x, y))
        x += 100

    moon_plate = pygame.Surface((2400, 350), pygame.SRCALPHA)
    pygame.draw.polygon(moon_plate, 'beige', ((0, 0), (0, 350), moon_coords[1], moon_coords[2], moon_coords[3],
                                              moon_coords[4], moon_coords[5], moon_coords[6], moon_coords[7],
                                              moon_coords[8], moon_coords[9], moon_coords[10], moon_coords[11],
                                              moon_coords[12], moon_coords[13], moon_coords[14], moon_coords[15],
                                              moon_coords[16], moon_coords[17], moon_coords[18], moon_coords[19],
                                              moon_coords[20], moon_coords[21], moon_coords[22], moon_coords[23],
                                              moon_coords[24], (2400, 0)))
    moon_plate = pygame.transform.flip(moon_plate, False, True)

    return moon_coords, moon_plate


def render_img():
    moon_arg = pygame.image.load("images/flight/moon.png").convert_alpha()
    moon_arg = pygame.transform.scale(moon_arg, (20, 20))
    space_arg = pygame.image.load("images/flight/space.png").convert_alpha()
    space_arg = pygame.transform.scale(space_arg, (20, 20))
    return moon_arg, space_arg


def render_bg():
    bg_landing_surf = pygame.Surface((800, 600))
    bg_landing_surf.fill((30, 33, 61))
    return bg_landing_surf


def draw_bg(moon_plate, bg_landing_surf, rocket):
    bg_landing_surf.blit(moon_plate, (-1000 + rocket.vx, 350 + rocket.h-6400000))


def calc_cords_and_angles(moon_cords):
    moon_angles_sin = []
    for i in len(moon_cords):
        moon_angles_sin.append((moon_cords[i+1][1] - moon_cords[i][1])/(moon_cords[i+1][0] - moon_cords[i][0]))
    return moon_angles_sin

#def cheack_landing(rocket.h)


def render_fire():
    """Функция генерирует массивыы изображений огней.
    :returns
    fire_big - огни для центральных двигателей
    fire_small - огни для боковых двигателей"""
    fire_big_arg = []
    fire_small_arg = []
    for fb in range(1, 6):
        fire1 = pygame.image.load('images/flight/fire/fire' + str(fb) + '.png')
        fire1 = pygame.transform.scale(fire1, (25, 25))
        fire_big_arg.append(fire1)
    for fs in range(6, 10):
        fire2 = pygame.image.load('images/flight/fire/fire' + str(fs) + '.png')
        fire2 = pygame.transform.scale(fire2, (25, 25))
        fire_small_arg.append(fire2)
    return fire_big_arg, fire_small_arg


def draw_fire(img_arg, fire_big_arg, fire_small_arg,
              flag_forward_arg, flag_left_arg, flag_right_arg, engines_cord_arg, engines_left_cord_arg,
              engines_right_cord_arg, fire_big_step_arg, fire_small_step_arg, time_step_arg):
    """Функция рисует огни у ракеты.
    :param img_arg - повернхность, на которой отображается огонь
    :param fire_big_arg - массив огней для центральных двигателей
    :param fire_small_arg - массив огней для центральных двигателей
    :param flag_forward_arg - флаг движения вперёд
    :param flag_left_arg - флаг движения налево
    :param flag_right_arg - флаг движения направо
    :param engines_cord_arg - массив кординат центральных двигателей
    :param engines_left_cord_arg - массив кординат левых двигателей
    :param engines_right_cord_arg - массив кординат правых двигателей
    :param fire_big_step_arg - счётчик отображения больших огней
    :param fire_small_step_arg - счётчик отображения маленьких огней
    :param time_step_arg - счётчик времени"""
    if flag_forward_arg:
        if time_step_arg % 5 == 0:
            fire_big_step_arg += 1
        if fire_big_step_arg % 5 == 0:
            fire_big_step_arg = 0
        for ce in range(len(engines_cord_arg)):
            img_arg.blit(fire_big_arg[fire_big_step_arg], (engines_cord_arg[ce][0]/2,
                                                           engines_cord_arg[ce][1]/2
                                                           + engines_cord_arg[ce][2]/2))
            fire_big_step_arg += 1

    if flag_left_arg:
        if time_step_arg % 2 == 0:
            fire_small_step_arg += 1
        if fire_small_step_arg % 4 == 0:
            fire_small_step_arg = 0
        for le in range(len(engines_left_cord_arg)):
            img_arg.blit(fire_small[fire_small_step_arg], (engines_left_cord_arg[le][0]/2,
                                                           engines_left_cord_arg[le][1]/2
                                                           + engines_left_cord_arg[le][2]/2))
        fire_small_step_arg += 1

    if flag_right_arg:
        if time_step_arg % 2 == 0:
            fire_small_step_arg += 1
        if fire_small_step_arg % 4 == 0:
            fire_small_step_arg = 0
        for re in range(len(engines_right_cord_arg)):
            img_arg.blit(fire_small_arg[fire_small_step_arg], (engines_right_cord_arg[re][0]/2,
                                                               engines_right_cord_arg[re][1]/2 +
                                                               engines_right_cord_arg[re][2]/2))
        fire_big_step_arg += 1


def draw_rotate(rocket_arg, fire_big_arg, fire_small_arg, flag_forward_arg, flag_left_arg, flag_right_arg,
                engines_cord_arg,
                engines_left_cord_arg, engines_right_cord_arg, fire_big_step_arg, fire_small_step_arg, time_step_arg,
                rocket_surface_width, rocket_surface_height):
    """
    :param rocket_arg - повернхность, на которой отображается огонь
    :param fire_big_arg - массив огней для центральных двигателей
    :param fire_small_arg - массив огней для центральных двигателей
    :param flag_forward_arg - флаг движения вперёд
    :param flag_left_arg - флаг движения налево
    :param flag_right_arg - флаг движения направо
    :param engines_cord_arg - массив кординат центральных двигателей
    :param engines_left_cord_arg - массив кординат левых двигателей
    :param engines_right_cord_arg - массив кординат правых двигателей
    :param fire_big_step_arg - счётчик отображения больших огней
    :param fire_small_step_arg - счётчик отображения маленьких огней
    :param time_step_arg - счётчик времени"""

    x_center_mass, y_center_mass = find_center_mass(rocket)
    x_center_mass, y_center_mass = int(x_center_mass/2), int(y_center_mass/2)
    angle = rocket_arg.angle
    pos = x_center_mass, y_center_mass
    rocket_surface_width = int(rocket_surface_width / 2)
    rocket_surface_height = int(rocket_surface_height / 2)
    rocket_arg.surface = pygame.transform.scale(rocket_arg.surface, (rocket_surface_width, rocket_surface_height))
    center = (400, 450 - rocket_surface_height + y_center_mass)  # откуда берётся высота ракеты
    if rocket_arg.fuel > 0:
        draw_fire(rocket_arg.surface, fire_big_arg, fire_small_arg, flag_forward_arg, flag_left_arg, flag_right_arg,
                  engines_cord_arg, engines_left_cord_arg, engines_right_cord_arg, fire_big_step_arg,
                  fire_small_step_arg, time_step_arg)
    img2 = pygame.Surface((2 * rocket_surface_width, 2 * rocket_surface_height), pygame.SRCALPHA)
    img2.blit(rocket_arg.surface, (rocket_surface_width - pos[0], rocket_surface_height - pos[1]))
    rocket_rotated_arg = pygame.transform.rotate(img2, angle)
    print('angle', angle)
    rect_arg = rocket_rotated_arg.get_rect()
    rect_arg.center = center

    return rocket_rotated_arg, rect_arg


def draw_rocket(bg_landing_surf_arg, rocket_rotated_arg, rect_arg):
    """Функция рисует ракету.
    :param rocket_rotated_arg - обновлённое изображение ракеты
    :param rect_arg - координаты, где нужно рисовать ракету
    :param bg_landing_surf_arg - поверхность, на которой рисуется ракета"""
    bg_landing_surf_arg.blit(rocket_rotated_arg, rect_arg)


def change_font_color(rocket_arg, parametr_arg, quantity_arg, measure_arg):
    text = FONT_small.render(' ', True, BLUE)
    if rocket_arg.h < 20000 + 6400000:
        text = FONT_small.render(parametr_arg + ': ' + str(quantity_arg) + ' ' + measure_arg, True, LIGHT_BLUE)
    if rocket.h >= 20000 + 6400000:
        text = FONT_small.render(parametr_arg + ': ' + str(quantity_arg) + ' ' + measure_arg, True, LIGHT_BLUE)
    return text


def draw_fuel(bg_landing_surf_arg, rocket_arg, rocket_fuel_max_arg):
    """Функция рисует текущее состояние топлива.
    :param bg_landing_surf_arg - поверхность, на которой рисуется состояние
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

    if rocket.fuel > 0:
        fuel_quantity = round(rocket.fuel, 1)
    else:
        fuel_quantity = 0

    fuel_text = change_font_color(rocket, 'fuel', fuel_quantity, 'kg')

    bg_landing_surf_arg.blit(fuel_max_image, (fuel_bar_pos_x, fuel_bar_pos_y))
    bg_landing_surf_arg.blit(fuel_image, (fuel_bar_pos_x, fuel_bar_pos_y + 100 + (100 - fuel_per_height)))
    bg_landing_surf_arg.blit(fuel_text, (fuel_bar_pos_x - 25, fuel_bar_pos_y + 200))


def draw_height(bg_landing_surf_arg, rocket_arg, moon_arg, space_arg):
    """Функция рисует текущую высоту ракеты.
    :param bg_landing_surf_arg - поверхность, на которой рисуется состояние
    :param rocket_arg - ракета, элемент класса Rocket
    :param moon_arg - картинка земли
    :param space_arg - картинка космоса"""
    cosmos_bar_height = 300
    cosmos_bar_width = 5
    cosmos_bar_pos_x = 750
    cosmos_bar_pos_y = 160
    cosmos_height_per = 100 * (rocket_arg.h - 6400000) / 100000
    cosmos_height_stick = pygame.Surface((cosmos_bar_width, cosmos_bar_height))
    cosmos_height_roll = pygame.Surface((15, 5))
    cosmos_height_stick.fill('white')
    cosmos_height_roll.fill('tomato')
    bg_landing_surf_arg.blit(cosmos_height_stick, (750, 160))

    cosmos_height = abs(round((rocket.h - 6400000) / 1000, 1))
    cosmos_text = change_font_color(rocket_arg, 'height', cosmos_height, 'km')

    if cosmos_height_per < 100:
        bg_landing_surf_arg.blit(cosmos_height_roll, (cosmos_bar_pos_x - 5,
                                cosmos_bar_pos_y + cosmos_bar_height
                                - (cosmos_bar_height / 100 * cosmos_height_per)))
    else:
        bg_landing_surf_arg.blit(cosmos_height_roll, (cosmos_bar_pos_x - 5, cosmos_bar_pos_y))
    """if rocket_arg.h - 6400000 >= 6000:
        if 6000 <= rocket_arg.h - 6400000 <= 20000:
            text_height = FONT_small.render('You are in the troposphere', True, BLUE)
        elif 20000 < rocket_arg.h - 6400000 <= 50000:
            text_height = FONT_small.render('You are in the stratosphere', True, LIGHT_BLUE)
        elif 50000 < rocket_arg.h - 6400000 <= 85000:
            text_height = FONT_small.render('You are in the mesosphere', True, LIGHT_BLUE)
        elif 85000 < rocket_arg.h - 6400000 <= 100000:
            text_height = FONT_small.render('You are up to the Karman line', True, LIGHT_BLUE)
        elif 100000 < rocket_arg.h - 6400000:
            text_height = FONT_small.render('You have crossed Karman line', True, LIGHT_BLUE)

        bg_landing_surf_arg.blit(text_height, (250, 15))"""

    bg_landing_surf_arg.blit(moon_arg, (cosmos_bar_pos_x - 7, cosmos_bar_height + cosmos_bar_pos_y + 10))
    bg_landing_surf_arg.blit(space_arg, (cosmos_bar_pos_x - 7, cosmos_bar_pos_y - 30))
    bg_landing_surf_arg.blit(cosmos_text, (cosmos_bar_pos_x - 140, cosmos_bar_pos_y + cosmos_bar_height + 50))


def draw_speed(bg_landing_surf_arg, rocket_arg):
    """Функция рисует текущую скорость ракеты.
    :param bg_landing_surf_arg - поверхность, на которой рисуется состояние
    :param rocket_arg - ракета, элемент класса Rocket"""
    # FIXME сделать всплывающую плашку "вы достигли первой комической скорости"
    speed_bar_height = 200
    speed_bar_width = 50
    speed_bar_pos_x = 50
    speed_bar_pos_y = 90
    speed = (rocket_arg.vx ** 2 + rocket_arg.vy ** 2) ** 0.5
    v_1 = 79.10  # 6.67 * 10**(-11) * 6 * 10**24 / rocket.h
    speed_per = speed * (100 / v_1)
    speed_per_height = (speed_bar_height / 100 * speed_per)
    speed_image = pygame.Surface((speed_bar_width, speed_per_height))
    speed_image_max = pygame.Surface((speed_bar_width, speed_bar_height))
    speed_image_max.fill(LIGHT_BLUE)
    speed_image.fill('tomato')

    speed_text = change_font_color(rocket_arg, 'speed', round(speed, 1), 'm/c')
    speed_vx_text = change_font_color(rocket_arg, 'v_x', round(rocket.vx, 1), 'm/c')
    speed_vy_text = change_font_color(rocket_arg, 'v_y', round(rocket.vy, 1), 'm/c')

    bg_landing_surf_arg.blit(speed_image_max, (speed_bar_pos_x, speed_bar_pos_y))

    if speed_per < 100:
        bg_landing_surf_arg.blit(speed_image, (speed_bar_pos_x, speed_bar_pos_y + (speed_bar_height - speed_per_height)))
    else:
        speed_image = pygame.Surface((speed_bar_width, speed_bar_height))
        speed_image.fill('tomato')
        bg_landing_surf_arg.blit(speed_image, (speed_bar_pos_x, speed_bar_pos_y))

    bg_landing_surf_arg.blit(speed_text, (speed_bar_pos_x - 25, speed_bar_pos_y - 30))
    bg_landing_surf_arg.blit(speed_vx_text, (speed_bar_pos_x - 25, speed_bar_pos_y - 90))
    bg_landing_surf_arg.blit(speed_vy_text, (speed_bar_pos_x - 25, speed_bar_pos_y - 60))


def draw_angle(bg_landing_surf_arg, rocket_arg):
    """Функция рисует текущий угол ракеты.
    :param bg_landing_surf_arg - поверхность, на которой рисуется состояние
    :param rocket_arg - ракета, элемент класса Rocket"""
    # FIXME поправить периодичность угла
    angle_center_x = 25
    angle_center_y = 50
    angle_center_bg_x = 760
    angle_center_bg_y = 110
    if rocket_arg.h <= 6400000 + 100000:
        angle_ideal = - 180 / (2 * 100000) * (rocket_arg.h - 6400000)
    else:
        angle_ideal = - 90
    angle_difference = angle_ideal - rocket.angle
    pos_angle = angle_center_x, angle_center_y
    center_angle = (angle_center_bg_x, angle_center_bg_y)
    angle1 = pygame.image.load("images/flight/angle.png")
    angle1 = pygame.transform.scale(angle1, (25, 50))
    w_angle, h_angle = angle1.get_size()
    angle2 = pygame.Surface((2 * w_angle, 2 * h_angle), pygame.SRCALPHA)
    angle2.blit(angle1, (w_angle - pos_angle[0], h_angle - pos_angle[1]))
    angle_rotated = pygame.transform.rotate(angle2, angle_ideal)
    rect_angle = angle_rotated.get_rect()
    rect_angle.center = center_angle
    angle_text = change_font_color(rocket, 'deviation', abs(round(angle_difference, 1)), ' ')

    bg_landing_surf_arg.blit(angle_rotated, rect_angle)
    bg_landing_surf_arg.blit(angle_text, (angle_center_bg_x - 150, angle_center_y - 40))


"""def fill_gradient(bg_landing_surf_arg, rocket_arg):

    if rocket_arg.h <= 6400000 + 30000:
        color1 = int(127 - (127 - 30) / 30000 * (rocket_arg.h - 6400000))
        color2 = int(199 - (199 - 33) / 30000 * (rocket_arg.h - 6400000))
        color3 = int(255 - (255 - 61) / 30000 * (rocket_arg.h - 6400000))
        bg_landing_surf_arg.fill((color1, color2, color3))
    else:
        bg_landing_surf_arg.fill((30, 33, 61))"""


def draw_status(bg_landing_surf_arg, rocket_arg, rocket_fuel_max_arg, moon_arg, space_arg):
    draw_fuel(bg_landing_surf_arg, rocket_arg, rocket_fuel_max_arg)
    draw_height(bg_landing_surf_arg, rocket_arg, moon_arg, space_arg)
    draw_speed(bg_landing_surf_arg, rocket_arg)
    draw_angle(bg_landing_surf_arg, rocket_arg)


def check_space_landing(bg_landing_surf_arg, rocket_arg):
    v_1 = 79  # 6.67 * 10**(-11) * 6 * 10**24 / rocket.h
    if abs(round(rocket_arg.angle) + 90) % 360 <= 20 and (rocket_arg.vx**2+rocket_arg.vy**2)**0.5 >= v_1\
            and rocket_arg.h - 6400000 >= 100000:
        pass_level1 = FONT_small.render('You have entered the space.',  True, LIGHT_BLUE)
        pass_level2 = FONT_small.render('Congratulations!', True, LIGHT_BLUE)
        pass_level3 = FONT_small.render('"Enter" to reach the Moon.', True, LIGHT_BLUE)
        bg_landing_surf_arg.blit(pass_level1, (240, 40))
        bg_landing_surf_arg.blit(pass_level2, (300, 80))
        bg_landing_surf_arg.blit(pass_level3, (250, 120))


def check_falling(bg_landing_surf_arg, rocket_arg):
    text_fall = FONT_small.render(' ', True, BLUE)
    if (rocket_arg.vx**2 + rocket_arg.vy**2)**0.5 >= 30 and rocket_arg.h <= 100:
        text_fall = FONT_small.render('You have fallen.', True, BLUE)
    bg_landing_surf_arg.blit(text_fall, (250, 120))


def draw_landing_foo(rocket, events, flag_forward, flag_left, flag_right, rocket_fuel_max):
    bg_landing_surf, moon, space = render_bg()
    fire_big, fire_small = render_fire()
    time_step = 0
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
    rocket_move(rocket, flag_left, flag_right, flag_forward)
    #fill_gradient(bg_landing_surf, rocket)
    draw_fuel(bg_landing_surf, rocket, rocket_fuel_max)
    draw_height(bg_landing_surf, rocket, moon, space)
    draw_speed(bg_landing_surf, rocket)
    draw_angle(bg_landing_surf, rocket)
    draw_bg(bg_landing_surf, time_step, rocket)
    draw_rocket(bg_landing_surf, rocket, rect)
    sc.blit(bg_landing_surf, (0, 0))
    pygame.display.update()
    clock.tick(FPS)
    time_step += 1
    return rocket, flag_forward, flag_left, flag_right, rocket_fuel_max


if __name__ == '__main__':

    flag_left = False
    flag_right = False
    flag_forward = False

    fuel_calc(rocket)
    rocket_fuel_max = rocket.fuel

    fire_big, fire_small = render_fire()
    moon, space = render_img()
    moon_cords, moon_plate = render_moon_plate()

    fire_big_step = 0
    fire_small_step = 0
    time_step = 0
    rocket.h = 6400000 + 100000
    rocket.angle = -90
    v_1_moon = (6.67 * 10**(-11)* 7.35 * 10**22 / (100000 + 1737100))**0.5
    rocket.vx = v_1_moon
    while True:
        bg_landing_surf = render_bg()
        rocket.surface = render_rocket_surface(rocket_surface_width, rocket_surface_height, x_left, y_top, rocket)

        rocket_rotated, rect = draw_rotate(rocket, fire_big, fire_small, flag_forward, flag_left, flag_right,
                                           engines_cord, engines_left_cord, engines_right_cord, fire_big_step,
                                           fire_small_step, time_step, rocket_surface_width, rocket_surface_height)

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

        rocket_move(rocket, flag_left, flag_right, flag_forward)

        #fill_gradient(bg_landing_surf, rocket)

        draw_bg(moon_plate, bg_landing_surf, rocket)

        draw_status(bg_landing_surf, rocket, rocket_fuel_max, moon, space)

        draw_rocket(bg_landing_surf, rocket_rotated, rect)


        check_space_landing(bg_landing_surf, rocket)

        check_falling(bg_landing_surf, rocket)

        sc.blit(bg_landing_surf, (0, 0))

        pygame.display.update()

        clock.tick(FPS)
        time_step += 1
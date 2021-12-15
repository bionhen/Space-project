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
i = 1

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
    sc.blit(bg_flight_surf, (0, 0))


def render_fire():
    fire_big = [pygame.image.load('images/flight/fire/fire1.png'), pygame.image.load('images/flight/fire/fire2.png'),
                pygame.image.load('images/flight/fire/fire3.png'), pygame.image.load('images/flight/fire/fire4.png'),
                pygame.image.load('images/flight/fire/fire5.png')]
    return fire_big


def draw_fire(rocket, fire_big, flag_forward):
    global i
    global time_step
    if flag_forward:
        if time_step % 2 == 0:
            i += 1
        if i % 5 == 0:
            i = 0
        for k in range(len(engines_cord)):
            rocket.surface.blit(fire_big[i], (engines_cord[k][0], engines_cord[k][1] + engines_cord[k][2]))


def draw_rocket(rocket, bg_flight_surf):
    """Эта функция поворачивает картинку на заданный угол относительно заданного центра вращения
    :param img: изображение, с которым произойдет преображение :)
    :param pos: координаты центра вращения на изображении
    :param center: координаты центра поверхности на экране
    :param angle: тот самый заданный угол поворота
    :return: повернутое изображение и координаты точки, где его надо нарисовать"""
    #rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
    x_center_mass, y_center_mass = find_center_mass(rocket)
    angle = rocket.angle
    pos = x_center_mass, y_center_mass
    center = (400, 520 - rocket_surface_height + 50 + y_center_mass)
    w, h = rocket_surface_widht, rocket_surface_height
    img2 = pygame.Surface((2*w, 2*h), pygame.SRCALPHA)
    img2.blit(rocket.surface, (w - pos[0], h - pos[1]))
    img4 = pygame.transform.rotate(img2, angle)
    rect = img4.get_rect()
    rect.center = center

    bg_flight_surf.blit(img4, rect)
    #sc.blit(img4, rect)


def draw_fuel(bg_flight_surf, rocket, rocket_fuel_max):
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
    if rocket.h < 30000 + 6400000 and rocket.fuel > 0:
        fuel_text = FONT_small.render('fuel: ' + str(round(rocket.fuel, 1)), True, BLUE)
    if rocket.h >= 30000 + 6400000 and rocket.fuel < 0:
        fuel_text = FONT_small.render('fuel: ' + str(round(rocket.fuel, 1)), True, LIGHT_BLUE)
    if rocket.h < 30000 + 6400000 and rocket.fuel <= 0:
        fuel_text = FONT_small.render('fuel: ' + str(0), True, BLUE)
    if rocket.h >= 30000 + 6400000 and rocket.fuel <= 0:
        fuel_text = FONT_small.render('fuel: ' + str(0), True, LIGHT_BLUE)
    bg_flight_surf.blit(fuel_max_image, (50, 300))
    bg_flight_surf.blit(fuel_status_image, (50, 400+(100 - fuel_per_height)))
    bg_flight_surf.blit(fuel_text, (50 - 25, 510))


def draw_height(bg_flight_surf, rocket, earth, space):
    # FIXME сделать всплывающую плашку "вы достигли космоса"
    cosmos_height_per = 100 * (rocket.h - 6400000) / 80000
    cosmos_height_stick = pygame.Surface((5, 300))
    cosmos_height_roll = pygame.Surface((15, 5))
    cosmos_height_stick.fill('white')
    cosmos_height_roll.fill(BLUE)
    bg_flight_surf.blit(cosmos_height_stick, (750, 200))
    if cosmos_height_per < 100:
        bg_flight_surf.blit(cosmos_height_roll, (750 - 5, 200 + 300 - (300 / 100 * cosmos_height_per)))
    else:
            bg_flight_surf.blit(cosmos_height_roll, (750 - 5, 200))
    bg_flight_surf.blit(earth, (743, 510))
    bg_flight_surf.blit(space, (743, 170))


def draw_speed(bg_flight_surf, rocket):
    # FIXME сделать всплывающую плашку "вы достигли первой комической скорости"
    speed = (rocket.vx**2 + rocket.vy**2)**0.5
    speed_per = speed*(100 / 7910)
    speed_per_height = (200 / 100 * speed_per)
    speed_image = pygame.Surface((50, speed_per_height))
    speed_image_max = pygame.Surface((50, 200))
    speed_image_max.fill(LIGHT_BLUE)
    speed_image.fill('tomato')
    speed_text = FONT_small.render('speed: ' + str(round(speed, 1)), True, BLUE)
    bg_flight_surf.blit(speed_image_max, (50, 50))
    if speed_per < 100:
        bg_flight_surf.blit(speed_image, (50, 50+(200 - speed_per_height)))
    else:
        speed_image = pygame.Surface((50, 200))
        speed_image.fill('tomato')
        bg_flight_surf.blit(speed_image, (50, 50))

    bg_flight_surf.blit(speed_text, (25, 270))

def draw_angle(bg_flight_surf, rocket):
    #FIXME поправить периодичность угла
    angle_ideal = 3.14 / (2 * 80000) * (rocket.h - 6400000)
    angle_difference = angle_ideal - rocket.angle
    pos_angle = 25, 50
    center_angle = (760, 100)
    angle1 = pygame.image.load("images/flight/angle.png")
    angle1 = pygame.transform.scale(angle1, (25, 50))
    w_angle, h_angle = angle1.get_size()
    angle2 = pygame.Surface((2*w_angle, 2*h_angle), pygame.SRCALPHA)
    angle2.blit(angle1, (w_angle - pos_angle[0], h_angle - pos_angle[1]))
    angle4 = pygame.transform.rotate(angle2, angle_ideal)
    rect_angle = angle4.get_rect()
    rect_angle.center = center_angle

    angle_text = FONT_small.render('deviation: ' + str(abs(round(angle_difference, 1))), True, BLUE)

    bg_flight_surf.blit(angle4, rect_angle)
    bg_flight_surf.blit(angle_text, (620, 120))



def fill_gradient(bg_flight_surf, h):
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
    fire_big = render_fire()
    rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
    while True:
        #rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
        print(rocket.surface)
        print(rocket.list)
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


        draw_fire(rocket, fire_big, flag_forward)

        draw_rocket(rocket, bg_flight_surf)
        #sc.blit(rocket.surface, (0,0))
        sc.blit(bg_flight_surf, (0, 0))

        pygame.display.update()

        clock.tick(FPS)
        time_step += 1
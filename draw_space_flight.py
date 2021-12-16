import pygame
from space_flight import *
from space_obj import *
from starship_rocket import *

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
    bg_space_flight_surf = pygame.image.load(("images/space_flight/bg_space_flight.png")).convert_alpha()

    print(Rocket_Obj.x / 1000000, Rocket_Obj.y / 1000000)
    return bg_space_flight_surf #, cosmodrom, ground, earth, space

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
        bg_space_flight_surf.blit(object.image, (object.x/1000000, object.y/1000000))


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

if __name__ == '__main__':
    Earth = Object()
    Earth.type = "planet"
    Earth.m = 6 * 10**24
    Earth.x = 100 * 10**6
    Earth.y = 200 * 10**6
    Earth.Vx = 0
    Earth.Vy = 0
    Earth.Fx = 0
    Earth.Fy = 0
    Earth.R = 0
    Earth.image = pygame.image.load("images/space_flight/earth_above.png")
    Earth.image = pygame.transform.scale(Earth.image, (100, 100))
    Earth.angle = 0
    Earth.omega = 0

    Moon = Object()
    Moon.type = "planet"
    Moon.m = 7.35 * 10**22
    Moon.x = 362 * 10**6 + 100 * 10**6
    Moon.y = 200 * 10**6
    Moon.Vx = 0
    Moon.Vy = -1020
    Moon.Fx = 0
    Moon.Fy = 0
    Moon.R = 0
    Moon.image = pygame.image.load("images/space_flight/moon_1.png")
    Moon.image = pygame.transform.scale(Moon.image, (30, 30))
    Moon.angle = 0
    Moon.omega = 0

    Rocket_Obj = Object()
    Rocket_Obj.type = "rocket"
    Rocket_Obj.m = 1
    Rocket_Obj.x = 110 * 10**6
    Rocket_Obj.y = 200 * 10**6
    Rocket_Obj.Vx = 0
    Rocket_Obj.Vy = 0
    Rocket_Obj.Fx = 0
    Rocket_Obj.Fy = 0
    Rocket_Obj.R = 0
    Rocket_Obj.image = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.polygon(Rocket_Obj.image, 'tomato', ((0, 100), (50, 0), (100, 100)))
    Rocket_Obj.list = rocket.list
    Rocket_Obj.angle = 90
    Rocket_Obj.omega = 0

    space_objects = [Earth, Moon, Rocket_Obj]


    #earth_images = render_earth()
    #moon_images = render_moon()

    while True:
        bg_space_flight_surf = render_bg()
        print(rocket.surface)
        draw_objects(space_objects, bg_space_flight_surf)
        recalculate_space_objects_positions(space_objects, 10000, False, False, False)
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

        #draw_earth(bg_space_flight_surf, earth_images)
        #draw_moon(bg_space_flight_surf, moon_images)
        sc.blit(bg_space_flight_surf, (0, 0))
        pygame.display.update()

        clock.tick(FPS)
        time_step_space += 1
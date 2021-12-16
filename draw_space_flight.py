import pygame

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
    #earth_3 = pygame.image.load(("images/space_flight/earth_3.png")).convert_alpha()
    #bg_space_flight_surf.blit(earth_3, (200, 250))

    """cosmodrom = pygame.image.load(("images/flight/cosmodrom.png")).convert_alpha()
    cosmodrom = pygame.transform.scale(cosmodrom, (300, 375))
    ground = pygame.image.load(("images/flight/ground.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (800, 80))
    earth = pygame.image.load(("images/flight/earth.png")).convert_alpha()
    earth = pygame.transform.scale(earth, (20, 20))
    space = pygame.image.load(("images/flight/space.png")).convert_alpha()
    space = pygame.transform.scale(space, (20, 20))"""

    return bg_space_flight_surf #, cosmodrom, ground, earth, space

def render_earth():
    """Функция генерирует массивыы изображений огней.
    :returns
    fire_big - огни для центральных двигателей
    fire_small - огни для боковых двигателей"""
    earth_images = []
    for n in range(1, 13):
        earth = pygame.image.load('images/space_flight/earth_'+str(n)+'.png')
        earth = pygame.transform.scale(earth, (100, 100))
        earth_images.append(earth)

    return earth_images

def render_moon():
    """Функция генерирует массивыы изображений огней.
    :returns
    fire_big - огни для центральных двигателей
    fire_small - огни для боковых двигателей"""
    moon_images = []
    for n in range(1, 20):
        moon = pygame.image.load('images/space_flight/moon_'+str(n)+'.png')
        moon = pygame.transform.scale(moon, (30, 30))
        moon_images.append(moon)

    return moon_images


def draw_earth(bg_space_flight_surf, earth_images):
    global e
    global time_step_space
    if time_step_space % 3 == 0:
        e += 1
    if e % 12 == 0:
        e = 0

    bg_space_flight_surf.blit(earth_images[e], (200, 250))

def draw_moon(bg_space_flight_surf, moon_images):
    global m
    global time_step_space
    if time_step_space % 3 == 0:
        m += 1
    if m % 19 == 0:
        m = 0

    bg_space_flight_surf.blit(moon_images[m], (500, 250))

if __name__ == '__main__':
    bg_space_flight_surf = render_bg()
    earth_images = render_earth()
    moon_images = render_moon()
    while True:

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

        draw_earth(bg_space_flight_surf, earth_images)
        draw_moon(bg_space_flight_surf, moon_images)
        sc.blit(bg_space_flight_surf, (0, 0))
        pygame.display.update()

        clock.tick(FPS)
        time_step_space += 1
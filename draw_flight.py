import pygame
from starship_rocket import *
from starship_flight import *
from starship_modules import *

pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 30

FONT = pygame.font.SysFont('century gothic', 24)
pygame.font.init()


def render_bg():
    """Функция генерирует составляющие фона."""
    bg_flight_surf = pygame.Surface((800, 600))
    cosmodrom = pygame.image.load(("images/flight/cosmodrom.png")).convert_alpha()
    cosmodrom = pygame.transform.scale(cosmodrom, (300, 375))
    ground = pygame.image.load(("images/flight/ground.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (800, 75))

    return bg_flight_surf, cosmodrom, ground

def draw_bg(bg_flight_surf, cosmodrom, ground, rocket):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_flight_surf.blit(cosmodrom, (250, 200))
    bg_flight_surf.blit(ground, (0, 525))
    rocket.surface = pygame.transform.scale(rocket.surface, (100, 200))
    bg_flight_surf.blit(rocket.surface, (400 - x_left, 315))
    sc.blit(bg_flight_surf, (0, 0))


def draw_status(bg_flight_surf, fuel):
    fuel_status_image = pygame.Surface((50, fuel + 10))
    if 50 < fuel:  #FIXME топливо не фиксированное, а в процентах от максимума.
        fuel_status_image.fill('green')
    elif 25 < fuel <= 50:
        fuel_status_image.fill('yellow')
    elif fuel <= 25:
        print('hee')
        fuel_status_image.fill('tomato')

    #fuel_text = FONT_small.render('fuel: ' + str(fuel), True, BLUE)

    bg_flight_surf.blit(fuel_status_image, (50, 50))

def fill_gradient(bg_flight_surf, h):
    if h<= 6400000 + 30000:
        color1 = int(127 - (127-30)/30000 * (h-6400000))
        color2 = int(199 - (199-33)/30000 * (h-6400000))
        color3 = int(255 - (255-61)/30000 * (h-6400000))
        bg_flight_surf.fill((color1, color2, color3))
    else:
        bg_flight_surf.fill((30, 33, 61))


module0 = Module()
module0.type = 'engine'
module0.m = 100
module0.fuel = 100
module0.price = 0
module0.resistance = 100
module0.force = 100
module0.image = 'engine_2x1'
module0.a = 50
module0.b = 100
module0.x = 0
module0.y = 0
module0.surface = pygame.image.load("images/constructor/modules/engine_2x1.png")
module0.surface = pygame.transform.scale(module0.surface, (module0.b, module0.a))

rocket.list = [module0]
h = 6400000
if __name__ == '__main__':
    fuel_calc(rocket)
    bg_flight_surf, cosmodrom, ground = render_bg()
    while True:
        #h = rocket.h

        fill_gradient(bg_flight_surf, h)
        draw_status(bg_flight_surf, 100)
        draw_bg(bg_flight_surf, cosmodrom, ground, rocket)

        h += 1000


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        flag_left = flag_right = flag = True
        if rocket_list != []:
            rocket_move(rocket, flag_left, flag_right, flag)


        pygame.display.update()

        clock.tick(FPS)
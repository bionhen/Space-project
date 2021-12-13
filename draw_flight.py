import pygame
from starship_rocket import *
from starship_flight import *

pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 30

FONT = pygame.font.SysFont('century gothic', 24)
pygame.font.init()

time_step = 0
i = 1

def render_bg():
    """Функция генерирует составляющие фона."""
    bg_flight_surf = pygame.Surface((800, 600))
    cosmodrom = pygame.image.load(("images/flight/cosmodrom.png")).convert_alpha()
    cosmodrom = pygame.transform.scale(cosmodrom, (300, 375))
    ground = pygame.image.load(("images/flight/ground.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (800, 75))

    return bg_flight_surf, cosmodrom, ground

def draw_bg(bg_flight_surf, cosmodrom, ground):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_flight_surf.blit(cosmodrom, (250, 200 + h - 6400000))
    bg_flight_surf.blit(ground, (0, 525+ h - 6400000))
    sc.blit(bg_flight_surf, (0, 0))

def draw_rocket(bg_flight_surf, rocket):
    bg_flight_surf.blit(rocket.surface, (400 - rocket_surface_widht/2, 520 - rocket_surface_height))
    sc.blit(bg_flight_surf, (0, 0))
    #rocket.surface = pygame.transform.scale(rocket.surface, (100, 200))



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

def draw_status(bg_flight_surf, rocket):
    fuel_per = rocket.fuel/(rocket_fuel_max/100)
    fuel_status_image = pygame.Surface((50, fuel_per - 100))
    if 75 < fuel_per:
        fuel_status_image.fill('green')
    if 50 < fuel_per <= 75:  #FIXME топливо не фиксированное, а в процентах от максимума.
        fuel_status_image.fill('yellow')
    elif 25 < rocket.fuel <= 50:
        fuel_status_image.fill('orange')
    elif rocket.fuel <= 25:
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


h = 6400000
flag_left = flag_right = False
flag_forward = False
if __name__ == '__main__':
    fuel_calc(rocket)
    bg_flight_surf, cosmodrom, ground = render_bg()

    while True:
        #rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    flag_forward = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    flag_forward = False


        h = rocket.h

        rocket_move(rocket, flag_left, flag_right, flag_forward)
        fill_gradient(bg_flight_surf, h)
        draw_status(bg_flight_surf, rocket)
        draw_bg(bg_flight_surf, cosmodrom, ground)
        fire_big = render_fire()
        draw_fire(rocket, fire_big, flag_forward)

        draw_rocket(bg_flight_surf, rocket)

        #sc.blit(rocket.surface, (100, 100)) #(400 - x_left, 315))





        pygame.display.update()

        clock.tick(FPS)
        time_step += 1
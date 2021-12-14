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
    """Функция генерирует составляющие фона."""
    bg_flight_surf = pygame.Surface((800, 600))
    cosmodrom = pygame.image.load(("images/flight/cosmodrom.png")).convert_alpha()
    cosmodrom = pygame.transform.scale(cosmodrom, (300, 375))
    ground = pygame.image.load(("images/flight/ground.png")).convert_alpha()
    ground = pygame.transform.scale(ground, (800, 80))
    #ground = pygame.transform.scale(ground, (800, 75))

    return bg_flight_surf, cosmodrom, ground

def draw_bg(bg_flight_surf, cosmodrom, ground):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_flight_surf.blit(cosmodrom, (250, 200 + (h - 6400000) * 15))
    bg_flight_surf.blit(ground, (0, 525+ (h - 6400000) * 15))
    sc.blit(bg_flight_surf, (0, 0))

#def draw_rocket(bg_flight_surf, rocket, fire_big, flag_forward):
    #draw_fire(rocket, fire_big, flag_forward)
    #bg_flight_surf.blit(rocket.surf, (400 - rocket_surface_widht/2, 520 - rocket_surface_height))
    #sc.blit(bg_flight_surf, (0, 0))
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
            rocket.surf.blit(fire_big[i], (engines_cord[k][0], engines_cord[k][1] + engines_cord[k][2]))
            #print("cvth")
"""
Огромный комментарий к функции draw_rotate
Во-первых, сначала нужно определить следующие переменные (не обязательно как в примере):"""
angle = 20
center = (400 - rocket_surface_widht/2, 520 - rocket_surface_height)
pos = [25, 50]
flag_left = flag_right = False
"""И да, rotate_left и rotate_right надо бы в flag_left и flag_right переименовать
Во-вторых, вот сама функция:"""
def draw_rotate(rocket, pos, center, angle):
    """Эта функция поворачивает картинку на заданный угол относительно заданного центра вращения
    :param img: изображение, с которым произойдет преображение :)
    :param pos: координаты центра вращения на изображении
    :param center: координаты центра поверхности на экране
    :param angle: тот самый заданный угол поворота
    :return: повернутое изображение и координаты точки, где его надо нарисовать"""
    #print(rocket.surf)

    w, h = rocket_surface_widht, rocket_surface_height
    img2 = pygame.Surface((2*w, 2*h), pygame.SRCALPHA)
    img2.blit(rocket.surf, (w - pos[0], h - pos[1]))
    img4 = pygame.transform.rotate(img2, angle)
    rect = img4.get_rect()
    rect.center = center
    return img4, rect
"""В-третьих, нужно написать еще вот эти строчки:"""

"""Потому что sc.blit(draw_rotate (img, (25, 25), (300, 100), angle)) по какой-то причине не работает"""

def draw_status(bg_flight_surf, rocket):
    fuel_per = rocket.fuel*(100/rocket_fuel_max)
    fuel_status_image = pygame.Surface((50, fuel_per))
    if 75 < fuel_per:
        fuel_status_image.fill('green')
    if 50 < fuel_per <= 75:  #FIXME топливо не фиксированное, а в процентах от максимума.
        fuel_status_image.fill('yellow')
    elif 25 < rocket.fuel <= 50:
        fuel_status_image.fill('orange')
    elif rocket.fuel <= 25:
        fuel_status_image.fill('tomato')
    if rocket.h < 3000 + 6400000:
        fuel_text = FONT_small.render('fuel: ' + str(round(rocket.fuel, 1)), True, BLUE)
    if rocket.h >= 3000 + 6400000:
        fuel_text = FONT_small.render('fuel: ' + str(round(rocket.fuel, 1)), True, LIGHT_BLUE)
    bg_flight_surf.blit(fuel_text, (50 - 25, 450))
    bg_flight_surf.blit(fuel_status_image, (50, 350+(100 - fuel_per)))


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
    rocket_fuel_max = rocket.fuel
    fire_big = render_fire()
    #rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
    while True:
        center = (400, 520 - rocket_surface_height/2)
        pos = [25, 50]
        #img4, rect = draw_rotate(rocket, pos, center, angle)
        #rocket.surface = render_rocket_surface(rocket_surface_widht, rocket_surface_height, rocket)
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
        img4, rect = draw_rotate(rocket, pos, center, angle)
        h = rocket.h
        angle = rocket.angle
        print(flag_forward)
        rocket_move(rocket, flag_left, flag_right, flag_forward)
        fill_gradient(bg_flight_surf, h)
        draw_status(bg_flight_surf, rocket)
        draw_bg(bg_flight_surf, cosmodrom, ground)

        bg_flight_surf.blit(img4, rect)
        draw_fire(rocket, fire_big, flag_forward)

        #draw_rocket(bg_flight_surf, rocket, fire_big, flag_forward)
        sc.blit(bg_flight_surf, (0, 0))


        #sc.blit(rocket.surface, (100, 100)) #(400 - x_left, 315))





        pygame.display.update()

        clock.tick(FPS)
        time_step += 1

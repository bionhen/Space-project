import pygame
from draw_constructor import *
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

def draw_bg(bg_flight_surf, cosmodrom, ground, rocket_surface, h):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_flight_surf.blit(cosmodrom, (250, 200+h))
    bg_flight_surf.blit(ground, (0, 525+h))
    rocket_surface = pygame.transform.scale(rocket_surface, (200, 250))
    bg_flight_surf.blit(rocket_surface, (300, 250))
    sc.blit(bg_flight_surf, (0, 0))



def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse

    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom
    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
            )
            fn_line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
            )
            fn_line(surface, color, (col, y1), (col, y2))
h = 1
if __name__ == '__main__':
    while True:
        bg_flight_surf, cosmodrom, ground = render_bg()
        fill_gradient(bg_flight_surf, (30 - 0.5 * h, 33 - 0.5 * h, 61 - 0.05 * h), (127 - h, 199 - h, 255 - 0.5 * h),
                      rect=None, vertical=True, forward=True)
        draw_bg(bg_flight_surf, cosmodrom, ground, rocket_surface, h)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


        h += 10
        pygame.display.update()

        clock.tick(FPS)
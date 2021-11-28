import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont('century gothic', 24)
pygame.font.init()

cash = 1000


class Button:
    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.button_surf = pygame.image.load(("images/missions/"+filename+".png")).convert_alpha()


class ButtonOff(Button):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.button_off_surf_width = pygame.Surface.get_width(self.button_surf)
        self.button_off_surf_height = pygame.Surface.get_height(self.button_surf)

    def check_button(self, cur_event):
        if ((cur_event[0] >= self.x)
                and (cur_event[0] <= self.x + self.button_off_surf_width)
                and (cur_event[1] >= self.y)
                and (cur_event[1] <= self.y + self.button_off_surf_height)):
            button_checked = True
        else:
            button_checked = False
        return button_checked


def render_bg():
    grid = pygame.image.load(("images/constructor/grid.png")).convert_alpha()
    bg_constructor_surf = pygame.image.load(("images/constructor/bg_constructor.png")).convert_alpha()
    panel = pygame.image.load(("images/constructor/panel.png")).convert_alpha()

    return grid, bg_constructor_surf, panel


def draw_bg(grid, bg_constructor_surf, panel):
    sc.blit(bg_constructor_surf, (0, 0))
    bg_constructor_surf.blit(grid, (200, 50))
    bg_constructor_surf.blit(panel, (0, 0))
    bg_constructor_surf.blit(panel, (650, 0))


def render_buttons():
    orbit = Button('entering orbit on', 100, 150)
    orbit_off = ButtonOff('entering orbit', 100, 150)
    moon = Button('flight to the moon on', 100, 250)
    moon_off = ButtonOff('flight to the moon', 100, 250)

    buttons_off = [orbit_off, moon_off]
    buttons_on = [orbit, moon]

    return buttons_off, buttons_on


def draw_buttons(bg_surf, buttons_off, buttons_on):
    for i in range(len(buttons_off)):
        bg_surf.blit(buttons_off[i].button_surf, (buttons_off[i].x, buttons_on[i].y))
        if buttons_off[i].check_button(pygame.mouse.get_pos()):
            bg_surf.blit(buttons_on[i].button_surf, (buttons_on[i].x, buttons_on[i].y))


def draw_points():
    """Метод отрисовывает количество поражённых целей на экране."""
    text = FONT.render('Score: ' + str(cash), True, (0, 0, 0))
    sc.blit(text, (660, 20))


grid, bg_constructor_surf, panel = render_bg()
buttons_off, buttons_on = render_buttons()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    draw_bg(grid, bg_constructor_surf, panel)
    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)
    draw_points()


    pygame.display.update()

    clock.tick(FPS)
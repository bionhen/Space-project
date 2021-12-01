import pygame
from starship_modules import *
from starship_constructor import *

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
        self.button_surf = pygame.image.load(("images/constructor/"+filename+".png")).convert_alpha()


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
    bg_constructor_surf.blit(grid, (200, 50))
    sc.blit(bg_constructor_surf, (0, 0))
    #bg_constructor_surf.blit(panel, (0, 0))
    #bg_constructor_surf.blit(panel, (650, 0))


def render_buttons():
    fuel_on = Button('fuel_on', 625, 75)
    fuel_off = ButtonOff('fuel_off', 625, 75)
    autopilot_on = Button('autopilot_on', 625, 150)
    autopilot_off = ButtonOff('autopilot_off', 625, 150)
    engines_on = Button('engines_on', 625, 225)
    engines_off = ButtonOff('engines_off', 625, 225)
    fairings_on = Button('fairings_on', 625, 300)
    fairings_off = ButtonOff('fairings_off', 625, 300)
    modules_on = Button('modules_on', 625, 375)
    modules_off = ButtonOff('modules_off', 625, 375)

    buttons_off = [fuel_off, autopilot_off,engines_off, fairings_off, modules_off]
    buttons_on = [fuel_on, autopilot_on, engines_on, fairings_on, modules_on]

    return buttons_off, buttons_on


"""engine1x1 = pygame.image.load("images/constructor/modules/engine 1x1.png")
module1x1 = pygame.image.load("images/constructor/modules/module 1x1.png")
engine1x1 = pygame.transform.scale(engine1x1, (50, 50))
module1x1 = pygame.transform.scale(module1x1, (50, 50))"""


def draw_buttons(bg_surf, buttons_off, buttons_on):
    for i in range(len(buttons_off)):
        bg_surf.blit(buttons_off[i].button_surf, (buttons_off[i].x, buttons_on[i].y))
        if buttons_off[i].check_button(pygame.mouse.get_pos()):
            bg_surf.blit(buttons_on[i].button_surf, (buttons_on[i].x, buttons_on[i].y))


def draw_points():
    text = FONT.render('Cash: ' + str(cash), True, (0, 0, 0))
    sc.blit(text, (630, 20))


def draw_rocket_surface():
    surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    sc.blit(surface, (200, 50))


blocks, engines, reww = read_modules_data_from_file('module_example')


def render_module_surf_list(dif_modules):
    dif_module_surf_list = []
    x = 75
    y = 100
    for dif_module in dif_modules:
        dif_module_surf = pygame.image.load(("images/constructor/modules/"+dif_module.image+".png"))
        dif_module_surf_width = pygame.Surface.get_width(dif_module_surf)
        dif_module_surf_height = pygame.Surface.get_height(dif_module_surf)
        dif_module_surf = pygame.transform.scale(dif_module_surf, (int(dif_module_surf_width/8), int(dif_module_surf_height/8)))
        dif_module_surf_width = pygame.Surface.get_width(dif_module_surf)
        dif_module_surf_height = pygame.Surface.get_height(dif_module_surf)
        dif_module_surf_list.append([dif_module_surf, dif_module_surf_width, dif_module_surf_height, x, y])
        y += 100

    return dif_module_surf_list


def draw_modules(dif_module_surf_list, bg_constructor_surf):
    dif_modules_surface = pygame.Surface((150, 600), pygame.SRCALPHA)
    for dif_module_surf in dif_module_surf_list:
        dif_modules_surface.blit(dif_module_surf[0], (dif_module_surf[3], dif_module_surf[4]))

    bg_constructor_surf.blit(dif_modules_surface, (0, 0))


def move_modules(dif_module_surf_list, bg_constructor_surf):
    x, y = pygame.mouse.get_pos()
    k = check_module(dif_module_surf_list)
    print(k)
    if k >= 0:
        bg_constructor_surf.blit(dif_module_surf_list[k][0], (x-0.5*dif_module_surf_list[k][1], y-0.5*dif_module_surf_list[k][2]))


def draw_constructor():
    grid, bg_constructor_surf, panel = render_bg()
    buttons_off, buttons_on = render_buttons()
    dif_module_surf_list = render_module_surf_list(blocks)

    move_modules(dif_module_surf_list, bg_constructor_surf)

    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)

    draw_modules(dif_module_surf_list, bg_constructor_surf)

    draw_bg(grid, bg_constructor_surf, panel)

    draw_points()

    draw_rocket_surface()




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            print("sagfsg")
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = True
        elif event.type == pygame.MOUSEBUTTONUP:
            flag1 = False

        draw_constructor()

    pygame.display.update()

    clock.tick(FPS)

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
    """Класс Button (Кнопка, на которую наведен курсор)"""
    def __init__(self, filename, x, y):
        """Инициализация класса Button
        :param filename - имя файла с изображением кнопки
        :param x - координата левого верхнего угла по горизонтали
        :param y - координата левого верхнего угла по вертикали"""
        self.x = x
        self.y = y
        self.button_surf = pygame.image.load(("images/constructor/"+filename+".png")).convert_alpha()


class ButtonOff(Button):
    """Инициализация класса ButtonOff, дочерний класс  (Кнопка, на которую не наведён курсор)
    :param filename - имя файла с изображением кнопки
    :param x - координата левого верхнего угла по горизонтали
    :param y - координата левого верхнего угла по вертикали"""
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.button_off_surf_width = pygame.Surface.get_width(self.button_surf)
        self.button_off_surf_height = pygame.Surface.get_height(self.button_surf)

    def check_button(self, cur_event):
        """Метод проверяет, наведён ли курсор на кнопку."""
        if ((cur_event[0] >= self.x)
                and (cur_event[0] <= self.x + self.button_off_surf_width)
                and (cur_event[1] >= self.y)
                and (cur_event[1] <= self.y + self.button_off_surf_height)):
            button_checked = True
        else:
            button_checked = False
        return button_checked


def render_bg():
    """Функция генерирует составляющие фона."""
    grid = pygame.image.load(("images/constructor/grid.png")).convert_alpha()  # сетка конструктора
    bg_constructor_surf = pygame.image.load(("images/constructor/bg_constructor.png")).convert_alpha()  # задний фон

    return grid, bg_constructor_surf


def draw_bg(grid, bg_constructor_surf, rocket_surface):
    """Функция отрисовывает составляющие заднего фона на экране."""
    bg_constructor_surf.blit(grid, (200, 50))
    bg_constructor_surf.blit(rocket_surface, (200, 50))
    sc.blit(bg_constructor_surf, (0, 0))


def render_buttons():
    """Функция генерирует кнопки."""
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
    done_on = Button('done_on', 625, 500)
    done_off = ButtonOff('done_off', 625, 500)

    buttons_off = [fuel_off, autopilot_off, engines_off, fairings_off, modules_off, done_off]
    buttons_on = [fuel_on, autopilot_on, engines_on, fairings_on, modules_on, done_on]

    return buttons_off, buttons_on


def draw_buttons(bg_surf, buttons_off, buttons_on):
    """Функция отрисовывает кнопки на заднем фоне слайда.
    :param bg_surf - поверность фона
    :param buttons_off - список кнопок, на которые не наведён курсор
    :param buttons_on - список кнопок, на которые наведён курсор"""
    for i in range(len(buttons_off)):
        bg_surf.blit(buttons_off[i].button_surf, (buttons_off[i].x, buttons_on[i].y))
        if buttons_off[i].check_button(pygame.mouse.get_pos()):
            bg_surf.blit(buttons_on[i].button_surf, (buttons_on[i].x, buttons_on[i].y))


def draw_points():
    """Функция отрисовывает количество денег на заднем фоне слайда."""
    text = FONT.render('Cash: ' + str(cash), True, (0, 0, 0))
    sc.blit(text, (630, 20))



def draw_modules(dif_modules, bg_constructor_surf):
    """Функция отрисовывает список модулей на заднем ыоне слайда.
    :param dif_module_surf_list - список поверхностей модулей.
    :param bg_constructor_surf - поверность заднего фона."""
    dif_modules_surface = pygame.Surface((150, 600), pygame.SRCALPHA)
    x = 75
    y = 100

    for dif_module in dif_modules:
        dif_module.x = x
        dif_module.y = y
        dif_module.surface = pygame.image.load(("images/constructor/modules/"+dif_module.image+".png"))
        dif_module.surface = pygame.transform.scale(dif_module.surface, (dif_module.b, dif_module.a))
        dif_modules_surface.blit(dif_module.surface, (dif_module.x, dif_module.y))
        y += 100

    bg_constructor_surf.blit(dif_modules_surface, (0, 0))


def move_modules(dif_modules, bg_constructor_surf, flag, k):
    """Функция отрисовывает движение модулей при взятии их игроком.
    :param dif_module_surf_list - список поверхностей модулей.
    :param bg_constructor_surf - поверность заднего фона.
    :param flag - указатель зажатия кнопки мыши
    :param k - номер элемента массива поверхостей модулей, который берёт пользователь."""
    x, y = pygame.mouse.get_pos()
    if flag:
        bg_constructor_surf.blit(dif_modules[k].surface, (x-0.5*dif_modules[k].b, y-0.5*dif_modules[k].a))


def set_modules(dif_modules, flag, k, rocket_list):
    """Функция добавляет модули в список ракеты.
    :param dif_module_surf_list - список поверхностей модулей
    :param flag - указатель зажатия кнопки мыши
    :param k - номер элемента массива поверхостей модулей, который берёт пользователь.
    :param rocket_list - список элементов ракеты"""
    if flag:
        dif_modules[k].x, dif_modules[k].y = pygame.mouse.get_pos()
        rocket_list.append(dif_modules[k])



def draw_rocket(rocket_list, rocket_surface):
    """Функция рисует модули ракеты на поверности ракеты.
    :param rocket_list - список модулей ракеты
    :param rocket_surface - поверность рактеты."""

    for rocket_module in rocket_list:
        x = rocket_module.x - rocket_module.x % 50 - 200
        y = rocket_module.y - rocket_module.y % 25 - 75
        rocket_surface.blit(rocket_module.surface, (x, y))

def find_y_max(rocket_list):
    """Функция находит наиболее близкий элемент к земле."""
    rocket_modules_y = []
    y_max = 0
    for rocket_module in rocket_list:
        rocket_modules_y.append(rocket_module.y)

    if rocket_modules_y != []:
        y_max = max(rocket_modules_y)

    return y_max

"""def draw_constructor():
    grid, bg_constructor_surf, panel = render_bg()
    buttons_off, buttons_on = render_buttons()
    dif_module_surf_list = render_module_surf_list(blocks)


    move_modules(dif_module_surf_list, bg_constructor_surf)

    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)

    draw_modules(dif_module_surf_list, bg_constructor_surf)

    draw_bg(grid, bg_constructor_surf, panel)

    draw_points()

    draw_rocket()
"""

flag1 = False
flag2 = False
k = -1
j = 0

blocks, engines, tanks, autopilot, fairings = read_modules_data_from_file('module_example')
rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
rocket_list = []

while True:
    grid, bg_constructor_surf = render_bg()
    buttons_off, buttons_on = render_buttons()
    dif_modules = blocks

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = True
            flag2 = False
            if check_module(dif_modules) > -1:
                k = check_module(dif_modules)
        elif event.type == pygame.MOUSEBUTTONUP:
            j = k
            flag1 = False
            flag2 = True
            k = -1
    if flag1 and k >= 0:
        move_modules(dif_modules, bg_constructor_surf, flag1, k)

    if flag2 and j >= 0:
        set_modules(dif_modules, flag2, j, rocket_list)
        j = k

    draw_rocket(rocket_list, rocket_surface)

    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)

    draw_modules(dif_modules, bg_constructor_surf)

    draw_bg(grid, bg_constructor_surf, rocket_surface)

    #print(find_y_max(rocket_list))


    draw_points()


    pygame.display.update()

    clock.tick(FPS)

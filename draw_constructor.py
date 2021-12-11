import pygame
from starship_modules import *
from starship_constructor import *
# from change_screen import *

pygame.init()

pygame.mixer.music.load('images/constructor/Space_Oddity.mp3')
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont('century gothic', 30, bold=True)
FONT_small = pygame.font.SysFont('century gothic', 24, bold=True)
pygame.font.init()

cash = 10000
BLUE = (39, 40, 91)
LIGHT_BLUE = (106, 139, 197)



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
    rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    return grid, bg_constructor_surf, rocket_surface


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
    done_on = Button('done_on', 625, 525)
    done_off = ButtonOff('done_off', 625, 525)
    delete_on = Button('delete_on', 625, 450)
    delete_off = ButtonOff('delete_off', 625, 450)

    buttons_off = [fuel_off, autopilot_off, engines_off, fairings_off, modules_off, done_off, delete_off]
    buttons_on = [fuel_on, autopilot_on, engines_on, fairings_on, modules_on, done_on, delete_on]

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
    text = FONT.render('cash: ' + str(cash), True, BLUE)
    sc.blit(text, (610, 20))


def draw_modules(dif_modules, bg_constructor_surf):
    """Функция отрисовывает список модулей на заднем фоне слайда.
    :param dif_module_surf_list - список поверхностей модулей.
    :param bg_constructor_surf - поверность заднего фона."""
    dif_modules_surface = pygame.Surface((150, 600), pygame.SRCALPHA)
    x = 75
    y = 50

    for dif_module in dif_modules:
        dif_module.x = x
        dif_module.y = y
        dif_module.surface = pygame.image.load(("images/constructor/modules/"+dif_module.image+".png"))
        dif_module.surface = pygame.transform.scale(dif_module.surface, (dif_module.b, dif_module.a))
        dif_modules_surface.blit(dif_module.surface, (dif_module.x, dif_module.y))
        price = FONT_small.render(str(dif_module.price), True, BLUE)
        #price_rect = pygame.draw.rect(dif_modules_surface, LIGHT_BLUE, (x-70, y+(dif_module.a / 3), 55, 30), width=1, border_radius=1)
        dif_modules_surface.blit(price, (x-60, y+(dif_module.a / 3)))

        y += dif_module.a + 10


    bg_constructor_surf.blit(dif_modules_surface, (0, 0))


def move_modules(moved_module, bg_constructor_surf, flag):
    """Функция отрисовывает движение модулей при взятии их игроком.
    :param dif_module_surf_list - список поверхностей модулей.
    :param bg_constructor_surf - поверность заднего фона.
    :param flag - указатель зажатия кнопки мыши
    :param k - номер элемента массива поверхостей модулей, который берёт пользователь."""
    x, y = pygame.mouse.get_pos()
    if flag:
        bg_constructor_surf.blit(moved_module.surface, (x, y))
    #print("move", moved_module.x)


"""def check_borders(moved_module):
    collide = False
    u, w = pygame.mouse.get_pos()
    for rocket_module in rocket_list:
        if rocket_module.x <= u + moved_module.b <= rocket_module.x + rocket_module.b and rocket_module.y <= moved_module.y <= rocket_module.y + rocket_module.a:
            collide = True
    return collide
    #print("check", moved_module.x)"""

def set_modules(moved_module, flag, rocket_list):
    """Функция добавляет модули в список ракеты.
    :param dif_module_surf_list - список поверхностей модулей
    :param flag - указатель зажатия кнопки мыши
    :param k - номер элемента массива поверхостей модулей, который берёт пользователь.
    :param rocket_list - список элементов ракеты"""
    global cash
    u, w = pygame.mouse.get_pos()
    if flag and cash - moved_module.price >= 0 and 200 <= u <= 600 and 50 <= w <= 550:
    #if flag and cash - moved_module.price >= 0 and 200 <= moved_module.x <= 600 and 50 <= moved_module.y <= 550:
        rocket_module = Module()
        rocket_module.type = moved_module.type
        rocket_module.m = moved_module.m
        rocket_module.fuel = moved_module.fuel
        rocket_module.price = moved_module.price
        rocket_module.resistance = moved_module.resistance
        rocket_module.force = moved_module.force
        rocket_module.image = moved_module.image
        rocket_module.a = moved_module.a
        rocket_module.b = moved_module.b
        rocket_module.x = u - u % 50
        rocket_module.y = w - w % 25
        #rocket_module.x = moved_module.x - moved_module.x % 50
        #rocket_module.y = moved_module.y - moved_module.y % 25
        rocket_module.surface = moved_module.surface
        rocket_list.append(rocket_module)
    #if 200 >= u >= 600 and 50 >= w >= 550:
     #   cash += moved_module.price
    #print("set", moved_module.x)

def draw_rocket(rocket_list, rocket_surface):
    """Функция рисует модули ракеты на поверности ракеты.
    :param rocket_list - список модулей ракеты
    :param rocket_surface - поверность рактеты."""
    for rocket_module in rocket_list:
        rocket_surface.blit(rocket_module.surface, (rocket_module.x - 200, rocket_module.y - 50))


def find_max_coord(rocket_list):
    """Функция находит наиболее близкий элемент к земле."""
    rocket_modules_y_bottom = []
    rocket_modules_y_top = []
    rocket_modules_x_left = []
    rocket_modules_x_right = []
    y_bottom = 0
    y_top = 0
    x_left = 0
    x_right = 0
    for rocket_module in rocket_list:
        rocket_modules_y_bottom.append(rocket_module.y + rocket_module.a - 50)
        rocket_modules_y_top.append(rocket_module.y - 50)
        rocket_modules_x_left.append(rocket_module.x - 200)
        rocket_modules_x_right.append(rocket_module.x + rocket_module.b - 200)

    if rocket_modules_y_top != [] and rocket_modules_y_bottom != []:
        y_bottom = max(rocket_modules_y_bottom)
        y_top = min(rocket_modules_y_top)

    if rocket_modules_x_left != [] and rocket_modules_x_right != []:
        x_left = min(rocket_modules_x_left)
        x_right = max(rocket_modules_x_right)

    return y_bottom, y_top, x_left, x_right


def delete_rocket(rocket_list):
    if buttons_off[6].check_button(pygame.mouse.get_pos()):
        rocket_list = []
    return rocket_list


flag1 = False
flag2 = False
k = -1
j = 0

blocks, engines, tanks, autopilot, fairings = read_modules_data_from_file('module_example')
rocket_list = []
click = [-1, -1, -1, -1, -1]

mouse_x, mouse_y = 0, 0


def recognise_modules(useless, mouse_x, mouse_y, click):
    """
    эта функция должна определять, запчасти какого рода надо показывать
    :param useless: значение переменной draw_screen
    :param mouse_x: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_y: вертикальная координата точки, в которой произошел щелчок мыши
    :param click: набор параметров, определяющих четность нажатия кнопки модуля
    :return: click
    """
    if (625 <= mouse_x <= 775) and (75 <= mouse_y <= 125) and useless == "constructor":
        click[0] = -1 * click[0]
        for i in 1, 2, 3, 4:
            click[i] = -1
    elif (625 <= mouse_x <= 775) and (150 <= mouse_y <= 200) and useless == "constructor":
        click[1] = -1 * click[1]
        for i in 0, 2, 3, 4:
            click[i] = -1
    elif (625 <= mouse_x <= 775) and (225 <= mouse_y <= 275) and useless == "constructor":
        click[2] = -1 * click[2]
        for i in 0, 1, 3, 4:
            click[i] = -1
    elif (625 <= mouse_x <= 775) and (300 <= mouse_y <= 350) and useless == "constructor":
        click[3] = -1 * click[3]
        for i in 0, 1, 2, 4:
            click[i] = -1
    elif (625 <= mouse_x <= 775) and (375 <= mouse_y <= 425) and useless == "constructor":
        click[4] = -1 * click[4]
        for i in 0, 1, 2, 3:
            click[i] = -1
    else:
        pass
    return click


def show_modules(click):
    dif_modules = []
    if click[0] == 1:
        dif_modules = tanks
        # draw_modules(tanks, bg_constructor_surf)
    if click[1] == 1:
        dif_modules = autopilot
        # draw_modules(autopilot, bg_constructor_surf)
    if click[2] == 1:
        dif_modules = engines
        # draw_modules(engines, bg_constructor_surf)
    if click[3] == 1:
        dif_modules = fairings
        # draw_modules(fairings, bg_constructor_surf)
    if click[4] == 1:
        dif_modules = blocks
        # draw_modules(blocks, bg_constructor_surf)
    return dif_modules


def draw_constructor_foo(eventus, click, rocket_list, rocket_surface, flag1, flag2, k, j):
    """
    Функция отрисовывает экран конструктора и все изменения, которые с ним происходят
    :param eventus: тип события мыши (функция должна понимать, когда надо брать координаты курсора мыши, а когда нет)
    :param click: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param rocket_list: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param rocket_surface: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flag1: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flag2: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param k: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param j: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :return: полностью отрисованный экран и все вводимые параметры
    """
    grid, bg_constructor_surf = render_bg()
    buttons_off, buttons_on = render_buttons()
    dif_modules = show_modules(click)

    if eventus == "mouse_button_down":
        x, y = pygame.mouse.get_pos()
        click = recognise_modules("constructor", x, y, click)
        if 625 <= x <= 775 and 450 <= y <= 500:
            rocket_list = []
        flag1 = True
        flag2 = False
        if check_module(dif_modules) > -1:
            k = check_module(dif_modules)
    if eventus == "mouse_button_up":
        j = k
        k = -1
        flag1 = False
        flag2 = True
    if flag1 and k >= 0:
        move_modules(dif_modules, bg_constructor_surf, flag1, k)
    if flag2 and j >= 0:
        set_modules(dif_modules, flag2, j, rocket_list)
        j = k
    draw_rocket(rocket_list, rocket_surface)
    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)
    draw_modules(dif_modules, bg_constructor_surf)
    draw_bg(grid, bg_constructor_surf, rocket_surface)
    draw_points()
    if not rocket_list:
        rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    return click, rocket_list, rocket_surface, flag1, flag2, k, j


if __name__ == '__main__':
    while True:
        grid, bg_constructor_surf, rocket_surface = render_bg()
        buttons_off, buttons_on = render_buttons()

        dif_modules = show_modules(click)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                rocket_list = delete_rocket(rocket_list)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click = recognise_modules("constructor", mouse_x, mouse_y, click)
                flag1 = True
                flag2 = False
                flag_dif = False
                flag_rock = False
                if check_module(dif_modules) > -1:
                    k = check_module(dif_modules)
                    moved_module = dif_modules[k]
                    flag_dif = True
                if check_module(rocket_list) > -1:
                    flag_rock = True
                    k = check_module(rocket_list)
                    moved_module = rocket_list[k]
                    rocket_list.pop(k)
            elif event.type == pygame.MOUSEBUTTONUP:
                j = k
                flag1 = False
                flag2 = True
                k = -1
        if flag1 and k >= 0 and flag_dif:
            move_modules(moved_module, bg_constructor_surf, flag1)

        if flag1 and k >= 0 and flag_rock:
            move_modules(moved_module, bg_constructor_surf, flag1)

        if flag2 and j >= 0 and flag_dif:
            set_modules(moved_module, flag2, rocket_list)
            cash -= moved_module.price
            j = k
            flag_dif = False

        if flag2 and j >= 0 and flag_rock:
            set_modules(moved_module, flag2, rocket_list)
            j = k
            flag_rock = False

        y_bottom, y_top, x_left, x_right = find_max_coord(rocket_list)

        draw_rocket(rocket_list, rocket_surface)

        draw_buttons(bg_constructor_surf, buttons_off, buttons_on)

        draw_modules(dif_modules, bg_constructor_surf)

        draw_bg(grid, bg_constructor_surf, rocket_surface)
        draw_points()
        if not rocket_list:
            rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)

        pygame.display.update()
        clock.tick(FPS)

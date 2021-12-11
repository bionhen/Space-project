from starship_modules import *
from starship_constructor import *
from starsip_rocket import *

pygame.init()

# pygame.mixer.music.load('images/constructor/Space_Oddity.mp3')
# pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60

FONT = pygame.font.SysFont('century gothic', 30, bold=True)
FONT_small = pygame.font.SysFont('century gothic', 24, bold=True)
pygame.font.init()

cash = 1000
BLUE = (39, 40, 91)
LIGHT_BLUE = (106, 139, 197)


class Button:
    """Класс Button (Кнопка, на которую наведен курсор)"""
    def __init__(self, filename, x, y):
        """
        Инициализация класса Button
        :param filename - имя файла с изображением кнопки
        :param x - координата левого верхнего угла по горизонтали
        :param y - координата левого верхнего угла по вертикали
        """
        self.x = x
        self.y = y
        self.button_surf = pygame.image.load(("images/constructor/"+filename+".png")).convert_alpha()


class ButtonOff(Button):
    """
    Инициализация класса ButtonOff, дочерний класс  (Кнопка, на которую не наведён курсор)
    :param filename - имя файла с изображением кнопки
    :param x - координата левого верхнего угла по горизонтали
    :param y - координата левого верхнего угла по вертикали
    """
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.button_off_surf_width = pygame.Surface.get_width(self.button_surf)
        self.button_off_surf_height = pygame.Surface.get_height(self.button_surf)

    def check_button(self, cur_event):
        """Метод проверяет, наведён ли курсор на кнопку"""
        if ((cur_event[0] >= self.x)
                and (cur_event[0] <= self.x + self.button_off_surf_width)
                and (cur_event[1] >= self.y)
                and (cur_event[1] <= self.y + self.button_off_surf_height)):
            button_checked = True
        else:
            button_checked = False
        return button_checked


def render_bg():
    """Функция генерирует составляющие фона: сетку, фон и поверхность ракеты"""
    grid_arg = pygame.image.load("images/constructor/grid.png").convert_alpha()  # сетка конструктора
    bg_constructor_surf_arg = pygame.image.load("images/constructor/bg_constructor.png").convert_alpha()  # задний фон
    rocket_surface_arg = pygame.Surface((400, 500), pygame.SRCALPHA)
    return grid_arg, bg_constructor_surf_arg, rocket_surface_arg


def draw_bg(grid_arg, bg_constructor_surf_arg, rocket_surface_arg):
    """Функция отрисовывает составляющие заднего фона (сетку, фон и ракету) на экране"""
    bg_constructor_surf_arg.blit(grid_arg, (200, 50))
    bg_constructor_surf_arg.blit(rocket_surface_arg, (200, 50))
    sc.blit(bg_constructor_surf_arg, (0, 0))


def render_buttons():
    """Функция генерирует кнопки"""
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

    buttons_off_arg = [fuel_off, autopilot_off, engines_off, fairings_off, modules_off, done_off, delete_off]
    buttons_on_arg = [fuel_on, autopilot_on, engines_on, fairings_on, modules_on, done_on, delete_on]

    return buttons_off_arg, buttons_on_arg


def draw_buttons(bg_surf, buttons_off_arg, buttons_on_arg):
    """
    Функция отрисовывает кнопки на заднем фоне слайда.
    :param bg_surf - поверность фона
    :param buttons_off_arg - список кнопок, на которые не наведён курсор
    :param buttons_on_arg - список кнопок, на которые наведён курсор
    """
    for i in range(len(buttons_off_arg)):
        bg_surf.blit(buttons_off_arg[i].button_surf, (buttons_off_arg[i].x, buttons_on_arg[i].y))
        if buttons_off_arg[i].check_button(pygame.mouse.get_pos()):
            bg_surf.blit(buttons_on_arg[i].button_surf, (buttons_on_arg[i].x, buttons_on_arg[i].y))


def calc_params(rocket_list_arg):
    """
    Функция рассчитывает общую массу самой ракеты и ее топлива
    :param rocket_list_arg: список запчастей, установленных на ракете
    """
    mass = 0
    fuel = 0
    for rocket_module in rocket_list_arg:
        mass += rocket_module.m
    for rocket_module in rocket_list_arg:
        fuel += rocket_module.fuel
    return mass, fuel


def draw_text(rocket_list_arg, bg_constructor_surf_arg):
    """Функция отрисовывает количество денег, массу ракеты и массу топлива на заднем фоне слайда"""
    mass, fuel = calc_params(rocket_list_arg)
    cash_text = FONT.render('cash: ' + str(cash), True, BLUE)
    fuel_text = FONT_small.render('fuel: ' + str(fuel), True, BLUE)
    mass_text = FONT_small.render('mass: ' + str(mass), True, BLUE)
    bg_constructor_surf_arg.blit(cash_text, (610, 20))
    bg_constructor_surf_arg.blit(fuel_text, (200, 555))
    bg_constructor_surf_arg.blit(mass_text, (350, 555))


def draw_modules(dif_modules_arg, bg_constructor_surf_arg):
    """
    Функция отрисовывает список модулей на заднем фоне слайда
    :param dif_modules_arg - список поверхностей модулей
    :param bg_constructor_surf_arg - поверность заднего фона
    """
    dif_modules_surface = pygame.Surface((150, 600), pygame.SRCALPHA)
    x = 75
    y = 50

    for dif_module in dif_modules_arg:
        dif_module.x = x
        dif_module.y = y
        dif_modules_surface.blit(dif_module.surface, (dif_module.x, dif_module.y))
        price = FONT_small.render(str(dif_module.price), True, BLUE)
        dif_modules_surface.blit(price, (x-60, y+(dif_module.a / 3)))
        y += dif_module.a + 10
    bg_constructor_surf.blit(dif_modules_surface, (0, 0))


def move_modules(moved_module_arg, bg_constructor_surf_arg, flag):
    """
    Функция отрисовывает движение модулей при взятии их игроком
    :param moved_module_arg - список поверхностей модулей
    :param bg_constructor_surf_arg - поверность заднего фона
    :param flag - указатель зажатия кнопки мыши
    """
    x, y = pygame.mouse.get_pos()
    if flag:
        bg_constructor_surf_arg.blit(moved_module_arg.surface, (x, y))


def set_modules(moved_module_arg, flag, rocket_list_arg):
    """
    Функция добавляет модули в список ракеты
    :param moved_module_arg - список поверхностей модулей
    :param flag - указатель зажатия кнопки мыши
    :param rocket_list_arg - список элементов ракеты
    """
    global cash
    u, w = pygame.mouse.get_pos()
    if flag and cash - moved_module_arg.price >= 0 and 200 <= u <= 600 and 50 <= w <= 550:
        rocket_module = Module()
        rocket_module.type = moved_module_arg.type
        rocket_module.m = moved_module_arg.m
        rocket_module.fuel = moved_module_arg.fuel
        rocket_module.price = moved_module_arg.price
        rocket_module.resistance = moved_module_arg.resistance
        rocket_module.force = moved_module_arg.force
        rocket_module.image = moved_module_arg.image
        rocket_module.a = moved_module_arg.a
        rocket_module.b = moved_module_arg.b
        rocket_module.x = u - u % 50
        rocket_module.y = w - w % 25
        rocket_module.surface = moved_module_arg.surface
        rocket_list_arg.append(rocket_module)


def draw_rocket(rocket_list, rocket_surface):
    """Функция рисует модули ракеты на поверности ракеты.
    :param rocket_list - список модулей ракеты
    :param rocket_surface - поверность рактеты."""
    for rocket_module in rocket_list:
        rocket_surface.blit(rocket_module.surface, (rocket_module.x - 200, rocket_module.y - 50))


def draw_center_mass(rocket_list, rocket_surface):
    m = 0
    my = 0
    mx = 0
    if rocket_list != []:
        for module in rocket_list:
            m += module.m
            my += module.m * (module.y - 50 + module.a/2)
            mx += module.m * (module.x - 200 + module.b/2)
        y_center_mass = my / m
        x_center_mass = mx / m

        center_mass = pygame.Surface((10, 10))
        center_mass.fill("tomato")
        rocket_surface.blit(center_mass, (x_center_mass-5, y_center_mass-5))


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


flag1 = False
flag2 = False
flag_dif = False
flag_rock = False
k = -1
j = 0

blocks, engines, tanks, autopilot, fairings = read_modules_data_from_file('module_example')
rocket_list = []
click = [-1, -1, -1, -1, -1]
mouse_x, mouse_y = 0, 0
moved_module = Module()


def draw_constructor_foo(eventus, click, rocket_list, moved_module, flag1, flag2, flag_dif, flag_rock, k, j):
    """
    Функция отрисовывает экран конструктора и все изменения, которые с ним происходят
    :param eventus: тип события мыши (функция должна понимать, когда надо брать координаты курсора мыши, а когда нет)
    :param click: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param rocket_list: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flag1: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flag2: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flag_dif: еще один параметр, который должен сохраняться
    :param flag_rock: еще один параметр, который должен сохраняться
    :param k: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param j: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :return: полностью отрисованный экран и все вводимые параметры
    """
    global cash
    grid, bg_constructor_surf, rocket_surface = render_bg()
    buttons_off, buttons_on = render_buttons()
    dif_modules = show_modules(click)

    if eventus == "mouse_button_down":
        # rocket_list = delete_rocket(rocket_list)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 625 <= mouse_x <= 775 and 450 <= mouse_y <= 500:
            rocket_list = []
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
    if eventus == "mouse_button_up":
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

    draw_text(rocket_list, bg_constructor_surf)
    draw_rocket(rocket_list, rocket_surface)
    draw_center_mass(rocket_list, rocket_surface)
    draw_buttons(bg_constructor_surf, buttons_off, buttons_on)
    draw_modules(dif_modules, bg_constructor_surf)
    draw_bg(grid, bg_constructor_surf, rocket_surface)

    if not rocket_list:
        rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    rocket = Rocket()
    rocket.list = rocket_list
    rocket.surface = rocket_surface
    pygame.display.update()
    clock.tick(FPS)
    return click, rocket_list, moved_module, flag1, flag2, flag_dif, flag_rock, k, j


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

        draw_text(rocket_list, bg_constructor_surf)

        draw_rocket(rocket_list, rocket_surface)

        draw_center_mass(rocket_list, rocket_surface)

        draw_buttons(bg_constructor_surf, buttons_off, buttons_on)

        draw_modules(dif_modules, bg_constructor_surf)

        draw_bg(grid, bg_constructor_surf, rocket_surface)

        if not rocket_list:
            rocket_surface = pygame.Surface((400, 500), pygame.SRCALPHA)
        rocket = Rocket()
        rocket.list = rocket_list
        rocket.surface = rocket_surface
        pygame.display.update()
        clock.tick(FPS)

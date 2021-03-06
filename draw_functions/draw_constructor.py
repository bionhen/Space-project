from draw_functions.constants import *
from draw_functions.draw_menu import Button, ButtonOff
from draw_functions.starship_rocket import *


def render_bg():
    """Функция генерирует составляющие фона: сетку, фон и поверхность ракеты
    :return grid_arg -  поверхность сетки
    :return bg_constructor_surf_arg - повехность заднего фона
    :return rocket_surface_arg - повехность ракеты"""
    grid_arg = pygame.image.load("images/constructor/grid.png").convert_alpha()  # сетка конструктора
    bg_constructor_surf_arg = pygame.image.load("images/constructor/bg_constructor.png").convert_alpha()  # задний фон
    rocket_surface_arg = pygame.Surface((400, 500), pygame.SRCALPHA)

    return grid_arg, bg_constructor_surf_arg, rocket_surface_arg


def draw_bg(grid_arg, bg_constructor_surf_arg, rocket_surface_arg):
    """Функция отрисовывает составляющие заднего фона (сетку, фон и ракету) на экране
    :param grid_arg - поверхность сетки
    :param bg_constructor_surf_arg - поверхность заднего фона
    :param rocket_surface_arg - поверхность ракеты"""
    bg_constructor_surf_arg.blit(grid_arg, (200, 50))
    bg_constructor_surf_arg.blit(rocket_surface_arg, (200, 50))
    sc.blit(bg_constructor_surf_arg, (0, 0))


def render_buttons():
    """Функция генерирует кнопки
    :return buttons_off_arg - список объектов кнопок класса ButtonOff
    :return buttons_on_arg - список объектов кнопок класса Button"""

    fuel_on = Button('constructor/fuel_on', 625, 75)
    fuel_off = ButtonOff('constructor/fuel_off', 625, 75)
    autopilot_on = Button('constructor/autopilot_on', 625, 150)
    autopilot_off = ButtonOff('constructor/autopilot_off', 625, 150)
    engines_on = Button('constructor/engines_on', 625, 225)
    engines_off = ButtonOff('constructor/engines_off', 625, 225)
    fairings_on = Button('constructor/fairings_on', 625, 300)
    fairings_off = ButtonOff('constructor/fairings_off', 625, 300)
    modules_on = Button('constructor/modules_on', 625, 375)
    modules_off = ButtonOff('constructor/modules_off', 625, 375)
    done_on = Button('constructor/done_on', 625, 525)
    done_off = ButtonOff('constructor/done_off', 625, 525)
    delete_on = Button('constructor/delete_on', 625, 450)
    delete_off = ButtonOff('constructor/delete_off', 625, 450)

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


def calc_params(rocket_arg):
    """
    Функция рассчитывает общую массу самой ракеты и ее топлива
    :param rocket_arg:  объект ракета
    :return mass - масса ракеты
    :return fuel - топливо рактеы
    """
    rocket_arg.mass = 0
    rocket_arg.fuel = 0
    for rocket_module in rocket_arg.list:
        rocket_arg.mass += rocket_module.m
    for rocket_module in rocket_arg.list:
        rocket_arg.fuel += rocket_module.fuel
        rocket_arg.fuel_max = rocket_arg.fuel


def draw_text(rocket_arg, bg_constructor_surf_arg, cash_arg):
    """Функция отрисовывает количество денег, массу ракеты и массу топлива на заднем фоне слайда
    :param rocket_arg - объект ракета
    :param bg_constructor_surf_arg - задний фон
    :param cash_arg - количество денег"""
    calc_params(rocket_arg)
    if cash > 0:
        cash_text = FONT.render('cash: ' + str(cash_arg), True, BLUE)
    else:
        cash_text = FONT.render('cash: ' + str(0), True, BLUE)
    fuel_text = FONT_small.render('fuel: ' + str(rocket_arg.fuel), True, BLUE)
    mass_text = FONT_small.render('mass: ' + str(rocket_arg.mass), True, BLUE)
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
    bg_constructor_surf_arg.blit(dif_modules_surface, (0, 0))


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


def check_point(cord_x, cord_y, rocket_module):
    upped_1 = False
    if (rocket_module.x + 10 < cord_x < rocket_module.x + rocket_module.b - 10) and \
            (rocket_module.y + 10 < cord_y < rocket_module.y + rocket_module.a - 10):
        upped_1 = True
    return upped_1


def check_dist(cord_x, cord_y, rocket_module, moved_module_arg):
    upped_2 = False
    if rocket_module.x + rocket_module.b + 50 < cord_x or cord_x < rocket_module.x - 50 or \
            rocket_module.y + rocket_module.a + 45 < cord_y or cord_y < rocket_module.y - moved_module_arg.a - 45:
        upped_2 = True
    return upped_2


def check_modules_pos(rocket_list_arg, moved_module_arg):
    upped = False
    upped_2_list = []
    x_mouse, y_mouse = pygame.mouse.get_pos()
    moved_module_x_r_u, moved_module_y_r_u = x_mouse, y_mouse - 10
    moved_module_x_l_u, moved_module_y_l_u = x_mouse + moved_module_arg.b, y_mouse - 10
    moved_module_x_r_d, moved_module_y_r_d = x_mouse, y_mouse + moved_module_arg.a
    moved_module_x_l_d, moved_module_y_l_d = x_mouse + moved_module_arg.b, y_mouse + moved_module_arg.a
    moved_module_x_c, moved_module_y_c = x_mouse + moved_module_arg.b/2, y_mouse + moved_module_arg.a/2
    moved_module_point = [(moved_module_x_r_u, moved_module_y_r_u), (moved_module_x_l_u, moved_module_y_l_u),
                          (moved_module_x_r_d, moved_module_y_r_d), (moved_module_x_l_d, moved_module_y_l_d),
                          (moved_module_x_c, moved_module_y_c)]
    for rocket_module in rocket_list_arg:
        for i in range(len(moved_module_point)):
            upped_1 = check_point(moved_module_point[i][0], moved_module_point[i][1], rocket_module)
            if upped_1:
                upped = True
                break
    for rocket_module in rocket_list_arg:
        upped_2 = check_dist(moved_module_x_r_u, moved_module_y_r_u, rocket_module, moved_module_arg)
        if upped_2:
            upped_2_list.append(upped_2)
    if len(upped_2_list) == len(rocket_list_arg):
        upped = True
    return upped


def set_modules(moved_module_arg, flag, rocket_arg):
    """
    Функция добавляет модули в список ракеты
    :param moved_module_arg - список поверхностей модулей
    :param flag - указатель зажатия кнопки мыши
    :param rocket_arg - объект ракета
    """
    u, w = pygame.mouse.get_pos()
    if flag and cash - moved_module_arg.price >= 0 and 200 <= u <= 600 and 50 <= w <= 550 and rocket_arg.list == []:
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
        rocket_arg.list.append(rocket_module)
    elif flag and cash - moved_module_arg.price >= 0 and 200 <= u <= 600 and 50 <= w <= 550 and \
            not check_modules_pos(rocket_arg.list, moved_module_arg):
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
        rocket_arg.list.append(rocket_module)


def check_module(surf_list):
    """
    функция, проверяющая попадание мышью в область, где находится модуль из surf_list
    :param surf_list: список модулей, для которых выполняетсяя проверка
    :return: k - номер модуля для которго мышь попадает в его область
    """
    kk = -1
    x, y = pygame.mouse.get_pos()
    for i in range(len(surf_list)):
        if surf_list[i].x <= x <= surf_list[i].x + surf_list[i].b and \
                surf_list[i].y <= y <= surf_list[i].y + surf_list[i].a:
            kk = i
    return kk


def draw_rocket(rocket_list_arg, rocket_surface_arg):
    """
    Функция рисует модули ракеты на поверности ракеты
    :param rocket_list_arg - список модулей ракеты
    :param rocket_surface_arg - поверность рактеты
    """
    for rocket_module in rocket_list_arg:
        rocket_surface_arg.blit(rocket_module.surface, (rocket_module.x - 200, rocket_module.y - 50))


def draw_center_mass(rocket_list_arg, rocket_surface_arg):
    """Функция считает координаты центра масс ракеты, постороенной игроком, и рисует на его месте небольшой квадрат"""
    m = 0
    my = 0
    mx = 0
    if rocket_list_arg:
        for module in rocket_list_arg:
            m += module.m
            my += module.m * (module.y - 50 + module.a/2)
            mx += module.m * (module.x - 200 + module.b/2)
        y_center_mass = my / m
        x_center_mass = mx / m
        center_mass = pygame.Surface((10, 10))
        center_mass.fill("tomato")
        rocket_surface_arg.blit(center_mass, (x_center_mass - 5, y_center_mass - 5))


def recognise_modules(useless, mouse_xx, mouse_yy, click_arg):
    """
    Эта функция должна определять, на какую кнопку нажал игрок
    :param useless: значение переменной draw_screen
    :param mouse_xx: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_yy: вертикальная координата точки, в которой произошел щелчок мыши
    :param click_arg: набор параметров, определяющих четность нажатия кнопки модуля
    :return: click
    """
    if (625 <= mouse_xx <= 775) and (75 <= mouse_yy <= 125) and useless == "constructor":
        click_arg[0] = -1 * click_arg[0]
        for i in 1, 2, 3, 4:
            click_arg[i] = -1
    elif (625 <= mouse_xx <= 775) and (150 <= mouse_yy <= 200) and useless == "constructor":
        click_arg[1] = -1 * click_arg[1]
        for i in 0, 2, 3, 4:
            click_arg[i] = -1
    elif (625 <= mouse_xx <= 775) and (225 <= mouse_yy <= 275) and useless == "constructor":
        click_arg[2] = -1 * click_arg[2]
        for i in 0, 1, 3, 4:
            click_arg[i] = -1
    elif (625 <= mouse_xx <= 775) and (300 <= mouse_yy <= 350) and useless == "constructor":
        click_arg[3] = -1 * click_arg[3]
        for i in 0, 1, 2, 4:
            click_arg[i] = -1
    elif (625 <= mouse_xx <= 775) and (375 <= mouse_yy <= 425) and useless == "constructor":
        click_arg[4] = -1 * click_arg[4]
        for i in 0, 1, 2, 3:
            click_arg[i] = -1
    else:
        pass
    return click_arg


def show_modules(click_arg):
    """Функция определяет, запчасти какого рода надо показывать"""
    dif_modules_arg = []
    if click_arg[0] == 1:
        dif_modules_arg = tanks
    if click_arg[1] == 1:
        dif_modules_arg = autopilot
    if click_arg[2] == 1:
        dif_modules_arg = engines
    if click_arg[3] == 1:
        dif_modules_arg = fairings
    if click_arg[4] == 1:
        dif_modules_arg = blocks
    return dif_modules_arg


flag1, flag2, flag_dif, flag_rock = False, False, False, False
k = -1
j = 0
blocks, engines, tanks, autopilot, fairings = read_modules_data_from_file('images/module_example')
click = [-1, -1, -1, -1, -1]
mouse_x, mouse_y = 0, 0
moved_module = Module()


def draw_constructor_foo(events, clicks, rocket_arg, moved_modules, flags1, flags2, flags_dif, flags_rock, ks, js,
                         cash_arg):
    """
    Функция отрисовывает экран конструктора и все изменения, которые с ним происходят
    :param events: тип события мыши (функция должна понимать, когда надо брать координаты курсора мыши, а когда нет)
    :param clicks: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param rocket_arg: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param moved_modules: параметр должен сохраняться в ходе выполнения функции, поэтому его надо вводить и выводить
    :param flags1: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flags2: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param flags_dif: еще один параметр, который должен сохраняться
    :param flags_rock: еще один параметр, который должен сохраняться
    :param ks: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param js: параметр должен сохраняться в ходе выполнения функции, поэтому придется его вводить и выводить
    :param cash_arg - количество денег
    :return: полностью отрисованный экран и все вводимые параметры
    """
    grids, bg_constructors_surf, rocket_arg.surface = render_bg()
    buttons_offs, buttons_ons = render_buttons()
    dif_modules_arg = show_modules(clicks)
    if events == "mouse_button_down":
        mouse_xx, mouse_yy = pygame.mouse.get_pos()
        if 625 <= mouse_xx <= 775 and 450 <= mouse_yy <= 500:
            rocket_arg.list = []
            cash_arg = 1000
        clicks = recognise_modules("constructor", mouse_xx, mouse_yy, clicks)
        flags1 = True
        flags2 = False
        flags_dif = False
        flags_rock = False
        if check_module(dif_modules_arg) > -1:
            ks = check_module(dif_modules_arg)
            moved_modules = dif_modules_arg[ks]
            flags_dif = True
        if check_module(rocket_arg.list) > -1:
            flags_rock = True
            ks = check_module(rocket_arg.list)
            moved_modules = rocket_arg.list[ks]
            rocket_arg.list.pop(ks)
    if events == "mouse_button_up":
        js = ks
        flags1 = False
        flags2 = True
        ks = -1
    if flags1 and ks >= 0 and flags_dif:
        move_modules(moved_modules, bg_constructors_surf, flags1)
    if flags1 and ks >= 0 and flags_rock:
        move_modules(moved_modules, bg_constructors_surf, flags1)
    if flags2 and js >= 0 and flags_dif:
        set_modules(moved_modules, flags2, rocket_arg)
        cash_arg -= moved_modules.price
        js = ks
        flags_dif = False
    if flags2 and js >= 0 and flags_rock:
        set_modules(moved_modules, flags2, rocket_arg)
        js = ks
        flags_rock = False

    draw_text(rocket_arg, bg_constructors_surf, cash_arg)
    draw_rocket(rocket_arg.list, rocket_arg.surface)
    draw_center_mass(rocket_arg.list, rocket_arg.surface)
    draw_buttons(bg_constructors_surf, buttons_offs, buttons_ons)
    draw_modules(dif_modules_arg, bg_constructors_surf)
    draw_bg(grids, bg_constructors_surf, rocket_arg.surface)

    if not rocket_arg.list:
        rocket_arg.surface = pygame.Surface((400, 500), pygame.SRCALPHA)
    return clicks, rocket_arg, moved_modules, flags1, flags2, flags_dif, flags_rock, ks, js, cash_arg

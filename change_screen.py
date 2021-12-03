from draw_constructor import *
mouse_click = [-1, -1, -1, -1, -1]


def show_screen(draw_screen, mouse_x, mouse_y):
    """
    Эта функция проверяет, надо ли переключить экран (например, перейти от главного меню к списку миссий),
    и если надо, то меняет параметр draw_screen соответствующим образом
    :param draw_screen: параметр, определяющий, какой экран включен
    :param mouse_x: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_y: вертикальная координата точки, в которой произошел щелчок мыши
    :return: draw_screen
    """
    if (draw_screen == "menu") and (325 <= mouse_x <= 475) and (400 <= mouse_y <= 450):
        draw_screen = "list_of_missions"
    elif (draw_screen == "list_of_missions") and (100 <= mouse_x <= 400) and (150 <= mouse_y <= 200):
        draw_screen = "constructor"
    elif (draw_screen == "list_of_missions") and (100 <= mouse_x <= 400) and (250 <= mouse_y <= 300):
        draw_screen = "constructor"
    elif draw_screen == "constructor":
        pass
    return draw_screen


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
    if click[0] == 1:
        draw_modules(tanks, bg_constructor_surf)
    if click[1] == 1:
        draw_modules(autopilot, bg_constructor_surf)
    if click[2] == 1:
        draw_modules(engines, bg_constructor_surf)
    if click[3] == 1:
        draw_modules(fairings, bg_constructor_surf)
    if click[4] == 1:
        draw_modules(blocks, bg_constructor_surf)

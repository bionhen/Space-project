from draw_constructor import *


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


def recognise_modules(useless, mouse_x, mouse_y):
    """
    эта функция должна определять, запчасти какого рода надо показывать
    :param useless: значение переменной draw_screen
    :param mouse_x: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_y: вертикальная координата точки, в которой произошел щелчок мыши
    :return: spare_part
    """
    if (625 <= mouse_x <= 775) and (75 <= mouse_y <= 125) and useless == "constructor":
        spare_part = "fuel"
    elif (625 <= mouse_x <= 775) and (150 <= mouse_y <= 200) and useless == "constructor":
        spare_part = "autopilot"
    elif (625 <= mouse_x <= 775) and (225 <= mouse_y <= 275) and useless == "constructor":
        spare_part = "engines"
    elif (625 <= mouse_x <= 775) and (300 <= mouse_y <= 350) and useless == "constructor":
        spare_part = "fairings"
    elif (625 <= mouse_x <= 775) and (375 <= mouse_y <= 425) and useless == "constructor":
        spare_part = "modules"
    else:
        spare_part = "nothing"
    return spare_part


def show_modules(spare_part):
    if spare_part == "fuel":
        draw_modules(blocks)
    if spare_part == "autopilot":
        print("autopilot")
    if spare_part == "engines":
        pass
    if spare_part == "fairings":
        pass
    if spare_part == "modules":
        pass
    if spare_part == "nothing":
        pass

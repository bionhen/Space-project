def show_screen(draw_screen, mouse_xx, mouse_yy):
    """
    Эта функция проверяет, надо ли переключить экран (например, перейти от главного меню к списку миссий),
    и если надо, то меняет параметр draw_screen соответствующим образом
    :param draw_screen: параметр, определяющий, какой экран включен
    :param mouse_xx: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_yy: вертикальная координата точки, в которой произошел щелчок мыши
    :return: draw_screen
    """
    if (draw_screen == "menu") and (300 <= mouse_xx <= 500) and (400 <= mouse_yy <= 450):
        draw_screen = "list_of_missions"
    elif (draw_screen == "list_of_missions") and (100 <= mouse_xx <= 400) and (150 <= mouse_yy <= 200):
        draw_screen = "constructor"
    elif (draw_screen == "list_of_missions") and (100 <= mouse_xx <= 400) and (250 <= mouse_yy <= 300):
        draw_screen = "constructor"
    elif (draw_screen == "constructor") and (625 <= mouse_xx <= 775) and (525 <= mouse_yy <= 575):
        draw_screen = "flying_unprepared"
    return draw_screen


def recognise_modules(useless, mouse_xx, mouse_yy, click_arg):
    """
    Эта функция должна определять, запчасти какого рода надо показывать
    :param useless: значение переменной draw_screen
    :param mouse_xx: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_yy: вертикальная координата точки, в которой произошел щелчок мыши
    :param click_arg: набор параметров, определяющих четность нажатия кнопки модуля
    :return: click_arg
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

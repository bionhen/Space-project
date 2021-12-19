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
        draw_screen = "constructor_1"
    elif (draw_screen == "list_of_missions") and (100 <= mouse_xx <= 400) and (250 <= mouse_yy <= 300):
        draw_screen = "constructor_2"
    elif (draw_screen == "constructor_1") and (625 <= mouse_xx <= 775) and (525 <= mouse_yy <= 575):
        draw_screen = "flying_prepared"
    elif (draw_screen == "constructor_2") and (625 <= mouse_xx <= 775) and (525 <= mouse_yy <= 575):
        draw_screen = "space_flying"
    return draw_screen

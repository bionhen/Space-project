def show_screen(draw_screen, mouse_x, mouse_y):
    """
    Эта функция проверяет, надо ли переключить экран (например, перейти от главного меню к списку миссий),
    и если надо, то меняет параметр draw_screen соответствующим образом
    :param draw_screen: параметр, определяющий, какой экран включен
    :param mouse_x: горизонтальная координата точки, в которой произошел щелчок мыши
    :param mouse_y: вертикальная координата точки, в которой произошел щелчок мыши
    :return: draw_screen
    """
    if (draw_screen == "menu") and (mouse_x >= 325) and (mouse_x <= 475) and (mouse_y <= 500) and mouse_y >= 400:
        draw_screen = "list_of_missions"
    # в следующие 2 цикла if надо вставить реальные границы кнопок
    elif (draw_screen == "list_of_missions") and (mouse_x >= 1) and (mouse_x <= 2) and (mouse_y <= 3) and mouse_y >= 4:
        draw_screen == "constructor"
    elif (draw_screen == "constructor") and (mouse_x >= 1) and (mouse_x <= 2) and (mouse_y <= 3) and mouse_y >= 4:
        draw_screen == "mission_1"
    # по мере надобности будем добавлять сциклы if
    return draw_screen

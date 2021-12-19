from draw_functions.constants import *
from draw_functions.draw_menu import Button, ButtonOff


def render_bg(screen_width=WIDTH, screen_height=HEIGHT):
    bg_missions_surf = pygame.image.load("images/missions/missions_bg.png").convert_alpha()
    bg_missions_surf = pygame.transform.scale(bg_missions_surf, (screen_width, screen_height))

    return bg_missions_surf


def render_buttons():
    """Функция загружает изобаржения кнопок
    :params None
    :return buttons_off_arg - список объектов кнопок класса ButtonOff
    :return buttons_on_arg - список объектов кнопок класса Button"""

    orbit = Button('missions/entering orbit on', 100, 150)
    orbit_off = ButtonOff('missions/entering orbit', 100, 150)
    moon = Button('missions/flight to the moon on', 100, 250)
    moon_off = ButtonOff('missions/flight to the moon', 100, 250)

    buttons_off_arg = [orbit_off, moon_off]
    buttons_on_arg = [orbit, moon]

    return buttons_off_arg, buttons_on_arg


def draw_buttons(bg_surf, buttons_off_arg, buttons_on_arg):
    """Функция отрисовыет загруженные изобрадения кнопок.
    :param bg_surf - поверхность, на которой отображаются кнопки.
    :param buttons_off_arg - список объектов кнопок класса ButtonOff
    :param buttons_on_arg - список объектов кнопок класса Button"""

    for i in range(len(buttons_off_arg)):
        bg_surf.blit(buttons_off_arg[i].button_surf, (buttons_off_arg[i].x, buttons_on_arg[i].y))
        if buttons_off_arg[i].check_button(pygame.mouse.get_pos()):
            bg_surf.blit(buttons_on_arg[i].button_surf, (buttons_on_arg[i].x, buttons_on_arg[i].y))


def draw_bg(bg_surf):
    """Функция рисует задний фон на главном экране.
    :param bg_surf - поверхность заднего фона"""
    sc.blit(bg_surf, (0, 0))


def draw_missions_foo():
    """Функция рисует задний фон на главном экране.
    :params None"""
    bg_missions_surf = render_bg(screen_width=WIDTH, screen_height=HEIGHT)
    buttons_off, buttons_on = render_buttons()
    draw_buttons(bg_missions_surf, buttons_off, buttons_on)
    draw_bg(bg_missions_surf)

import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))


def load_image(i, x, y):
    """
    Эта функция нужна для загрузки картинки
    :param i: полный путь к изображению
    :param x: масштаб по вертикальной оси
    :param y: масштаб по горизонтальной оси
    :return: изображение в требуемом масштабе
    """
    menu_bg_surf = pygame.image.load(i).convert()
    menu_bg_surf = pygame.transform.scale(menu_bg_surf, (x, y))
    return menu_bg_surf


def draw_menu(mouse_x, mouse_y):
    """
    Эта функция рисует главное меню в игре. Цвет кнопок зависит от того, указывает ли на нее курсор
    :param mouse_x: горизонтальная координата курсора
    :param mouse_y: вертикальная координата курсора
    :return:
    """
    a = load_image("images/menu/space_bg_4.jpg", 800, 600)
    b = load_image("images/menu/Кнопка Missions 2.png", 150, 50)
    c = load_image("images/menu/Кнопка Missions нажатая 1.png", 150, 50)
    screen.blit(a, (0, 0))
    if (mouse_x >= 325) and (mouse_x <= 475) and (mouse_y <= 450) and mouse_y >= 400:
        screen.blit(c, (325, 400))
    else:
        screen.blit(b, (325, 400))

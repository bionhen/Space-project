import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))


def load_image(i, x, y):
    """
    эта функция загружает в переменную картинку в нужном масштабе
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
    Эта функция отрисовывает экран главного меню в зависимости от того, наведен ли курсор мыши нв кнопку
    :param mouse_x: горизонтальная координата курсора
    :param mouse_y: вертикальная координата курсора
    """
    a = load_image("images/menu/space_bg_4.jpg", 800, 600)
    b = load_image("images/menu/Кнопка Missions 2.png", 150, 50)
    c = load_image("images/menu/Кнопка Missions нажатая 1.png", 150, 50)
    screen.blit(a, (0, 0))
    if (mouse_x >= 325) and (mouse_x <= 475) and (mouse_y <= 450) and mouse_y >= 400:
        screen.blit(c, (325, 400))
    else:
        screen.blit(b, (325, 400))

import pygame


def check_module(surf_list):
    """
    функция, проверяющая попадание мышью в область, где находится модуль из surf_list
    :param surf_list: список модулей, для которых выполняетсяя проверка
    :return: k - номер модуля для которго мышь попадает в его область
    """
    k = -1
    x, y = pygame.mouse.get_pos()
    for i in range(len(surf_list)):
        if surf_list[i].x <= x <= surf_list[i].x + surf_list[i].b and surf_list[i].y <= y <= surf_list[i].y + surf_list[i].a:
            k = i
    return k


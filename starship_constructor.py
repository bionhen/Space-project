import pygame

def module_upgrade(module, resistance, fuel, mass, force, module_price, price, cash):
    """
    функция улучшения модуля
    Args:
    module - улучшаемый модуль
    resistance - изменение прочности
    fuel - изменение количества топлива, которое несет модуль
    mass - изменение массы модуля
    force - изменение тяги элемента
    module_price - иизменение цены модуля
    price - цена улучшения
    cash - игровая валюта, которая есть у игрока
    """
    module.resistance += resistance
    module.fuel += fuel
    module.mass += mass
    module.force += force
    module.price += module_price
    cash -= price


def add_module(rocket, module, cash):
    """
    функция добавления модуля в состав ракеты
    Args:
    rocket - список, состоящий из модулей ракеты
    module - добавляемый модуль
    cash - игровая валюта, которая есть у игрока
    """
    rocket.add(module)
    cash -= module.price


def net():
    """
    функция создает двумерную сетку для размещения элементов

    net_list - кортеж кортежей с значением клеток по правилу ij-ая клетка содержит число 10*i+j
    """
    #width = 800
    #height = 600
    net_list = []
    for i in range(20):
        net_list.append([0] * 8)
    for i in range(20):
        for j in range(8):
            net_list[i][j] = 1 + 10 * i + j


def set_module(module, main_surface):
    """
    Функция ставит изображение модуля в левый верхний угол сетки
    Args:
    module: -экземпляр класса модуль
    main_surface: главная поверхность
    """
    x, y = pygame.mouse_get_pos
    sc = main_surface
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 100 < x < 700 and 50 < y < 650:
                sc.blit(module.image, (x-x % 50-100, y-50-y % 25))

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
    # width = 800
    # height = 600
    net_list = []
    for i in range(20):
        net_list.append([0] * 8)
    for i in range(20):
        for j in range(8):
            net_list[i][j] = 1 + 10 * i + j


def check_module(self, cur_event):
    if ((cur_event[0] >= self.x)
            and (cur_event[0] <= self.x + self.button_off_surf_width)
            and (cur_event[1] >= self.y)
            and (cur_event[1] <= self.y + self.button_off_surf_height)):
        button_checked = True
    else:
        button_checked = False
    return button_checked


def module_moving(module, main_surface):
    """
    Функция перемещения модуля после его выбора в левом меню

    """
    x, y = pygame.mouse.get_pos
    sc = main_surface
    flag1 = False
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if check_module(module, [x, y]):
                flag1 = True
        if event.type == pygame.MOUSEBUTTONUP:
            flag1 = False
        while flag1:
            sc.blit(module.image, (x - module.b / 2, y - module.a / 2))


def set_module(module, cash, rocket_surface):
    """
    Функция ставит изображение модуля в левый верхний угол сетки
    Args:
    module: экземпляр класса модуль
    main_surface: главная поверхность
    """
    x, y = pygame.mouse_get_pos
    sc = rocket_surface
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTOUP:
            if 100 < x < 700 and 50 < y < 650:
                cash -= module.price
                sc.blit(module.image, (x - x % 50, y - y % 25))


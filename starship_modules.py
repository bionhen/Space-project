# переменная cash - глобальная, отвечает за модуль
import pygame


class Module:
    """
    Класс, описывающий модули ракеты, например элементы корпуса или топливные баки
    """

    m = 0
    """собственная масса модуля """

    fuel = 0
    """собственное значение топлива, 0 - для модулей без топлива"""

    price = 0
    """собственная цена модуля"""

    resistance = 0
    """собственная прочность модуля"""

    force = 0
    """собственная тяга модуля"""

    image = ' '
    "название изображения"

    a = 0
    "высота модуля"

    b = 0
    "ширина модуля"

    surface = pygame.image.load("images/modules/"+image+".png").convert_alpha()


def read_modules_data_from_file(input_filename):
    """Cчитывает данные о модулях из файла, создаёт сами модули
    и вызывает создание их графических образов
    Args:
    **input_filename** — имя входного файла
    """

    modules = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            else:
                module = Module()
                parse_modules_parameters(line, module)
                modules.append(module)
    return modules


def parse_modules_parameters(line, module):
    """Считывает данные о модуле из строки.
    Входная строка должна иметь слеюущий формат:
    module m fuel price resistance force a b image
    Args:
    **line** — строка с описание звезды.
    **module** — объект звезды.
    """
    module_list = []
    for i in range(len(line)):
        if line[i] == ' ':
            module_list.append(i)
    module.m = int(float(line[module_list[0]+1:module_list[1]]))
    module.fuel = int(float(line[module_list[1] + 1:module_list[2]]))
    module.price = int(float(line[module_list[2] + 1:module_list[3]]))
    module.resistance = int(float(line[module_list[3] + 1:module_list[4]]))
    module.force = int(float(line[module_list[4] + 1:module_list[5]]))
    module.a = int(float(line[module_list[5] + 1:module_list[6]]))
    module.b = int(float(line[module_list[6] + 1:module_list[7]]))
    module.image = (line[module_list[1] + 1:])

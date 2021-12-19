import numpy as np
from random import *

g = 9.81
G = 6.67 * 10 ** (-11)
M = 6.02 * 10 ** 24


def force_coord(flag, engine_type, rocket_e, f_e_y, f_e_x):
    """
    функция рассчитывающая значения силы при условии flag
    :param flag: - флаг, если True - то двигатели включены, False - отключены
    :param engine_type: строка, являющаяся обозначением типа двигателя
    :param rocket_e: экземпляр класса Rocket, для которого рассчитывается сила
    :param f_e_y: параметер силы тяги по y до прибавления сил engine_type
    :param f_e_x: параметер силы тяги по x до прибавления сил engine_type
    :return: f_e_y, f_e_x - параметры силы после прибавления
    """
    if flag:
        for module in rocket_e.list:
            if rocket_e.fuel >= 0 and module.type == engine_type:
                f_e_y += module.force * np.cos(rocket_e.angle*np.pi/180) * 100
                f_e_x += module.force * np.sin(rocket_e.angle*np.pi/180) * 100
                rocket_e.fuel -= module.force * 0.0005
    return f_e_y, f_e_x


def moment_coord(flag, rocket_e, module, module_type, x_c, mf):
    """
    Функция, прибавляющая к mf - моменту сил, значения моментов от определенных двигателей
    :param flag: флаг, если True - то двигатели включены, False - отключены
    :param rocket_e: экземпляр класса Rocket, для которого рассчитывается сила
    :param module: экземпляр класса module
    :param module_type: - строка, являющаяся обозначением типа двигателя
    :param x_c: - значение координаты центра масс
    :param mf: - момент сил до прибавления
    :return: mf - момент сил после прибавления
    """
    if flag and rocket_e.fuel >= 0:
        if module.type == module_type:
            rocket_e.fuel -= module.force * 0.001
            mf += module.force * (module.x + module.b / 2 - x_c)
    return mf


def force_calc(rocket_obj, flag, flag_l, flag_r, sign):
    """
    функция рассчета сил, действующих на ракету
    получает объект класса rocket, возвращает силы по оси x и y
    :param rocket_obj: - экземпляр класса
    :param flag - флаг, определяющий включение основных двигателей
    :param flag_l - флаг, определяющий включение левых маневровых двигателей
    :param flag_r - флаг, определяющий включение правых маневровых двигателей
    :param sign - флаг, характеризующий наличие трения, True - если есть, False - если нет
    :return: f_k, f_y - силы, действующие на ракету
    """
    if sign:
        if rocket_obj.h <= 6440000:
            k = 0.000001 * (6490000-rocket_obj.h)/90000
        else:
            k = 0
    else:
        k = 0
    f_m = 0
    f_e_x = 0
    f_e_y = 0
    y_1, y_2, x_1, x_2 = rocket_obj.y_top, rocket_obj.y_bottom, rocket_obj.x_left, rocket_obj.x_right
    height = np.abs(y_1 - y_2)
    width = np.abs(x_1 - x_2)
    for module in rocket_obj.list:
        if rocket_obj.h >= 6400000:
            f_m -= module.m * G * M / rocket_obj.h ** 2 - module.m * rocket_obj.vx**2/rocket_obj.h
        else:
            f_m = 0
            rocket_obj.vy = 0
            rocket_obj.h = 6400000
    f_s_y = - rocket_obj.vy * np.abs(rocket_obj.vy) * (
            k * height * rocket_obj.angle + k * width * (180 - rocket_obj.angle))
    f_s_x = - rocket_obj.vx * np.abs(rocket_obj.vx) * (
            k * width * rocket_obj.angle + k * height * (180 - rocket_obj.angle))
    f_e_y, f_e_x = force_coord(flag, 'engine', rocket_obj, f_e_y, f_e_x)
    f_e_y, f_e_x = force_coord(flag_l, 'engine_l', rocket_obj, f_e_y, f_e_x)
    f_e_y, f_e_x = force_coord(flag_r, 'engine_r', rocket_obj, f_e_y, f_e_x)
    f_x = f_s_x + f_e_x
    f_y = f_s_y + f_m + f_e_y
    return f_x, f_y


def momentum_calc(rocket_obj, left_flag, right_flag, flag_forward, sign):
    """
        функция рассчета сил, действующих на ракету
        получает объект класса rocket, возвращает силы по оси x и y
        :param rocket_obj: - экземпляр класса
        :param left_flag - флаг, определяющий включение левых маневровых двигателей
        :param right_flag - флаг, определяющий включение правых маневровых двигателей
        :param flag_forward - флаг, определяющий включение основных двигателей
        :param sign - флаг, характеризующий наличие трения, True - если есть, False - если нет
        :return: mf - момент сил, действующих на ракету
        """
    if sign:
        if rocket_obj.h <= 6440000:
            k = 0.000001 * (6490000-rocket_obj.h)/90000
        else:
            k = 0
    else:
        k = 0
    mass = 0
    my = 0
    mx = 0
    for module in rocket_obj.list:
        mass += module.m
        my += module.m * (module.y + module.a/2)
        mx += module.m * (module.x + module.b/2)
    x_c = mx / mass
    mf = 0
    for module in rocket_obj.list:
        mf = moment_coord(left_flag, rocket_obj, module, 'engine_l', x_c, mf)
        mf = moment_coord(right_flag, rocket_obj, module, 'engine_r', x_c, mf)
        mf = moment_coord(flag_forward, rocket_obj, module, 'engine', x_c, mf)
    y_1, y_2, x_1, x_2 = rocket_obj.y_top, rocket_obj.y_bottom, rocket_obj.x_left, rocket_obj.x_right
    height = np.abs(y_1 - y_2)
    width = np.abs(x_1 - x_2)
    f_s_y = - rocket_obj.vy * np.abs(rocket_obj.vy) * (
            k * height * rocket_obj.angle + k * width * (180 - rocket_obj.angle))
    f_s_x = - rocket_obj.vx * np.abs(rocket_obj.vx) * (
            k * width * rocket_obj.angle + k * height * (180 - rocket_obj.angle))
    mf += f_s_y * (randint(-5, 5))
    mf -= -f_s_x * (randint(-5, 5))
    mf -= 10**6 * 0.0001 * rocket_obj.omega
    epsilon = mf/mass
    return epsilon


def rocket_move(rocket_obj, flag_left, flag_right, flag, sign):
    """
    функция, перемещающая ракету
    :param rocket_obj: экземпляр класса ракета
    :param flag_left: - флаг, характеризующий включение левых маневровых  двигателей
    :param flag_right: - флаг, характеризующий включение правых маневровых  двигателей
    :param flag:- флаг, характеризующий включение двигателей
    :param sign: - флаг, характеризующий наличие трения, True - если есть, False - если нет
    """
    mass = 0
    dt = 0.1
    rocket_obj.angle = rocket_obj.angle % 360
    for module in rocket_obj.list:
        mass += module.m
    f_x, f_y = force_calc(rocket_obj, flag, flag_left, flag_right, sign)
    a_x = f_x / mass
    a_y = f_y / mass
    rocket_obj.vx += a_x * dt
    rocket_obj.vy += a_y * dt
    rocket_obj.x += rocket_obj.vx * dt
    rocket_obj.h += rocket_obj.vy * dt
    epsilon = momentum_calc(rocket_obj, flag_left, flag_right, flag, sign)
    rocket_obj.omega += epsilon * dt
    rocket_obj.angle += rocket_obj.omega * dt

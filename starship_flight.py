import numpy as np
from starship_rocket import *
from random import *

g = 9.81
G = 6.67 * 10 ** (-11)
M = 6.02 * 10 ** 24


def fuel_calc(rocket):
    for module in rocket.list:
        rocket.fuel += module.fuel


def force_calc(rocket, flag):
    """
    функция рассчета сил, действующих на ракету
    получает объект класса rocket, возвращает силы по оси x и y
    :param rocket: - экземпляр класса
    :return: f_k, f_y - силы, действующие на ракету
    """
    if rocket.h <= 6440000:
        k = 0.01*(6490000-rocket.h)/90000
    else:
        k = 0
    f_m = 0
    f_s_x = 0
    f_s_y = 0
    f_e_x = 0
    f_e_y = 0
    y_bottom, y_top, x_left, x_right = find_max_coord(rocket.list)
    height = np.abs(y_bottom - y_top)
    width = np.abs(x_left - x_right)
    for module in rocket.list:
        if rocket.h >= 6400000:
            f_m -= module.m * G * M / rocket.h ** 2 - module.m * rocket.vx**2/rocket.h
        else:
            f_m = 0
            rocket.vy = 0
            rocket.h = 6400000
    f_s_y = - rocket.vy * (k * height * rocket.angle + k * width * (180 - rocket.angle))
    f_s_x = - rocket.vx * (k * width * rocket.angle + k * height * (180 - rocket.angle))
    if flag:
        for module in rocket.list:
            if module.type == 'engine' and rocket.fuel >= 0:
                f_e_y += module.force * np.cos(rocket.angle*np.pi/180) * 1000
                f_e_x += module.force * np.sin(rocket.angle*np.pi/180) * 1000
                rocket.fuel -= module.force * 0.0005
    else:
        f_e_y = 0
        f_e_x = 0
    f_x = f_s_x + f_e_x
    f_y = f_s_y + f_m + f_e_y
    return f_x, f_y


def momentum_calc(rocket, left_flag, right_flag, flag_forward):
    m = 0
    my = 0
    mx = 0
    for module in rocket.list:
        m += module.m
        my += module.m * module.y
        mx += module.m * module.x
    y_c = my / m
    x_c = mx / m
    mf = 0
    for module in rocket.list:
        if left_flag and rocket.fuel >= 0:
            if module.type == 'engine_l':
                rocket.fuel -= module.force * 0.001
                mf += module.force * (module.x - x_c)
        if right_flag and rocket.fuel >= 0:
            if module.type == 'engine_r':
                rocket.fuel -= module.force * 0.001
                mf += module.force * (module.x - x_c)
        if flag_forward and rocket.fuel >= 0:
            if module.type == 'engine':
                rocket.fuel -= module.force * 0.001
                mf += module.force * (module.x - x_c)
    mf += randint(0, 1)
    epsilon = mf/m
    return epsilon


def rocket_move(rocket, flag_left, flag_right, flag):
    m = 0
    dt = 1 / 30
    for module in rocket.list:
        m += module.m
    f_x, f_y = force_calc(rocket, flag)
    a_x = f_x / m
    a_y = f_y / m
    rocket.vx += a_x * dt
    rocket.vy += a_y * dt
    rocket.x += rocket.vx * dt
    rocket.h += rocket.vy * dt
    epsilon = momentum_calc(rocket, flag_left, flag_right, flag)
    rocket.omega += epsilon * dt
    rocket.angle += rocket.omega * dt
    print(np.sqrt(rocket.vx**2+rocket.vy**2), rocket.vx, rocket.vy)

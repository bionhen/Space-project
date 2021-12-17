import numpy as np
from starship_rocket import *
from random import *

g = 9.81
G = 6.67 * 10 ** (-11)
M = 6.02 * 10 ** 24


def fuel_calc(rocket):
    for module in rocket.list:
        rocket.fuel += module.fuel


def force_coord(flag, engine_type, rocket, f_e_y, f_e_x):
    if flag:
        for module in rocket.list:
            if rocket.fuel >= 0 and module.type == engine_type:
                f_e_y += module.force * np.cos(rocket.angle*np.pi/180) * 100
                f_e_x += module.force * np.sin(rocket.angle*np.pi/180) * 100
                rocket.fuel -= module.force * 0.0005
    return f_e_y, f_e_x


def moment_coord(flag, rocket, module, module_type, x_c, mf):
    if flag and rocket.fuel >= 0:
        if module.type == module_type:
            rocket.fuel -= module.force * 0.001
            mf += module.force * (module.x + module.b / 2 - x_c)
    return mf


def force_calc(rocket, flag, flag_l, flag_r, sign):
    """
    функция рассчета сил, действующих на ракету
    получает объект класса rocket, возвращает силы по оси x и y
    :param rocket: - экземпляр класса
    :return: f_k, f_y - силы, действующие на ракету
    """
    if sign:
        if rocket.h <= 6440000:
            k = 0.000001 * (6490000-rocket.h)/90000
        else:
            k = 0
    else:
        k = 0
    f_m = 0
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
    f_s_y = - rocket.vy * np.abs(rocket.vy) * (k * height * rocket.angle + k * width * (180 - rocket.angle))
    f_s_x = - rocket.vx * np.abs(rocket.vx) * (k * width * rocket.angle + k * height * (180 - rocket.angle))
    f_e_y, f_e_x = force_coord(flag, 'engine', rocket, f_e_y, f_e_x)
    f_e_y, f_e_x = force_coord(flag_l, 'engine_l', rocket, f_e_y, f_e_x)
    f_e_y, f_e_x = force_coord(flag_r, 'engine_r', rocket, f_e_y, f_e_x)
    f_x = f_s_x + f_e_x
    f_y = f_s_y + f_m + f_e_y
    return f_x, f_y


def momentum_calc(rocket, left_flag, right_flag, flag_forward):
    if rocket.h <= 6440000:
        k = 0.000001 * (6490000-rocket.h)/90000
    else:
        k = 0
    m = 0
    my = 0
    mx = 0
    for module in rocket.list:
        m += module.m
        my += module.m * (module.y + module.a/2)
        mx += module.m * (module.x + module.b/2)
    y_c = my / m
    x_c = mx / m
    mf = 0
    for module in rocket.list:
        mf = moment_coord(left_flag, rocket, module, 'engine_l', x_c, mf)
        mf = moment_coord(right_flag, rocket, module, 'engine_r', x_c, mf)
        mf = moment_coord(flag_forward, rocket, module, 'engine', x_c, mf)
    y_bottom, y_top, x_left, x_right = find_max_coord(rocket.list)
    height = np.abs(y_bottom - y_top)
    width = np.abs(x_left - x_right)
    f_s_y = - rocket.vy * np.abs(rocket.vy) * (k * height * rocket.angle + k * width * (180 - rocket.angle))
    f_s_x = - rocket.vx * np.abs(rocket.vx) * (k * width * rocket.angle + k * height * (180 - rocket.angle))
    mf += f_s_y * (randint(-10, 10))
    mf -= -f_s_x * (randint(-10, 10))
    print(10**10 * k * rocket.omega)
    print('mf', rocket.omega, 10**5 * k * rocket.omega)
    mf -= 10**6 * k * rocket.omega**3
    epsilon = mf/m
    return epsilon


def rocket_move(rocket, flag_left, flag_right, flag, sign):
    m = 0
    dt = 0.1
    rocket.angle = rocket.angle % 360
    print(rocket.angle)
    for module in rocket.list:
        m += module.m
    f_x, f_y = force_calc(rocket, flag, flag_left, flag_right, sign)
    a_x = f_x / m
    a_y = f_y / m
    rocket.vx += a_x * dt
    rocket.vy += a_y * dt
    rocket.x += rocket.vx * dt
    rocket.h += rocket.vy * dt
    epsilon = momentum_calc(rocket, flag_left, flag_right, flag)
    rocket.omega += epsilon * dt
    rocket.angle += rocket.omega * dt


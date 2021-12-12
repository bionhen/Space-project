import numpy as np

g = 9.81
G = 6.67 * 10 ** (-11)
M = 6.02 * 10 ** (-24)


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
    f_m = 0
    f_s_x = 0
    f_s_y = 0
    f_e_x = 0
    f_e_y = 0
    for module in rocket.list:
        f_m += module.m * G * M / rocket.h ** 2
    f_s_y += -rocket.vy * (rocket.angle / 180 + 0.1)
    f_s_x += -rocket.vx * ((180 - rocket.angle) / 180 + 0.1)
    if flag:
        for module in rocket.list:
            if module.type == 'engine' and rocket.fuel >= 0:
                f_e_y += module.force * np.cos(rocket.angle)
                f_e_x += module.force * np.sin(rocket.angle)
                rocket.fuel -= module.force * 0.005
    f_x = f_s_x + f_e_x
    f_y = f_s_y + f_m + f_e_x
    return f_x, f_y


def momentum_calc(rocket, left_flag, right_flag):
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
        if right_flag and rocket.fuel >= 0:
            if module.type == 'engine_r':
                rocket.fuel -= module.force * 0.001
        mf += module.force * (module.x-x_c)
    epsilon = mf/m
    return epsilon


def rocket_move(rocket, flag_left, flag_right, flag):
    m = 0
    dt = 0.01
    for module in rocket.list:
        m += module.m
    f_x, f_y = force_calc(rocket, flag)
    a_x = f_x / m
    a_y = f_y / m
    rocket.vx += a_x * dt
    rocket.vy += a_y * dt
    rocket.x += rocket.vx * dt
    rocket.h += rocket.vy * dt
    epsilon = momentum_calc(rocket, flag_left, flag_right)
    rocket.omega += epsilon * dt
    rocket.angle += rocket.angle * dt

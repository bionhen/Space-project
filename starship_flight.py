import numpy as np

g = 9.81
G = 6.67 * 10 ** (-11)
M = 6.02 * 10 ** (-24)


def force_calc(rocket):
    f_m = 0
    f_s_x = 0
    f_s_y = 0
    f_e_x = 0
    f_e_y = 0
    f_x = 0
    f_y = 0
    for module in rocket.list:
        f_m += module.m * G * M / rocket.h ** 2
    f_s_y += -rocket.vy * (rocket.angle / 180 + 0, 1)
    f_s_x += -rocket.vx * ((180 - rocket.angle) / 180 + 0, 1)
    for module in rocket.list:
        f_e_y += module.force * np.cos(rocket.angle)
        f_e_x += module.force * np.sin(rocket.angle)
    f_x = f_s_x + f_e_x
    f_y = f_s_y + f_m + f_e_x
    return f_x, f_y


def momentum_calc(rocket, left_flag, right_flag):
    m = 0
    my = 0
    mx = 0
    for module in rocket.list:
        m += module.m
        my = module.m * module.y
        mx = module.m * module.x
    y_c = my / m
    x_c = mx / m
    mf = 0
    for module in rocket.list:
        if left_flag:
            if module.type == 'left_manevour_engine':
                module.force = 10
        for module in rocket.list:
            if right_flag:
                if module.type == 'right_manevour_engine':
                    module.force = 10
        mf += module.force * (module.x-x_c)
    epsilon = mf/m
    return epsilon


def rocket_move(rocket, flag_left, flag_right):
    m = 0
    dt = 0.01
    for module in rocket.list:
        m += module.m
    f_x, f_y = force_calc(rocket)
    a_x = f_x / m
    a_y = f_y / m
    rocket.vx += a_x * dt
    rocket.vy += a_y * dt
    rocket.x += rocket.vx * dt
    rocket.y += rocket.vy * dt
    epsilon = momentum_calc(rocket, flag_left, flag_right)
    rocket.omega += epsilon * dt
    rocket.angle += rocket.angle * dt
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


def momentum_calc(rocket, flag_left, flag_right):
    m = 0
    for module in rocket.list:
        m += module.m
    mf = 0
    if flag_left:
        mf = rocket.manevour_force
    if flag_right:
        mf = rocket.manevour_force
    e = mf/m
    return e


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
    e = momentum_calc(rocket, flag_left, flag_right)
    rocket.o += e * dt
    rocket.angle += rocket.angle * dt
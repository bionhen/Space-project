import numpy as np
from space_obj import Object

G = 6.67408E-11
"""Гравитационная постоянная"""


def calculate_m_rocket(rocket):
    """
    функция, рассчитывающая массу ракеты
    :param rocket: - экземпляр класса Rocket
    :return: m - масса ракеты
    """
    m = 0
    for module in rocket.list:
        m += module.m
    return m


def calculate_m_fuel(rocket):
    """
    функция, рассчитывающая топливо ракеты
    :param rocket: - экземпляр класса Rocket
    :return: fuel - топливо ракеты
    """
    fuel = 0
    for module in rocket.list:
        fuel += module.fuel
    return fuel


def calculate_force(body, space_objects, flag, flag_l, flag_r):
    """
    функция, рассчитывающая силу и момент сил, действующих на тело
    :param body: тело, для которого рассчитывется сила
    :param space_objects: список тел, которые взаимодействуют с телом
    :param flag - флаг, определяющий включение основных двигателей
    :param flag_l - флаг, определяющий включение левых маневровых двигателей
    :param flag_r - флаг, определяющий включение правых маневровых двигателей
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if obj.type == 'rocket':
            obj.m = calculate_m_rocket(obj)
        if body == obj:
            continue
        r = ((body.x - obj.x) ** 2 + (body.y - obj.y) ** 2) ** 0.5
        body.Fx += G * obj.m * body.m * (obj.x - body.x) / (r ** 3)
        body.Fy += G * obj.m * body.m * (obj.y - body.y) / (r ** 3)
        if body.type == 'rocket':
            for module in body.list:
                if module.type == 'engine' and flag and body.fuel >= 0:
                    body.Fx += module.force * np.cos(body.angle * np.pi / 180)
                    body.Fy += module.force * np.sin(body.angle * np.pi / 180)
                    body.fuel -= module.force * 0.001
            my = 0
            mx = 0
            for module in body.list:
                my += module.m * (module.y + module.a / 2)
                mx += module.m * (module.x + module.b / 2)
            x_c = mx / body.m
            mf = 0
            for module in body.list:
                if flag_l and body.fuel >= 0:
                    if module.type == 'engine_l':
                        body.fuel -= module.force * 0.001
                        mf += 10 ** (-7) * module.force * (module.x + module.b / 2 - x_c)
                if flag_r and body.fuel >= 0:
                    if module.type == 'engine_r':
                        body.fuel -= module.force * 0.001
                        mf += 10 ** (-7) * module.force * (module.x + module.b / 2 - x_c)
                if flag and body.fuel >= 0:
                    if module.type == 'engine':
                        body.fuel -= module.force * 0.001
                        mf += 10 ** (-7) * module.force * (module.x + module.b / 2 - x_c)
            body.epsilon = mf / body.m


def move_space_object(body, dt):
    """
    функция, перемещающая космическое тело
    :param body: - перемещаемое тело
    :param dt: - маленький промежуток времени
    """
    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.Vx += ax * dt
    body.Vy += ay * dt
    body.x += body.Vx * dt
    body.y += body.Vy * dt
    body.angle += body.omega * dt
    body.omega += body.epsilon * dt


def recalculate_space_objects_positions(space_objects, dt, flag, flag_l, flag_r):
    """
    функция, пересчитывающая координаты тел
    :param space_objects: - список космических объектов
    :param dt: промежуток времени
    :param flag - флаг, определяющий включение основных двигателей
    :param flag_l - флаг, определяющий включение левых маневровых двигателей
    :param flag_r - флаг, определяющий включение правых маневровых двигателей
    """

    for body in space_objects:
        calculate_force(body, space_objects, flag, flag_l, flag_r)
    for body in space_objects:
        move_space_object(body, dt)


def calculation_orbit(body, object_list, dt):
    """
    функция, рассчитывающая список координат предполагаемой орбиты
    :param body: - тело для которого рассчитываается орбита
    :param object_list: - список объектов, взаимодействующих с телом
    :param dt: - промежуток времени
    :return: calc_list - список координат для предполагаемой орбиты
    """
    calc_list = []
    body_test = Object()
    body_test.type = 'rocket'
    body_test.x = body.x
    body_test.y = body.y
    body_test.Vx = body.Vx
    body_test.Vy = body.Vy
    body_test.m = body.m
    for t in range(10 * dt):
        body_test.Fx = body_test.Fy = 0
        for obj in object_list:
            if obj == body:
                continue
            r = ((body_test.x - obj.x) ** 2 + (body_test.y - obj.y) ** 2) ** 0.5
            body_test.Fx += G * obj.m * body_test.m * (obj.x - body_test.x) / (r ** 3)
            body_test.Fy += G * obj.m * body_test.m * (obj.y - body_test.y) / (r ** 3)
        ax = body_test.Fx / body_test.m
        ay = body_test.Fy / body_test.m
        body_test.Vx += ax * dt
        body_test.Vy += ay * dt
        body_test.x += body_test.Vx * dt
        body_test.y += body_test.Vy * dt
        calc_list.append([body_test.x/10**6, body_test.y/10**6])
        t += dt
    return calc_list

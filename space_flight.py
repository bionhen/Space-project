import numpy as np

G = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""


def calculate_m_rocket(rocket):
    m = 0
    for module in rocket.list:
        m += module.m
    return m


def calculate_m_fuel(rocket):
    fuel = 0
    for module in rocket.list:
        fuel += module.fuel
    return fuel


def calculate_force(body, space_objects, flag, flag_l, flag_r):
    """Вычисляет силу, действующую на тело.
    Параметры:
    **body** — тело, для которого нужно вычислить дейстующую силу.
    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if obj.type == 'rocket':
            obj.m = calculate_m_rocket(obj)
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        body.Fx += G*obj.m*body.m*(obj.x - body.x)/(r**3)
        body.Fy += G*obj.m*body.m*(obj.y - body.y)/(r**3)
        if body.type == 'rocket':
            for module in body.list:
                if module.type == 'engine' and flag and body.fuel >= 0:
                    body.Fx += module.force * np.cos(body.angle*np.pi/180)
                    body.Fy += module.force * np.sin(body.angle*np.pi/180)
                    body.fuel -= module.force * 0.001
                if module.type == 'engine_l' and flag_l and body.fuel >= 0:
                    body.Fx += module.force * np.cos(body.angle*np.pi/180)
                    body.Fy += module.force * np.sin(body.angle*np.pi/180)
                    body.fuel -= module.force * 0.001
                if module.type == 'engine_r' and flag_r and body.fuel >= 0:
                    body.Fx += module.force * np.cos(body.angle*np.pi/180)
                    body.Fy += module.force * np.sin(body.angle*np.pi/180)
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
                        mf += 10**(-6)*module.force * (module.x + module.b / 2 - x_c)
                if flag_r and body.fuel >= 0:
                    if module.type == 'engine_r':
                        body.fuel -= module.force * 0.001
                        mf += 10**(-6)*module.force * (module.x + module.b / 2 - x_c)
                if flag and body.fuel >= 0:
                    if module.type == 'engine':
                        body.fuel -= module.force * 0.001
                        mf += 10**(-6)*module.force * (module.x + module.b / 2 - x_c)
            body.epsilon = mf/body.m


def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.
    Параметры:
    **body** — тело, которое нужно переместить.
    """

    ax = body.Fx / body.m
    ay = body.Fy / body.m
    body.Vx += ax*dt
    body.Vy += ay*dt
    body.x += body.Vx*dt
    body.y += body.Vy*dt
    body.angle += body.omega*dt
    body.omega += body.epsilon*dt


def recalculate_space_objects_positions(space_objects, dt, flag, flag_l, flag_r):
    """Пересчитывает координаты объектов.
    Параметры:
    **space_objects** — список объектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects, flag, flag_l, flag_r)
    for body in space_objects:
        move_space_object(body, dt)

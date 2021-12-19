from draw_functions.starship_modules import *


class Rocket:
    """
    класс ракеты
    surface - поверхность ракеты
    list - список элементов ракеты
    h - расстояние до цента Земли в км
    angle - угол поворота ракеты
    vx, vy - скорости по осям x и y
    omega -  угловая скорость
    """
    def __init__(self):
        self.surface = pygame.Surface((400, 500), pygame.SRCALPHA)
        self.list = []
        self.h = 6400000
        self.x = 0
        self.angle = 0
        self.vx = 0
        self.vy = 0
        self.omega = 0
        self.fuel = 0
        self.fuel_max = 0
        self.mass = 0
        self.x_left = 0
        self.x_right = 0
        self.y_top = 0
        self.y_bottom = 0
        self.x_center_mass = 0
        self.y_center_mass = 0
        self.surface_width = 0
        self.surface_height = 0
        self.engines_cord = []
        self.left_engines_cord = []
        self.right_engines_cord = []

    def find_max_coord(self):
        """Функция находит наиболее близкий элемент к земле."""
        rocket_modules_y_bottom = []
        rocket_modules_y_top = []
        rocket_modules_x_left = []
        rocket_modules_x_right = []
        for rocket_module in self.list:
            rocket_modules_y_bottom.append(rocket_module.y + rocket_module.a)
            rocket_modules_y_top.append(rocket_module.y)
            rocket_modules_x_left.append(rocket_module.x)
            rocket_modules_x_right.append(rocket_module.x + rocket_module.b)
        if rocket_modules_y_top != [] and rocket_modules_y_bottom != []:
            self.y_bottom = max(rocket_modules_y_bottom)
            self.y_top = min(rocket_modules_y_top)

        if rocket_modules_x_left != [] and rocket_modules_x_right != []:
            self.x_left = min(rocket_modules_x_left)
            self.x_right = max(rocket_modules_x_right)

        if self.x_left == self.x_right:
            self.x_left = 0

        if self.y_top == self.y_bottom:
            self.y_top = 0

    def change_cords(self):
        self.x = self.x - 200
        self.y = self.y - 50

    def find_rocket_width_and_height(self):
        self.surface_width = self.x_right - self.x_left
        self.surface_height = self.y_bottom - self.y_top + 50

    def render_rocket_surface(self):
        print(self.surface)
        self.surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        print(self.surface)
        print(self.surface_width)
        for rocket_module in self.list:
            rocket_module.x = rocket_module.x - self.x_left
            rocket_module.y = rocket_module.y - self.y_top
            self.surface.blit(rocket_module.surface, (rocket_module.x, rocket_module.y))

    def find_center_mass(self):
        m = 0
        mx = 0
        my = 0
        for module in self.list:
            m += module.m
            my += module.m * (module.y + module.a / 2)
            mx += module.m * (module.x + module.b / 2)
        if m == 0:
            m = 100
        self.y_center_mass = my / m
        self.x_center_mass = mx / m

    def find_engines(self):
        for rocket_module in self.list:
            if rocket_module.type == 'engine':
                self.engines_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
            if rocket_module.type == 'engine_l':
                self.left_engines_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
            if rocket_module.type == 'engine_r':
                self.right_engines_cord.append([rocket_module.x, rocket_module.y, rocket_module.a])
from draw_functions.constants import *
pygame.init()


class Button:
    """Класс Button (Кнопка, на которую наведен курсор)"""
    def __init__(self, filename, x, y):
        """
        Инициализация класса Button
        :param filename - путь к файлу с изображением кнопки
        :param x - координата левого верхнего угла по горизонтали
        :param y - координата левого верхнего угла по вертикали
        """
        self.x = x
        self.y = y
        self.button_surf = pygame.image.load(("images/"+filename+".png")).convert_alpha()


class ButtonOff(Button):
    """
    Инициализация класса ButtonOff, дочерний класс  (Кнопка, на которую не наведён курсор)
    :param filename - имя файла с изображением кнопки
    :param x - координата левого верхнего угла по горизонтали
    :param y - координата левого верхнего угла по вертикали
    """
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.button_off_surf_width = pygame.Surface.get_width(self.button_surf)
        self.button_off_surf_height = pygame.Surface.get_height(self.button_surf)

    def check_button(self, cur_event):
        """Метод проверяет, наведён ли курсор на кнопку"""
        if ((cur_event[0] >= self.x)
                and (cur_event[0] <= self.x + self.button_off_surf_width)
                and (cur_event[1] >= self.y)
                and (cur_event[1] <= self.y + self.button_off_surf_height)):
            button_checked = True
        else:
            button_checked = False
        return button_checked


def load_image(i, x, y):
    """
    эта функция загружает в переменную картинку в нужном масштабе
    :param i: полный путь к изображению
    :param x: масштаб по вертикальной оси
    :param y: масштаб по горизонтальной оси
    :return: изображение в требуемом масштабе
    """
    menu_bg_surf = pygame.image.load(i).convert()
    menu_bg_surf = pygame.transform.scale(menu_bg_surf, (x, y))
    return menu_bg_surf


def draw_menu_foo():
    """
    Эта функция отрисовывает экран главного меню в зависимости от того, наведен ли курсор мыши нв кнопку
    """
    a = load_image("images/menu/space_bg_4.jpg", 800, 600)
    b = ButtonOff('menu/Кнопка Missions 2', 300, 400)
    c = Button('menu/Кнопка Missions нажатая 1', 300, 400)

    a.blit(b.button_surf, (b.x, b.y))

    if b.check_button(pygame.mouse.get_pos()):
        a.blit(c.button_surf, (c.x, c.y))

    sc.blit(a, (0, 0))

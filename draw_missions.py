import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60


class Button:
    def __init__(self, filename, x, y):
        self.x = x
        self.y = y
        self.button_surf = pygame.image.load(("images/missions/"+filename+".png")).convert_alpha()


class ButtonOff(Button):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)
        self.button_off_surf_width = pygame.Surface.get_width(self.button_surf)
        self.button_off_surf_height = pygame.Surface.get_height(self.button_surf)

    def check_button(self, cur_event):
        if ((cur_event[0] >= self.x)
                and (cur_event[0] <= self.x + self.button_off_surf_width)
                and (cur_event[1] >= self.y)
                and (cur_event[1] <= self.y + self.button_off_surf_height)):
            button_checked = True
        else:
            button_checked = False
        return button_checked

"""def set_missinons_buttons():
    orbit = Button('entering orbit on', 100, 150)
    orbit_off = ButtonOff('entering orbit', 100, 150)
    moon = Button('flight to the moon on', 100, 250)
    moon_off = ButtonOff('flight to the moon', 100, 250)

    buttons_off = [orbit_off, moon_off]
    buttons_on = [orbit, moon]"""

bg_missions_surf = pygame.image.load(("images/missions/missions_bg.png")).convert_alpha()
bg_missions_surf = pygame.transform.scale(bg_missions_surf, (WIDTH, HEIGHT))

orbit = Button('entering orbit on', 100, 150)
orbit_off = ButtonOff('entering orbit', 100, 150)
moon = Button('flight to the moon on', 100, 250)
moon_off = ButtonOff('flight to the moon', 100, 250)

buttons_off = [orbit_off, moon_off]
buttons_on = [orbit, moon]


while True:
    sc.blit(bg_missions_surf, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    for i in range(len(buttons_off)):
        bg_missions_surf.blit(buttons_off[i].button_surf, (buttons_off[i].x, buttons_on[i].y))
        if buttons_off[i].check_button(pygame.mouse.get_pos()):
            bg_missions_surf.blit(buttons_on[i].button_surf, (buttons_on[i].x, buttons_on[i].y))

    pygame.display.update()

    clock.tick(FPS)

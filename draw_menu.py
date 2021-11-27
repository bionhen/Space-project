import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)

bg_surf = pygame.image.load(("images/menu/space_bg_4.jpg")).convert()
bg_surf = pygame.transform.scale(bg_surf, (WIDTH, HEIGHT))


missions_button_off_surf = pygame.image.load(("images/menu/Кнопка Missions 2.png")).convert_alpha()
missions_button_off_surf_width = pygame.Surface.get_width(missions_button_off_surf)
missions_button_off_surf_height = pygame.Surface.get_height(missions_button_off_surf)

missions_button_on_surf = pygame.image.load(("images/menu/Кнопка Missions нажатая 1.png")).convert_alpha()


def check_button(cur_event):
    if ((cur_event[0] >= 300)
            and (cur_event[0] <= 300 + missions_button_off_surf_width)
            and (cur_event[1] >= 350)
            and (cur_event[1] <= 350 + missions_button_off_surf_height)):
        button_checked = True
    else:
        button_checked = False
    return button_checked


while True:
    sc.blit(bg_surf, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(missions_button_off_surf, (300, 350))
    if check_button(pygame.mouse.get_pos()):
        sc.blit(bg_surf, (0, 0))
        sc.blit(missions_button_on_surf, (300, 350))

    pygame.display.update()

    clock.tick(FPS)


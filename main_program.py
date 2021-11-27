import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dolgoprudniy Program")
pygame.display.set_icon(pygame.image.load("emblem.ico"))

clock = pygame.time.Clock()
FPS = 60



while True:
    # FIXME вставить отображение фона

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    # FIXME вставить кнопку ненаведённую
    # FIXME вставить кнупку наведённую

    pygame.display.update()

    clock.tick(FPS)


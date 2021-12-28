import pygame
import sys
from settings import *
from level1 import Level1

pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
level = Level1(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        screen.fill('black')
        level.run()
        pygame.display.update()
        clock.tick(60)













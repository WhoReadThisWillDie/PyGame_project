import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)
        self.axis = pygame.math.Vector2(0, 0)
        self.speed = 5
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.axis.x = 1
        elif keys[pygame.K_LEFT]:
            self.axis.x = -1
        else:
            self.axis.x = 0

    def update(self):
        self.get_input()
        self.rect.x += self.axis.x * self.speed

import pygame
import sys, os

pygame.init()
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
tile_size = 50

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
tiles_sprite = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    global level_map
    filename = "levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '1':
                Tile('dirt', x, y)
            elif level[y][x] == '2':
                Tile('grass', x, y)
            elif level[y][x] == 'p':
                new_player = Player(x, y)
            elif level[y][x] == '3':
                Tile('sign', x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(tiles_sprite, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite, all_sprites)
        self.image = load_image('player.png', -1)
        # self.image = pygame.image.load('data/player2.png').convert()
        # self.image.set_colorkey(-1)
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 15)
        self.axis = pygame.math.Vector2(0, 0)
        self.speed = 5

    # def get_input(self):
    #     keys = pygame.key.get_pressed()
    #
    #     if keys[pygame.K_RIGHT]:
    #         self.axis.x = 1
    #     elif keys[pygame.K_LEFT]:
    #         self.axis.x = -1
    #     else:
    #         self.axis.x = 0
    #
    # def update(self):
    #     self.get_input()
    #     self.rect.x += self.axis.x * self.speed

    def update(self):
        if not pygame.sprite.spritecollideany(self, tiles_sprite):
            self.rect = self.rect.move(0, 5)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect = self.rect.move(5, 0)
        elif keys[pygame.K_LEFT]:
            self.rect = self.rect.move(-5, 0)
        elif keys[pygame.K_UP]:
            self.rect = self.rect.move(0, -10)


background = pygame.transform.scale(load_image('background.png'), (width, height))
tile_images = {'dirt': load_image('dirt.png'), 'grass': load_image('grass.png'), 'sign': load_image('sign.png', -1)}
player, lvl_x, lvl_y = generate_level(load_level('level_1.txt'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(pygame.Color('black'))
    player_sprite.update()
    screen.blit(background, (0, 0))
    tiles_sprite.draw(screen)
    player_sprite.draw(screen)
    pygame.display.update()
    clock.tick(60)

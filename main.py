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


# tile_size = 64
# screen_width = 1200
# screen_height = len(level_map) * tile_size


# class Level:
#     def __init__(self, level_data, surface):
#         self.display_surface = surface
#         self.setup_level(level_data)
#         self.world_shift = 0
#         self.tile_size = 64
#
#     def setup_level(self, layout):
#         self.tiles = pygame.sprite.Group()
#         self.player = pygame.sprite.GroupSingle()
#         for row_i, row in enumerate(layout):
#             for col_i, col in enumerate(row):
#                 #print(f'{row_i},{col_i}:{col}')
#                 x, y = col_i * self.tile_size, row_i * self.tile_size
#
#                 if col == '1':
#                     tile = Tile((x, y), self.tile_size)
#                     self.tiles.add(tile)
#
#                 if col == 'p':  # p это player
#                     player_sprite = Player((x, y))
#                     self.player.add(player_sprite)
#
#     def run(self):
#         self.tiles.update(self.world_shift)
#         self.tiles.draw(self.display_surface)
#         self.player.draw(self.display_surface)
#         self.player.update()


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
            print(y, x)
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
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill('red')
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y + 5)
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
        self.rect = self.rect.move(self.axis.x * self.speed, self.axis.y * self.speed)


# class Tile(pygame.sprite.Sprite):
#     def __init__(self, pos, size):
#         super().__init__()
#         self.image = pygame.Surface((size, size))
#         self.image.fill('white')    # цвет преград выберем сёдня
#         self.rect = self.image.get_rect(topleft=pos)
#
#     def update(self, x_shift):
#         self.rect.x += x_shift


# level = Level(level_map, screen)
background = pygame.transform.scale(load_image('background.png'), (width, height))
tile_images = {'dirt': load_image('dirt.png'), 'grass': load_image('grass.png'), 'sign': load_image('sign.png', -1)}
player, lvl_x, lvl_y = generate_level(load_level('level_1.txt'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(pygame.Color('black'))
    screen.blit(background, (0, 0))
    tiles_sprite.draw(screen)
    player_sprite.draw(screen)
    pygame.display.update()
    clock.tick(60)



import pygame
import sys, os
pygame.init()
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
tile_size = 50

score = 0

hero_width = 50
hero_height = 66

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
tiles_sprite = pygame.sprite.Group()
coins_sprite = pygame.sprite.Group()


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
            elif level[y][x] == '4':
                Coin(x, y)
    return new_player, x, y


def update_score(score, x, y):
    font = pygame.font.Font(None, 50)
    img = load_image('coin.png', -1)
    img = pygame.transform.scale(img, (50, 50))
    count = font.render(score, True, pygame.Color('black'))
    screen.blit(img, (x, y))
    screen.blit(count, (x + 50, y + 8))


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(tiles_sprite, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_sprite, all_sprites)
        self.image = load_image('coin.png', -1)
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite, all_sprites)
        Player.image_right = load_image('player.png', -1)
        Player.image_left = pygame.transform.flip(Player.image_right, True, False)
        self.image = Player.image_right
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 50)
        self.axis = pygame.math.Vector2(0, 0)
        self.can_jump = False
        self.on_ground = True

    def update(self):
        global score
        keys = pygame.key.get_pressed()
        self.axis.x = 0
        y_speed = 0
        if keys[pygame.K_LEFT]:
            self.axis.x = -5
            self.image = Player.image_left
        if keys[pygame.K_RIGHT]:
            self.axis.x = 5
            self.image = Player.image_right
        if keys[pygame.K_UP] and self.can_jump and self.on_ground:
            self.axis.y = -20
            self.on_ground = False
        if not keys[pygame.K_UP]:
            self.on_ground = True

        self.axis.y += 1
        if self.axis.y > 15:
            self.axis.y = 15
        y_speed += self.axis.y

        self.can_jump = False
        for sprite in tiles_sprite:
            if sprite.rect.colliderect(self.rect.x + self.axis.x, self.rect.y, hero_width, hero_height):
                self.axis.x = 0
            if sprite.rect.colliderect(self.rect.x, self.rect.y + y_speed, hero_width, hero_height):
                if self.axis.y < 0:
                    y_speed = sprite.rect.bottom - self.rect.top
                    self.axis.y = 0
                elif self.axis.y >= 0:
                    y_speed = sprite.rect.top - self.rect.bottom
                    self.can_jump = True
                    self.axis.y = 0

        if pygame.sprite.spritecollide(self, coins_sprite, True):
            score += 1

        self.rect.x += self.axis.x
        self.rect.y += y_speed


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
    coins_sprite.draw(screen)
    player_sprite.draw(screen)
    update_score(str(score), 5, 5)
    pygame.display.update()
    clock.tick(60)

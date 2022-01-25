import pygame, sqlite3
import sys, os

pygame.init()
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
ticks = pygame.time.get_ticks()
timeLastCheck = 0.0
tile_size = 50

hero_width = 50
hero_height = 66

enemyWidth = 40
enemyHeight = 40

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
tiles_sprite = pygame.sprite.Group()


level1Test = False
level2Test = False
level3Test = False


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
            elif level[y][x] == 'e':
                Tile("enemy", x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(tiles_sprite, all_sprites)
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(tile_size * pos_x, tile_size * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_sprite, all_sprites)
        Player.image_right = load_image('player.png', -1)
        Player.image_left = pygame.transform.flip(Player.image_right, True, False)
        self.image = Player.image_right
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 15)
        self.axis = pygame.math.Vector2(0, 0)
        self.can_jump = True


    def update(self):
        global player, lvl_x, lvl_y
        global level1Test, level2Test, level3Test
        global tiles_sprite, player_sprite, ticks, timeLastCheck
        keys = pygame.key.get_pressed()
        self.axis.x = 0
        y_speed = 0
        reserv = 0
        time = (pygame.time.get_ticks() - ticks) / 1000
        if keys[pygame.K_LEFT]:
            self.axis.x = -5
            self.image = Player.image_left
        if keys[pygame.K_RIGHT]:
            self.axis.x = 5
            self.image = Player.image_right
        if keys[pygame.K_UP] and self.can_jump:
            self.axis.y = -20
            self.can_jump = False
        if not keys[pygame.K_UP]:
            self.can_jump = True
        if keys[pygame.K_r]:
            ticks = pygame.time.get_ticks()
            reserv = timeLastCheck
            if level2Test:
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                tiles_sprite.empty()
                player, lvl_x, lvl_y = generate_level(load_level('level_3.txt'))
                tiles_sprite.draw(screen)
            elif level1Test:
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                tiles_sprite.empty()
                player, lvl_x, lvl_y = generate_level(load_level('level_2.txt'))
                tiles_sprite.draw(screen)
            else:
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                tiles_sprite.empty()
                player, lvl_x, lvl_y = generate_level(load_level('level_1.txt'))
                tiles_sprite.draw(screen)
        if level2Test:
            con = sqlite3.connect("database.sql")
            cur = con.cursor()
            cur.execute("""insert ?, ? into records""", ("not ready", 0))
            con.commit()
            con.close()

        self.axis.y += 1
        if self.axis.y > 10:
            self.axis.y = 10
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

            if self.rect.x == 1000 and self.rect.y == 84 and level1Test is False:
                timeLastCheck = time
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                level1Test = True
                tiles_sprite.empty()
                player, lvl_x, lvl_y = generate_level(load_level('level_2.txt'))
                tiles_sprite.draw(screen)

            if self.rect.x == 1100 and self.rect.y == 634 and level2Test is False:
                timeLastCheck = time
                level2Test = True
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                player_sprite.update()
                tiles_sprite.empty()
                player, lvl_x, lvl_y = generate_level(load_level('level_3.txt'))
                tiles_sprite.draw(screen)
        time = ((pygame.time.get_ticks() - ticks) / 1000) + reserv
        print(self.rect.x, self.rect.y)
        self.rect.x += self.axis.x
        self.rect.y += y_speed


background = pygame.transform.scale(load_image('background.png'), (width, height))
tile_images = {'dirt': load_image('dirt.png'), 'grass': load_image('grass.png'), 'sign': load_image('sign.png', -1), "enemy": load_image("enemy.png", -1)}
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

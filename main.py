import pygame
import sys, os

pygame.init()
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
tile_size = 50

score = 0
old_score = 0

lvls = ['level_1.txt', 'level_2.txt', 'level_3.txt']
current_lvl = 0
lvl_passed = False
finish_coords = [(1000, 84), (1100, 634), (1100, 784)]

hero_width = 50
hero_height = 66

enemyWidth = 40
enemyHeight = 40

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
tiles_sprite = pygame.sprite.Group()
coins_sprite = pygame.sprite.Group()
# enemy_sprite = pygame.sprite.Group()

level1Test = False
level2Test = False
level3Test = False

pygame.init()

SCREEN = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


class Button():

    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def input_check(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def color_change(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def play():
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        SCREEN.fill("black")

        play_text_btn = get_font(45).render("This is the PLAY screen.", True, "White")
        play_rect_btn = play_text_btn.get_rect(center=(640, 260))
        SCREEN.blit(play_text_btn, play_rect_btn)

        play_bc = Button(image=None, pos=(640, 460),
                         text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        play_bc.color_change(play_mouse_position)
        play_bc.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_bc.input_check(play_mouse_position):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        options_mouse_position = pygame.mouse.get_pos()

        SCREEN.fill("white")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        SCREEN.blit(options_text, options_rect)

        options_bc = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_bc.color_change(options_mouse_position)
        options_bc.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_bc.input_check(options_mouse_position):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        menu_mouse_position = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_btn = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                          text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        options_btn = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                             text_input="RECORDS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_btn = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                          text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_btn, options_btn, quit_btn]:
            button.color_change(menu_mouse_position)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.input_check(menu_mouse_position):
                    play()
                if options_btn.input_check(menu_mouse_position):
                    options()
                if quit_btn.input_check(menu_mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


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
    # newEnemy = None
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
            elif level[y][x] == '4':
                Coin(x, y)
            # newEnemy = Player.Enemy(x, y)
    return new_player, x, y  # newEnemy


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
        self.rect = self.image.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 15)
        self.axis = pygame.math.Vector2(0, 0)
        self.can_jump = False
        self.on_ground = True

    """
        Player.EnemyImage = load_image('enemy.png', -1)
        self.EnemyImage = Player.EnemyImage
        self.EnemyRect = self.EnemyImage.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 15)
        self.EnemyAxis = pygame.math.Vector2(0, 0)
        self.EnemyAxis.x = 3
    def Enemy(self, pos_x, pos_y):
        Player.EnemyImage = load_image('enemy.png', -1)
        self.EnemyImage = Player.EnemyImage
        self.EnemyRect = self.EnemyImage.get_rect().move(tile_size * pos_x + 15, tile_size * pos_y - 15)
    """

    def update(self):
        global player, lvl_x, lvl_y
        global score, old_score, lvls, current_lvl, lvl_passed, finish_coords  # enemy
        global level1Test, level2Test, level3Test
        global tiles_sprite, player_sprite
        keys = pygame.key.get_pressed()
        self.axis.x = 0
        y_speed = 0
        if keys[pygame.K_LEFT]:
            self.axis.x = -5
            self.image = Player.image_left
        if keys[pygame.K_RIGHT]:
            self.axis.x = 5
            self.image = Player.image_right
        if keys[pygame.K_UP] and self.can_jump:
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

            if self.rect.x == finish_coords[current_lvl][0] and self.rect.y == finish_coords[current_lvl][1] \
                    and current_lvl < len(finish_coords) - 1:
                self.rect.x = 0
                self.rect.y = 0
                player_sprite.empty()
                player_sprite.update()
                tiles_sprite.empty()
                current_lvl += 1
                old_score = score
                player, lvl_x, lvl_y = generate_level(load_level(lvls[current_lvl]))
                tiles_sprite.draw(screen)
            elif self.rect.x == finish_coords[current_lvl][0] and self.rect.y == finish_coords[current_lvl][1] \
                    and current_lvl == len(finish_coords) - 1:
                print('')

        if pygame.sprite.spritecollide(self, coins_sprite, True):
            score += 1

        self.rect.x += self.axis.x
        self.rect.y += y_speed

        if keys[pygame.K_r]:
            score = old_score
            update_score(str(score), 5, 5)
            self.rect.x = 0
            self.rect.y = 0
            player_sprite.empty()
            player_sprite.update()
            tiles_sprite.empty()
            player, lvl_x, lvl_y = generate_level(load_level(lvls[current_lvl]))
            tiles_sprite.draw(screen)

            # if sprite.rect.colliderect(self.EnemyRect.x + self.EnemyAxis.x, self.EnemyRect.y, enemyWidth, enemyHeight):
            #    self.EnemyAxis.x *= -1


background = pygame.transform.scale(load_image('background.png'), (width, height))
tile_images = {'dirt': load_image('dirt.png'), 'grass': load_image('grass.png'), 'sign': load_image('sign.png', -1),
               "enemy": load_image("enemy.png", -1)}
player, lvl_x, lvl_y = generate_level(load_level('level_1.txt'))  # enemy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    main_menu()
    screen.fill(pygame.Color('black'))
    player_sprite.update()
    screen.blit(background, (0, 0))
    tiles_sprite.draw(screen)
    coins_sprite.draw(screen)
    player_sprite.draw(screen)
    update_score(str(score), 5, 5)
    pygame.display.update()
    clock.tick(60)

import pygame
import sys, os


tileSize = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('white')    # цвет преград выберем сёдня
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class Player:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.facing = "right"
        self.death = False
    

    def playerImage(self):
        fullname = os.path.join('data', "playerImg.png")
        image = pygame.image.load(fullname)
        return image
    

    def setPos(self, posX, posY):
        self.posX = posX
        self.posY = posY
    

    def getPos(self):
        return (self.posX, self.posY)


class Render:
    def __init__(self, surface):
        self.display_surface = surface
        self.currentLevel = os.path.join('data', "level_1.txt")
        self.setup_level()
        self.world_shift = 0
        

    def setup_level(self, layout):
        tile_size = 64
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_i, row in enumerate(layout):
            for col_i, col in enumerate(row):
                #print(f'{row_i},{col_i}:{col}')
                if col == '1':
                    x, y = col_i * tile_size, row_i * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.player.update()
    
    def setLevel(self, level):
        currentLevel = "level"
        currentLevel += str(level)
        self.currentLevel = os.path.join('data', f'{currentLevel}.txt')


"""
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_i, row in enumerate(layout):
            for col_i, col in enumerate(row):
                #print(f'{row_i},{col_i}:{col}')
                x, y = col_i * tileSize, row_i * tileSize

                if col == '1':
                    tile = Tile((x, y), tileSize)
                    self.tiles.add(tile)

                if col == 'p':  # p это player
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)


    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.player.update()
"""




pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
screen.fill('black')
world_shift = 0

while True:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        currentPos = Player.getPos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if key[pygame.K_RIGHT]:
            if currentPos[0] < 1200:
                Player.setPos(currentPos[0], currentPos[1] + 5)
        if key[pygame.K_LEFT]:
            if currentPos[0] > 0:
                Player.setPos(currentPos[0], currentPos[1] - 5)
        if key[pygame.K_UP]:
            if currentPos[0] > 0:
                Player.setPos(currentPos[0] + 5, currentPos[1])
        if key[pygame.K_DOWN]:
            if currentPos[0] < 700:
                Player.setPos(currentPos[0] -51, currentPos[1])
        Render.run()
        pygame.display.update()
        clock.tick(60)













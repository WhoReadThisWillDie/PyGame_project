import pygame
import sys, os


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


class render:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.currentLevel = fullname = os.path.join('data', "level_1.txt")
        self.setup_level()
        self.world_shift = 0

    def setup_level(self, layout):
        tile_size = 64
        self.tiles = pygame.sprite.Group()
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
    
    def setLevel(self,level):
        level = "level"

        self.currentLevel = fullname = os.path.join('data', "level_1.txt")



pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
screen.fill('black')
fullname = os.path.join('data', "level_1.txt")
world_shift = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if 
        pygame.display.update()
        clock.tick(60)













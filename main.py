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

class Player1:
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
        self.currentLevel = [[]]
        self.setLevel(1)
        self.world_shift = 0
        self.setup_level(surface)
        

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
        currentLevel = "level_"
        currentLevel += str(level)
        with open(f"{currentLevel}.txt") as text1:
            text = text1.readlines()
        times = 0
        for n1 in text:
            for n2 in n1:
                if n2 != '\n':
                    self.currentLevel[times].append(n2)
            self.currentLevel.append([])
            times += 1




pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
screen.fill('black')
world_shift = 0
while True:
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        currentPos = Player1().getPos( )
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if key[pygame.K_RIGHT]:
            if currentPos[0] < 1200:
                Player1().setPos(currentPos[0], currentPos[1] + 5)
        if key[pygame.K_LEFT]:
            if currentPos[0] > 0:
                Player1().setPos(currentPos[0], currentPos[1] - 5)
        if key[pygame.K_UP]:
            if currentPos[1] > 0:
                Player1().setPos(currentPos[0], currentPos[1] + 5)
        if key[pygame.K_DOWN]:
            if currentPos[1] < 700:
                Player1().setPos(currentPos[0], currentPos[1] - 5)
        Render(screen).run()
        pygame.display.update()
        clock.tick(60)
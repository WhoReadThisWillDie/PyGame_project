import pygame
from settings import tile_size
from tile import Tile

class Level1:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
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


















import pygame
from settings import tile_size
from tile import Tile
from player import Player

class Level1:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_i, row in enumerate(layout):
            for col_i, col in enumerate(row):
                #print(f'{row_i},{col_i}:{col}')
                x, y = col_i * tile_size, row_i * tile_size

                if col == '1':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if col == 'p':  # p это player
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.player.update()
















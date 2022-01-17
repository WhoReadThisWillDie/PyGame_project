import pygame
from settings import tile_size, screen_width
from tile import Tile
from player import *


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
                # print(f'{row_i},{col_i}:{col}')
                x, y = col_i * tile_size, row_i * tile_size

                if col == '1':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if col == 'p':  # p это player
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        axis_x = player.axis.x
        if player_x < screen_width / 4 and axis_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and axis_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.axis.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.axis.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.axis.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        self.make_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.axis.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.axis = 0
                elif player.axis.y < 0:
                    player.rect.top = sprite.rect.bottom

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.draw(self.display_surface)
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.scroll_x()

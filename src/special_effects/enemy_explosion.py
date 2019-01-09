# coding=utf-8
import pygame

from src.components.PVector import PVector
from src.constants import GFX


class EnemyExplosion(pygame.sprite.Sprite):
    def __init__(self, game, enemy):
        super().__init__(game.special_effects)
        self.pos = enemy.pos
        self.ratio = enemy.image.get_width() / 150
        self.frame = 0
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

    def update(self, *args):
        self.frame+=1
        if self.frame > 90:
            self.kill()
        else:
            orig_image = GFX[f'explosion_100{self.frame//10}{self.frame%10}']
            dimensions = PVector.from_tuple(orig_image.get_size())
            self.image = pygame.transform.scale(orig_image, tuple((dimensions * self.ratio).trunc()))
            self.rect = self.image.get_rect(center=tuple(self.pos))

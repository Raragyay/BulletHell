# coding=utf-8
import pygame

from src.components.PVector import PVector
from src.constants import GFX


class BulletExplosion(pygame.sprite.Sprite):  # TODO All explosions have base class?
    def __init__(self, game, weapon_level, pos):
        super().__init__(game.special_effects)
        i = game.frame % 50 + 1  # between 1 and 50
        image = GFX[f'fire1_ {i//10}{i%10}']  # If number is less than 10, will have 0 at start
        size = (PVector.from_tuple(image.get_size()) / 10 * weapon_level).trunc()
        self.image = pygame.transform.scale(image, tuple(size))
        self.rect = self.image.get_rect(center=tuple(pos))

    def update(self):
        self.kill()

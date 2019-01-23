# coding=utf-8
from itertools import cycle

import pygame

from src.constants import GFX


class Cone(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.special_effects)
        self.pos = pos
        self.images = cycle(
            [pygame.transform.flip(GFX['h_st_00{}{}'.format(x // 10, x % 10)], False, True) for x in range(1, 16)])
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 100:
            self.kill()

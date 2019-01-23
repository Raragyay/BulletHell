# coding=utf-8
from itertools import cycle

import pygame

from src.constants import GFX, SFX


class WarningSign(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game.special_effects)
        self.pos = pos
        self.images = cycle((GFX['warningitem'], GFX['name_blank']))
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.frame = 0
        SFX['alarm'].play()

    def update(self):
        self.frame += 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= 120:
            self.kill()

# coding=utf-8
from itertools import cycle

import pygame

from src.constants import GFX, SFX
from src.items.powerup import Powerup


class Life(Powerup):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        self.images = cycle([GFX[f'life{x}'] for x in range(1, 7)])
        self.image: pygame.Surface = next(self.images)

    def apply_effect(self, player):
        SFX['life'].play()
        player.lives += 1

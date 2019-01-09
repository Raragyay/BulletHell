# coding=utf-8
from __future__ import annotations

from itertools import cycle
from typing import TYPE_CHECKING

import pygame

from src.components.PVector import PVector
from src.constants import GFX

if TYPE_CHECKING:
    from src.enemies.enemy import Enemy


class Exhaust(pygame.sprite.Sprite):
    def __init__(self, enemy: Enemy, offset: PVector, type: int, reverse: bool):
        super().__init__(enemy.game.special_effects)
        assert 1 <= type <= 3
        self.frame = 0
        self.enemy = enemy
        self.offset = offset
        self.pos = self.enemy.pos + self.offset
        self.images = cycle(
                [pygame.transform.flip(GFX[f'exhaust{type}_frame{x}'], False, reverse) for x in range(1, 9)])
        self.image: pygame.Surface = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def update(self):
        # Move
        self.pos = self.enemy.pos + self.offset
        self.rect.center = tuple(self.pos)

        self.frame += 1
        if self.frame % 4 == 0:
            self.image = next(self.images)

        if not self.enemy.alive():
            self.kill()

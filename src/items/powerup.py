# coding=utf-8
from __future__ import annotations
from itertools import cycle
from math import copysign

import pygame

from src.components.PVector import PVector
from src.constants import GFX, HEIGHT, WIDTH, SFX
from src.items.item import Item
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.level import Level


class Powerup(Item):
    speed = 2

    def __init__(self, game: Level, pos):
        super().__init__(game, pos)
        # print("spawned powerup")
        f = self.game.frame % 4
        self.direction: PVector = PVector(copysign(1, f % 3 - 1), copysign(1, f // 2 - 1)) * self.speed
        # this results in (-1,-1) (1,-1) (1,1) (-1,1) * speed for 0-3, effectively "randomizing" the direction
        self.images = cycle([GFX[f'power{x}'] for x in range(1, 7)])
        self.image: pygame.Surface = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.frame = 0

    def move(self):
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

    def update_img(self):
        self.frame += 1
        if self.frame % 4 == 1:
            # print("updating image")
            self.image = next(self.images)

    def check_oob(self):
        a = self.rect
        if self.frame < 3600:  # 1 minute
            if a.bottom >= HEIGHT or a.top <= 0:
                # print("flip_y")
                self.direction.flip_y(in_place=True)
            if a.right >= WIDTH or a.left <= 0:
                # print("flip_x")
                self.direction.flip_x(in_place=True)
        else:
            super().check_oob()

    def apply_effect(self, player):
        # print(f"collected at {self.pos}")
        SFX['powerup'].play()
        if player.weapon_level <= 7:
            player.weapon_level += 1
        else:
            player.score += 50000

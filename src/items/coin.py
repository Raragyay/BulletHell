# coding=utf-8

from __future__ import annotations
from random import randint

import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.States.level import Level
from src.components.PVector import PVector
from src.constants import GFX, SFX
from src.items.item import Item


class Coin(Item):
    def __init__(self, game: Level, pos, target=None):
        super().__init__(game, pos)
        self.target = target
        luck = randint(20, 30)
        rand_speed = randint(1, 2)
        self.speed = 20 if self.target else luck / 4 + rand_speed
        self.value = luck * 100
        self.direction: PVector = None
        self.image: pygame.Surface = pygame.transform.scale(GFX['coin'], (luck, luck))
        self.rect: pygame.Rect = self.image.get_rect(center=tuple(self.pos))

    def calc_direction(self):
        if self.target:
            angle = self.pos.angle_to(self.target.pos)
            self.direction = PVector(0, 0).project(angle, self.speed)
        else:
            self.direction = PVector(0, self.speed)

    def move(self):
        self.calc_direction()
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

    def apply_effect(self, player):
        player.score += self.value
        SFX['coin'].play()

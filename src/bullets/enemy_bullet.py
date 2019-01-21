# coding=utf-8
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from src.bullets.bullet import Bullet
from src.components.PVector import PVector

if TYPE_CHECKING:
    from src.states.level import Level


class EnemyBullet(Bullet):
    def __init__(self, game: Level, pos: PVector):
        super().__init__(game.enemy_bullets)
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.direction: PVector = None
        self.pos: PVector = pos
        self.frame = 0

    def update(self):
        self.frame += 1
        self.check_oob()
        self.move()
        self.update_img()
        self.custom_action()

    def move(self):
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

    def custom_action(self):
        pass

    def update_img(self):
        pass

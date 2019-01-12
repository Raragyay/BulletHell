# coding=utf-8
from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from src.components.PVector import PVector
from src.constants import GFX
from src.enemies.enemy import Enemy

if TYPE_CHECKING:
    from src.states.level import Level


class Sergeant0(Enemy):
    health = 300
    speed = 1

    def __init__(self, game: Level, pos: PVector):
        super().__init__(game, pos)
        self.direction=PVector(0,self.speed)
        self.image=pygame.transform.flip(GFX['e_sergeant0.png'],False,True)



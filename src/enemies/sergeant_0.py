# coding=utf-8
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

import pygame

from src.bullets.enemy_weapons import SergeantWeapon0
from src.components.PVector import PVector
from src.constants import GFX
from src.enemies.enemy import Enemy
from src.items.coin import Coin
from src.special_effects.enemy_explosion import EnemyExplosion
from src.special_effects.exhaust import Exhaust

if TYPE_CHECKING:
    from src.states.level import Level


class Sergeant0(Enemy):
    health = 300
    speed = 1

    def __init__(self, game: Level, pos: PVector):
        super().__init__(game, pos)
        self.direction = PVector(0, self.speed)
        self.image: pygame.Surface = pygame.transform.flip(GFX['e_sergeant0'], False, True)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((60, 60))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        self.weapon = SergeantWeapon0
        self.target: PVector
        Exhaust(self, PVector(-15, -90), 1, True)
        Exhaust(self, PVector(15, -90), 1, True)

    def check_shoot(self):
        # Need to lock its position before firing, otherwise it's too accurate
        if self.frame % 200 > 150:
            if self.frame % 10 == 1:
                left_pos = self.pos + PVector(-40, 55)
                right_pos = self.pos + PVector(40, 55)
                self.weapon(self, left_pos, self.target)
                self.weapon(self, right_pos, self.target)
        elif self.frame % 200 == 149:  # Lock right before firing
            self.target = self.find_target_pos()

    def check_death(self):
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            for _ in range(5):
                Coin(self.game, self.pos + PVector(randint(-25, 25), randint(-90, 90)))
            self.kill()
            self.hitbox.kill()

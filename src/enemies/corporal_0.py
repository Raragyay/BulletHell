# coding=utf-8
from __future__ import annotations
from math import degrees
from random import randint

import pygame

from src.bullets.corporal_bullet import CorporalBullet
from src.components.PVector import PVector
from src.constants import GFX, HEIGHT
from src.enemies.enemy import Enemy
from src.special_effects.enemy_explosion import EnemyExplosion
from src.items.coin import Coin
from typing import TYPE_CHECKING

from src.special_effects.exhaust import Exhaust

if TYPE_CHECKING:
    from src.states.level import Level


class Corporal0(Enemy):
    speed = 1

    def __init__(self, game: Level, pos: PVector):
        super().__init__(game, pos)
        self.speed = Corporal0.speed
        self.health = 100
        self.direction = PVector(0, Corporal0.speed)
        self.target = self.find_target_pos()
        self.image: pygame.Surface = pygame.transform.flip(GFX['e_corporal0'], False, True)
        self.rect: pygame.Rect = self.image.get_rect(center=tuple(self.pos))
        # Pretty much the "main" portion of the ship excluding wings.
        self.hitbox.image: pygame.Surface = pygame.Surface((44, 50))
        self.hitbox.rect: pygame.Rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        Exhaust(self, PVector(0, -90), 1, True)


    def check_shoot(self):  # Shoot a circle to try and "trap" the player
        if self.frame % 150 == 0:  # Shoot every 2.5 seconds
            target = self.find_target_pos()
            angle = (degrees(self.pos.angle_to(target)) + 360) % 360
            # So it is between 0 and 360, because atan can be negative
            # print(angle)
            for i in range(0, 360, 15):
                a = angle - i
                if abs(a) >= 30:  # 60 degrees around player are empty
                    # print(i)
                    CorporalBullet(self.game, self.pos, i, target)

    def check_death(self):
        if self.rect.top >= HEIGHT:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            for i in range(3):
                Coin(self.game, self.pos + PVector(randint(-20, 20), randint(-20, 20)))
            self.kill()
            self.hitbox.kill()

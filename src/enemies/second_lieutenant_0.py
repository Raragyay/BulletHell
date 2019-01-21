# coding=utf-8
from random import randint

import pygame

from src.bullets.enemy_weapons import SecondLieutenantWeapon0
from src.components.PVector import PVector
from src.constants import GFX
from src.enemies.enemy import Enemy
from src.items.coin import Coin
from src.special_effects.enemy_explosion import EnemyExplosion
from src.special_effects.exhaust import Exhaust


class SecondLieutenant0(Enemy):
    """
    Ship moves upwards but stops when firing.
    """
    health = 400
    speed = 0.5

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.direction = PVector(0, -self.speed)
        self.image = GFX['e_secondlieutenant0']
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((50, 180))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        Exhaust(self, PVector(-10, 150), 3, False)
        Exhaust(self, PVector(0, 150), 3, False)
        Exhaust(self, PVector(10, 150), 3, False)

    def check_shoot(self):
        if self.frame % 200 > 150:
            self.direction = PVector(0, 0)
            if self.frame % 10 == 0:
                SecondLieutenantWeapon0(self,self.pos)
        else:
            self.direction = PVector(0, -self.speed)

    def check_death(self):
        if self.rect.bottom <= 0:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            for _ in range(7):
                Coin(self.game, self.pos + PVector(randint(-25, 25), randint(-90, 90)))
            self.kill()
            self.hitbox.kill()

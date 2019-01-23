# coding=utf-8
from random import randint

import pygame

from src.bullets.first_lieutenant_bullet import FirstLieutenantBullet
from src.components.PVector import PVector
from src.constants import GFX
from src.enemies.enemy import Enemy
from src.items.coin import Coin
from src.special_effects.enemy_explosion import EnemyExplosion
from src.special_effects.exhaust import Exhaust


class FirstLieutenant0(Enemy):  # Shoots a rotating bullet that increases in radius
    health = 400
    speed = 0.5

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.direction = PVector(0, self.speed)
        self.image = pygame.transform.flip(GFX['e_firstlieutenant0'], False, True)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((80, 50))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        self.circle_radius_delta = 0.5
        self.initial_radius = 10
        Exhaust(self, PVector(-24, -90), 1, True)
        Exhaust(self, PVector(24, -90), 1, True)

    def check_shoot(self):
        if self.frame % 200 > 150:
            if self.frame % 5 == 1:
                self.shoot()

    def shoot(self):
        left_weapon = self.pos + PVector(-20, 40)
        right_weapon = self.pos + PVector(20, 40)
        if self.game.player_1.alive() and self.game.player_2.alive():
            FirstLieutenantBullet(self.game, left_weapon, self.initial_radius, 0, self.game.player_1.pos.copy(), 15,
                                  self.circle_radius_delta)
            FirstLieutenantBullet(self.game, right_weapon, self.initial_radius, 0, self.game.player_2.pos.copy(), 15,
                                  self.circle_radius_delta)
        else:
            target = self.find_target_pos()
            FirstLieutenantBullet(self.game, left_weapon, self.initial_radius, 0, target, 15, self.circle_radius_delta)
            FirstLieutenantBullet(self.game, right_weapon, self.initial_radius, 0, target, 15, self.circle_radius_delta)

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            for _ in range(9):
                Coin(self.game, self.pos + PVector(randint(-40, 40), randint(-25, 25)))
            self.kill()
            self.hitbox.kill()

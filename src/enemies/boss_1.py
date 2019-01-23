# coding=utf-8
from itertools import cycle
from random import randint

import pygame

from src.bullets.boss_bullet_1 import BossBullet1
from src.bullets.enemy_weapons import Boss1Pattern1, Boss1Pattern2
from src.components.PVector import PVector
from src.constants import GFX, WIDTH
from src.enemies.enemy import Enemy
from src.items.coin import Coin
from src.items.life import Life
from src.special_effects.ending_explosion import EndingExplosion
from src.special_effects.enemy_explosion import EnemyExplosion
from src.special_effects.exhaust import Exhaust
from src.special_effects.warning_cone import Cone


class Boss1(Enemy):
    health = 1
    speed = 0.5

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.target: PVector = None
        self.base_health = Boss1.health
        self.health_percent = self.health / self.base_health
        self.direction = PVector(1, 0)
        self.image = pygame.transform.flip(GFX['boss11'], False, True)
        self.rect = self.image.get_rect(center=tuple(self.pos))

        self.hitbox.image = pygame.Surface((100, 100))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        Exhaust(self, PVector(-78, -140), 2, True)
        Exhaust(self, PVector(78, -140), 2, True)
        # TODO ROTATERING

        self.effect_img = cycle([GFX['e_00{}{}'.format(x // 10, x % 10)] for x in range(1, 16)])
        self.effect_image = next(self.effect_img)
        self.shooting = False

    def move(self):
        if self.rect.left <= 0:
            self.direction = PVector(1, 0)
        elif self.rect.right >= WIDTH:
            self.direction = PVector(-1, 0)
        self.pos += self.direction * self.speed
        self.rect.center = tuple(self.pos)
        self.hitbox.rect.center = tuple(self.pos)

    def update_img(self):
        if self.shooting:
            if self.health_percent <= 0.2:  # less than 20% health
                self.image = pygame.transform.flip(GFX['boss12'], False, True)
            else:
                self.image = pygame.transform.flip(GFX['boss11'], False, True)

            self.image.blit(self.effect_image, (self.image.get_width() / 2 - 32, self.image.get_height() / 2 - 32))
            self.effect_image = next(self.effect_img)
        else:
            if self.health_percent <= 0.2:  # less than 20% health
                self.image = pygame.transform.flip(GFX['boss12'], False, True)
            else:
                self.image = pygame.transform.flip(GFX['boss11'], False, True)

    def check_shoot(self):
        if self.health_percent >= 0.5:
            if self.frame % 400 == 101:
                self.speed = 0
                self.shooting = False
                Cone(self.game, self.pos + PVector(0, 250))
            elif self.frame % 400 >= 300:
                self.shooting = False
                self.speed = Boss1.speed
            elif self.frame % 400 >= 200:
                self.shooting = True
                self.speed = 0
                BossBullet1(self.game, self.pos)
        elif self.health_percent >= 0.2:
            if self.frame % 20 == 1:
                self.shooting = True
                self.speed = Boss1.speed
                Boss1Pattern1(self, self.pos)
            else:
                self.shooting = False
        else:
            self.speed = 0
            Boss1Pattern2(self, self.pos)

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.hitbox.kill()
            EnemyExplosion(self.game, self)
            Life(self.game, self.pos)
            for _ in range(50):
                Coin(self.game, self.pos + PVector(randint(-50, 50), randint(-50, 50)))
            EndingExplosion(self.game)

    def custom_action(self):
        self.health_percent = self.health / self.base_health

# coding=utf-8
from itertools import cycle
from random import randint

import pygame

from src.bullets.enemy_weapons import ColonelWeapon1
from src.components.PVector import PVector
from src.constants import GFX, WIDTH
from src.enemies.enemy import Enemy
from src.items.coin import Coin
from src.special_effects.emerge_2 import Emerge2
from src.special_effects.enemy_explosion import EnemyExplosion
from src.special_effects.exhaust import Exhaust


class Colonel0(Enemy):
    health = 800
    speed = 1

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.direction = PVector(self.speed, 0)
        self.image = pygame.transform.flip(GFX['e_colonel0'], False, True)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((128, 80))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        Exhaust(self, PVector(-48, -63), 2, True)
        Exhaust(self, PVector(48, -63), 2, True)
        self.effect_img = cycle([GFX['e_00{}{}'.format(x // 10, x % 10)] for x in range(1, 16)])
        self.effect_image = next(self.effect_img)
        self.shooting = False
        self.weapon_of_choice=ColonelWeapon1

    def check_shoot(self):
        if self.frame % 200 > 100:
            self.shoot()
            self.shooting = True
        else:
            self.shooting = False

    def shoot(self):
        if self.frame % 200 == 110:
            self.weapon_of_choice(self, self.pos, 7)
        if self.frame % 200 == 120:
            self.weapon_of_choice(self, self.pos, 6)
        if self.frame % 200 == 130:
            self.weapon_of_choice(self, self.pos, 5)
        if self.frame % 200 == 140:
            self.weapon_of_choice(self, self.pos, 4)
        if self.frame % 200 == 150:
            self.weapon_of_choice(self, self.pos, 3)
        if self.frame % 200 == 160:
            self.weapon_of_choice(self, self.pos, 2)
        if self.frame % 200 == 170:
            self.weapon_of_choice(self, self.pos, 1)

    def update_img(self):

        self.image = pygame.transform.flip(GFX['e_colonel0'], False, True)
        if self.frame % 200 > 100:
            self.image.blit(self.effect_image, (self.image.get_width() / 2 - 32, self.image.get_height() / 2 - 32))
            self.effect_image = next(self.effect_img)

    def move(self):
        super().move()
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def check_death(self):
        if self.frame >= 2000:
            Emerge2(self.game, self.pos)
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            for _ in range(9):
                Coin(self.game, self.pos + PVector(randint(-60, 60), randint(-40, 40)))
            self.kill()
            self.hitbox.kill()

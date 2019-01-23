# coding=utf-8
# coding=utf-8
from itertools import cycle

import pygame

from src.bullets.captain_bullet_0 import CaptainBullet0
from src.components.PVector import PVector
from src.constants import GFX
from src.enemies.enemy import Enemy
from src.items.bomb import Bomb
from src.special_effects.enemy_explosion import EnemyExplosion


class Captain0(Enemy):  # Shoots a sprial of bullets
    health = 100
    speed = 0.5

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.direction = PVector(0, self.speed)
        self.image = pygame.transform.flip(GFX['e_captain0'], False, True)
        self.rect = self.image.get_rect(center=tuple(self.pos))
        self.hitbox.image = pygame.Surface((60, 60))
        self.hitbox.rect = self.hitbox.image.get_rect(center=tuple(self.pos))
        self.effect_img = cycle([GFX['e_00{}{}'.format(x // 10, x % 10)] for x in range(1, 16)])
        self.effect_image = next(self.effect_img)

    def check_shoot(self):
        if self.frame % 200 > 100:
            self.shoot()

    def shoot(self):
        CaptainBullet0(self.game, self.pos, self.frame * 5)
        CaptainBullet0(self.game, self.pos, -self.frame * 5)

    def update_img(self):
        self.image = pygame.transform.flip(GFX['e_captain0'], False, True)
        if self.frame % 200 > 100:
            self.image.blit(self.effect_image, (self.image.get_width() / 2 - 32, self.image.get_height() / 2 - 32))
            self.effect_image = next(self.effect_img)

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            Bomb(self.game, self.pos)
            self.kill()
            self.hitbox.kill()

# coding=utf-8
import pygame

from src.bullets.captain_bullet_1 import CaptainBullet1
from src.constants import GFX
from src.enemies.captain_0 import Captain0
from src.items.powerup import Powerup
from src.special_effects.enemy_explosion import EnemyExplosion


class Captain1(Captain0):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = pygame.transform.flip(GFX['e_captain1'], False, True)

    def check_death(self):
        if self.rect.top >= 800:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            Powerup(self.game, self.pos)
            self.kill()
            self.hitbox.kill()

    def shoot(self):
        CaptainBullet1(self.game, self.pos,self.frame*14)

    def update_img(self):
        self.image = pygame.transform.flip(GFX['e_captain1'], False, True)
        if self.frame % 200 > 100:
            self.image.blit(self.effect_image, (self.image.get_width() / 2 - 32, self.image.get_height() / 2 - 32))
            self.effect_image = next(self.effect_img)

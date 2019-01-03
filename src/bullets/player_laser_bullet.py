# coding=utf-8
import pygame

from src.components.PVector import PVector
from src.bullets.bullet import Bullet
from src.constants import GFX


class PlayerLaserBullet(Bullet):
    speed = 10

    def __init__(self, player, *group):
        super().__init__(*group)
        self.game = player.game
        self.player = player

        self.pos = self.player.pos - PVector(0, 40) + self.player.direction.x * PVector(4, 0)
        # if self.player.id in {3, 4}:
        #     self.pos -= PVector(0, 3)

        self.image_0: pygame.Surface = None
        self.image_1: pygame.Surface = None

        self.damage = 0

        self.choose_image()
        self.align_frame()
        self.calc_damage()

        self.rect = self.image.get_rect(center=tuple(self.pos))

    def choose_image(self):
        lev = self.player.weapon_level
        pid = self.player.id
        self.image_0 = pygame.transform.scale(GFX[f'{pid*2-1}'], (lev * 10, 30))
        self.image_1 = pygame.transform.scale(GFX[f'{pid*2}'], (lev * 10, 30))

    def align_frame(self):
        if self.game.frame % 8 <= 3:
            self.image = self.image_0
        else:
            self.image = self.image_1

    def calc_damage(self):
        if self.player.id in {1, 2}:
            self.damage = 2 * (1 + self.player.weapon_level / 2.0)
        else:
            self.damage = 2 * (0.8 + self.player.weapon_level / 2.0)

    def update(self):
        if not self.player.weapon_2:
            self.kill()
        self.align_frame()
        self.pos.x = self.player.hitbox.rect.center[0] + self.player.direction.x * 4
        self.pos.y -= self.speed
        self.rect.center = tuple(self.pos)
        self.check_oob()

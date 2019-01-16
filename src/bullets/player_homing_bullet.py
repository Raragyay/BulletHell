# coding=utf-8
from math import degrees

import pygame

from src.bullets.bullet import Bullet
from src.bullets.player_bullet import PlayerBullet
from src.components.PVector import PVector


class PlayerHomingBullet(PlayerBullet):
    speed = 5
    max_speed=15

    def __init__(self, player, offset, bullet_level: int):
        super().__init__(player, 90, offset, bullet_level)
        self.orig_image: pygame.Surface = pygame.transform.scale(self.orig_image, (self.orig_image.get_width(), 20))
        self.rect: pygame.Rect = self.image.get_rect(center=tuple(self.pos))
        self.rect.inflate_ip(-5, -5)  # Just like before
        # A little less tall to distinguish
        self.game = self.player.game
        self.angle = 0
        self.speed = PlayerHomingBullet.speed
        self.target = None
        self.target_pos: PVector = None
        self.determine_target()

    def determine_target(self):
        class default:
            class rect:
                center = (self.pos.x, -100)

            rect = rect

            @classmethod
            def alive(cls):
                return False

        self.target = min(self.game.enemy_hitboxes,
                          key=lambda x: self.pos.dist_from(PVector.from_tuple(x.rect.center)),
                          default=default)
        self.target_pos = PVector.from_tuple(self.target.rect.center)

    def update(self):
        if not self.target.alive():
            self.determine_target()
        self.update_direc()
        self.update_image()
        self.move()
        self.check_oob()

    def update_direc(self):
        # print(target_pos)
        self.target_pos = PVector.from_tuple(self.target.rect.center)
        self.speed = min(self.max_speed, self.speed + 0.1)
        self.angle = self.pos.angle_to(self.target_pos)
        self.direction = PVector(0, 0).project(self.angle, self.speed)

    def update_image(self):
        self.image: pygame.Surface = pygame.transform.rotate(self.orig_image.copy(), degrees(self.angle) - 90)
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def move(self):
        self.pos += self.direction
        self.rect.center = tuple(self.pos)

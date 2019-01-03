# coding=utf-8
from math import copysign, sqrt, degrees, sin, radians, cos

import pygame

from src.components.PVector import PVector
from src.constants import GFX, HEIGHT, WIDTH
from src.enemies.enemy import Enemy
from src.explosion.enemy_explosion import EnemyExplosion
from src.items.coin import Coin


class Private0(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.health = 10
        self.speed = 4
        self.starting_pos = PVector.from_tuple(pos)
        self.target_pos = self.find_target_pos()

        self.image = GFX['e_private0']
        self.orig_image = GFX['e_private0']
        self.image_rotation = 0
        self.rect = self.image.get_rect(center=tuple(self.starting_pos))

        self.hitbox.image = pygame.Surface((20, 20))
        self.hitbox.rect = self.hitbox.image.get_rect(
            center=(self.pos.x, self.pos.y - 6))  # hit box is the "engine" part

    def move(self):
        if self.starting_pos == self.target_pos:  # how could this happen to me
            self.kill()
            self.hitbox.kill()
        elif self.starting_pos.x == self.target_pos.x:
            self.pos += PVector(0, copysign(self.speed, self.target_pos.y - self.starting_pos.y))
            self.image_rotation = 180 if self.starting_pos.y > self.target_pos.y else 0
            # if self.starting_pos.y > self.target_pos.y:
            #     self.pos -= PVector(0, self.speed)  # move upwards
            # else:
            #     self.pos += PVector(0, self.speed)
        elif self.starting_pos.y == self.target_pos.y:
            self.pos += PVector(copysign(self.speed, self.target_pos.x - self.starting_pos.x), 0)

            self.image_rotation = -90 if self.starting_pos.x > self.target_pos.x else 90

            # if self.starting_pos.x>self.target_pos.x: #move left
            #     self.pos-=PVector(0,self.speed)
            # else:
            #     self.pos+=PVector(0,self.speed)
        else:
            # Parabola with destination as vertex
            # equation is y=a(x-end.x)^2+end.y
            # solve for a by subbing in start.x, start.y
            s = self.starting_pos
            e = self.target_pos
            a = (s.y - e.y) / ((s.x - e.x) ** 2)
            f = lambda x: a * (x - e.x) ** 2 + e.y
            new_x = self.pos.x + copysign(
                max(2/a/self.pos.x, ((self.pos.x-self.target_pos.x)/200)**2),
                self.target_pos.x - self.starting_pos.x)  # TODO fix speed
            # the speed will be minimum self.speed and will occur between +-100 pixels of the target
            new_y = f(new_x)
            new_pos = PVector(new_x, new_y)

            # To simplify, assume speed/2 is x speed. Otherwise, would take lots and lots of math
            angle_to_new_pos = degrees(self.pos.angle_to(new_pos))
            self.image_rotation = angle_to_new_pos + 90
            self.pos = new_pos
        self.rect.center = tuple(self.pos)
        self.hitbox.rect.center = (
            self.pos.x + 6 * sin(radians(self.image_rotation)), self.pos.y - 6 * cos(radians(self.image_rotation)))

    def update_img(self):
        self.image = pygame.transform.rotate(self.orig_image.copy(), self.image_rotation)
        # assume that pos is on the parabola, want to find point on the parabola whose straight line is the same
        # as speed

    def check_death(self):
        if self.rect.top > HEIGHT:
            self.kill()
            self.hitbox.kill()
        elif self.rect.bottom < 0:
            self.kill()
            self.hitbox.kill()
        elif self.rect.left > WIDTH:
            self.kill()
            self.hitbox.kill()
        elif self.rect.right < 0:
            self.kill()
            self.hitbox.kill()
        if self.health <= 0:
            EnemyExplosion(self.game, self)
            Coin(self.game, self.pos, None)
            self.kill()
            self.hitbox.kill()

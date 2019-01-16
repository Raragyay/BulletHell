# coding=utf-8
from math import copysign, sqrt, degrees, sin, radians, cos

import pygame

from src.components.PVector import PVector
from src.constants import GFX, HEIGHT, WIDTH
from src.enemies.enemy import Enemy
from src.special_effects.enemy_explosion import EnemyExplosion
from src.items.coin import Coin


class Private0(Enemy):
    health = 10
    speed = 4
    vert_travel_threshold = 10

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.starting_pos = PVector.from_tuple(pos)
        self.target_pos = self.find_target_pos()

        s = self.starting_pos
        v = self.target_pos
        # TODO if s.x-v.x=0
        if not abs(s.x - v.x) <= self.vert_travel_threshold:
            self.a: float = float(s.y - v.y) / float(((s.x - v.x) ** 2))

        self.image = GFX['e_private0']
        self.orig_image = GFX['e_private0']
        self.image_rotation = 0
        self.rect = self.image.get_rect(center=tuple(self.starting_pos))
        self.log: str = ""

        self.hitbox.image = pygame.Surface((20, 20))
        self.hitbox.rect: pygame.Rect = self.hitbox.image.get_rect(
                center=(self.pos.x, self.pos.y - 6))  # hit box is the "engine" part

    def move(self):
        if self.starting_pos == self.target_pos:  # how could this happen to me
            self.kill()
            self.hitbox.kill()
        elif abs(self.starting_pos.x - self.target_pos.x) <= self.vert_travel_threshold:
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
            a = self.a
            s = self.starting_pos
            v = self.target_pos
            # Parabola with destination as vertex
            # equation is y=a(x-end.x)^2+end.y
            # solve for a by subbing in start.x, start.y
            f = lambda x: a * (x - v.x) ** 2 + v.y

            # Condition: if ship is within 1 pixel of vertex and is approaching it, flip it over to the other side.
            # This is because the slope of the quadratic as we approach the vertex is very small; therefore, a large
            # amount of the speed is allocated to delta_x. This results in an enormous shift in delta_y which
            # effectively makes the ship disappear.

            if v.x - self.pos.x == copysign(v.x - self.pos.x, v.x - s.x) and abs(self.pos.x - v.x) <= 1:
                delta_x = 2
            else:

                # Goal: delta_x^2 + delta_y^2=speed^2
                # Known: dy/dx = 2*a*(x-v.x)
                # Approximate dy=delta_y, dx=delta_x
                # delta_y=2*a*(x-v.x)*delta_x
                # Let z=2*a*(x-v.x)
                # delta_y=z*delta_x
                # Substitute: delta_x^2+(z*delta_x)^2=speed^2
                # Expand: delta_x^2+z^2*delta_x^2=speed^2
                # Collect: (delta_x^2)(1+z^2)=speed^2
                # Divide: delta_x^2=(speed^2)/(1+z^2)
                # Take the root: delta_x=sqrt(speed^2/(1+z^2))
                z = 2 * a * (self.pos.x - v.x)
                delta_x = sqrt(self.speed ** 2 / (1 + z ** 2))
            new_x = self.pos.x + copysign(delta_x, v.x - s.x)
            new_y = f(new_x)

            # TODO Problem: when position.x is very close to vertex, slope of derivative is very small, approximation is very inaccurate.
            # inverse_f = lambda y: sqrt(abs(y - v.y) / a) + v.x  # Doesn't work because it's not a function
            # """
            # Potential bug: When Vertex x is very close to current.x, delta x is extremely large.
            # Therefore, min value has been implemented to remove that possibility
            # """
            # dist_from_v = copysign(max(abs(self.pos.x - v.x), 1), s.x - v.x)
            # new_x = self.pos.x + copysign(
            #     max(min(abs(self.speed / (2 * a * dist_from_v)), self.speed),abs(1/a)),  # max(abs(self.pos.x -
            # v.x), 1 / a / 2),
            #     v.x - s.x)  # TODO fix speed
            # new_y = f(new_x)
            self.log += f'Current:{self.pos}, Future:{PVector(new_x,new_y)}, Start:{s}, Vertex:{v}, a-value:{a},delta_x:{delta_x}\n'
            assert -50 <= new_x <= 650 and -50 <= new_y <= 850, f'{self.log}{new_x},{new_y}\n' \
                                                                f'{new_x-v.x}\n' \
                                                                f'{(new_x-v.x)**2}\n' \
                                                                f'{a*(new_x-v.x)**2}\n' \
                                                                f'{a*(new_x-v.x)**2+v.y}\n'

            #
            # delta_x = abs(new_x - self.pos.x)
            # assert delta_x >= 0.01, f'{self.log}'
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

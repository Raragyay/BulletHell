# coding=utf-8
from __future__ import annotations
import pygame

from src.components.PVector import PVector
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.player import Player


class Enemy(pygame.sprite.Sprite):
    """
    Base enemy class.
    """

    def __init__(self, game, pos):
        super().__init__(game.enemies)
        self.tag = 'enemy'
        self.health: int
        self.speed: int
        self.game = game
        self.pos: PVector = pos  # It's a list, but still an iterable
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.hitbox: pygame.sprite.Sprite = pygame.sprite.Sprite(game.enemy_hitboxes)
        self.hitbox.body = self  # When checking for sprite collision, pointer from hitbox to enemy object
        self.frame = 0

    def find_target_pos(self):
        p1: Player = self.game.player_1
        p2: Player = self.game.player_2
        if p1.alive() and not p1.explosion and p2.alive() and not p2.explosion:
            return min(p1.pos, p2.pos, key=lambda x: self.pos.dist_from(x)).copy()
        elif p1.alive() and not p1.explosion:
            return p1.pos.copy()
        elif p2.alive() and not p2.explosion:
            return p2.pos.copy()
        else:
            return self.pos + PVector(0, 1)  # Shoot downwards when no player alive

    def take_damage(self, bullet):
        self.health -= bullet.damage

    def take_bomb_damage(self):
        self.health -= 15

    def update(self):
        self.frame += 1
        self.move()
        self.update_img()
        self.check_shoot()
        self.check_death()
        self.custom_action()

    def move(self):
        pass

    def update_img(self):
        pass

    def check_death(self):
        pass

    def custom_action(self):
        pass

    def check_shoot(self):
        pass

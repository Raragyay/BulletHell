# coding=utf-8
from __future__ import annotations

from itertools import cycle

import pygame

from typing import TYPE_CHECKING

from src.constants import GFX
from src.items.bullet_coin import BulletCoin

if TYPE_CHECKING:
    from src.player import Player
    from src.States.level import Level


class BombEffect(pygame.sprite.Sprite):
    def __init__(self, player: Player, game: Level):
        super().__init__(game.special_effects)
        self.game = game
        self.player = player
        self.images = cycle([GFX['bm_0'], GFX[f'bm_{player.id}']])
        self.image = next(self.images)
        self.rect = self.image.get_rect()  # No need for get_center since the bomb is 600 by 800
        self.frame = 0
        self.bomb_timer = 60

    def update(self):
        self.hurt_enemies()
        self.destroy_bullets()
        self.frame -= 1
        if self.frame % 4 == 1:
            self.image = next(self.images)
        if self.frame >= self.bomb_timer:
            self.kill()
            self.player.bomb_on = False

    def destroy_bullets(self):
        for bullet in self.game.enemy_bullets:
            BulletCoin(self.game, bullet.pos)

    def hurt_enemies(self):
        pass

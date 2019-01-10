# coding=utf-8
from __future__ import annotations
import sys
from typing import Dict, List

import pygame
from itertools import cycle

from src.components.PVector import PVector
from src.bullets.weapons import PlayerWeapon1, PlayerWeapon2
from src.constants import GFX, SCREENRECT
from src.components.tools import subsurfaces
from typing import TYPE_CHECKING

from src.special_effects.bomb_effect import BombEffect
from src.items.powerup import Powerup

if TYPE_CHECKING:
    from src.states.level import Level


class Player(pygame.sprite.Sprite):
    def __init__(self, game: Level, id: int, pos: PVector):
        super().__init__(game.players)

        self.id: int = id
        self.speed: int = 5
        self.game: Level = game
        self.score = 0
        self.lives = 3

        self.pos: PVector = pos
        self.direction: PVector = PVector(0, 0)
        self.rect: pygame.Rect = None

        self.weapon_1: bool = False
        self.weapon_2: bool = False
        self.bomb_num = 3
        self.bomb_on = False

        self.hitbox: pygame.sprite.Sprite = pygame.sprite.Sprite()

        self.image: pygame.Surface = None
        self.images: cycle = None
        self.image_frame: int = 4
        self.image_dict: Dict[str, cycle] = {}

        self.explosion = False
        self.explosion_anim: List[pygame.Surface] = []
        self.explosion_frame = 0
        self.explosion_time = 120

        self.invincible = False
        self.invincible_timer = 60

        self.weapon_level = 1
        self.bullets = pygame.sprite.Group()
        self.weapon_charge_up_time = 1000
        self.weapon_time = pygame.time.get_ticks()

        self.weapon_1 = False
        self.weapon_1_cooldown = 0
        self.weapon_2 = False

        self.init_image_dict()
        self.verify_id()
        self.init_speed()
        self.init_hitbox()

    def verify_id(self):
        assert 1 <= self.id <= 4, f"Invalid ID for player ship: {self.id}"

    def init_image_dict(self):
        def flip(surface: pygame.Surface):
            return pygame.transform.flip(surface, True, False)

        if self.id == 1:
            self.image_dict = {
                "default": cycle([GFX["cricket10"], GFX['cricket11'], GFX['cricket12'], GFX['cricket11']]),
                "left"   : cycle([GFX["cricket13"], GFX['cricket14'], GFX['cricket15'], GFX['cricket14']]),
                "right"  : cycle(
                        [flip(GFX["cricket13"]), flip(GFX['cricket14']), flip(GFX['cricket15']),
                         flip(GFX['cricket14'])])
            }
            self.explosion_anim = subsurfaces(GFX['player_explosion_1'], (0, 0), (90, 90), 10)
        elif self.id == 2:
            self.image_dict = {
                'default': cycle([GFX['cricket20'], GFX['cricket21'], GFX['cricket22'], GFX['cricket21']]),
                'left'   : cycle([GFX['cricket23'], GFX['cricket24'], GFX['cricket25'], GFX['cricket24']]),
                'right'  : cycle(
                        [flip(GFX['cricket23']), flip(GFX['cricket24']), flip(GFX['cricket25']),
                         flip(GFX['cricket24'])])
            }

            self.explosion_anim = subsurfaces(GFX['player_explosion_1'], (0, 0), (90, 90), 10)

        elif self.id == 3:
            self.image_dict = {
                'default': cycle([GFX['locust10'], GFX['locust11'], GFX['locust12'], GFX['locust11']]),
                'left'   : cycle([GFX['locust13'], GFX['locust14'], GFX['locust15'], GFX['locust14']]),
                'right'  : cycle(
                        [flip(GFX['locust13']), flip(GFX['locust14']),
                         flip(GFX['locust15']),
                         flip(GFX['locust14'])])
            }
            self.explosion_anim = subsurfaces(GFX['player_explosion_2'], (0, 0), (90, 90), 10)
        elif self.id == 4:
            self.image_dict = {
                'default': cycle([GFX['locust20'], GFX['locust21'], GFX['locust22'], GFX['locust21']]),
                'left'   : cycle([GFX['locust23'], GFX['locust24'], GFX['locust25'], GFX['locust24']]),
                'right'  : cycle(
                        [flip(GFX['locust23']), flip(GFX['locust24']),
                         flip(GFX['locust25']),
                         flip(GFX['locust24'])])
            }
            self.explosion_anim = subsurfaces(GFX['player_explosion_2'], (0, 0), (90, 90), 10)

        self.images = self.image_dict['default']
        self.image = next(self.images)
        self.rect = self.image.get_rect(center=tuple(self.pos))

    def init_speed(self):
        self.speed = 5 if self.id in {1, 2} else 6

    def init_hitbox(self):
        self.hitbox.image = pygame.Surface((8, 8))
        if self.id in {1, 2}:
            # Hitbox is 5 pixels below center
            self.hitbox.rect = self.hitbox.image.get_rect(center=(self.pos.x, self.pos.y + 5))
        else:
            # hitbox is 15 pixels above center
            self.hitbox.rect = self.hitbox.image.get_rect(center=(self.pos.x, self.pos.y - 15))

    def check_speed(self):
        if self.weapon_2:
            self.speed = 4 if self.id in {1, 2} else 5
        else:
            self.speed = 5 if self.id in {1, 2} else 6

    def fire_weapons(self):
        if self.weapon_1 and not self.weapon_1_cooldown:
            PlayerWeapon1(self)
            self.weapon_1_cooldown = 5
        elif self.weapon_1:
            self.weapon_1_cooldown -= 1
        else:
            self.weapon_1_cooldown = 0  # This is designed so that if you have fast fingers you can spam the button

        if self.weapon_2:
            PlayerWeapon2(self)

    def cycle_img(self):
        if 0 < self.direction.x <= 1:
            self.images = self.image_dict['right']
        elif -1 <= self.direction.x < 0:
            self.images = self.image_dict['left']
        else:
            self.images = self.image_dict['default']
        self.image_frame -= 1
        if self.image_frame <= 0:
            self.image_frame = 4
            self.image = next(self.images)

    def check_invincible(self):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
                self.invincible_timer = 60
            self.image = GFX['cricket'] if self.id in {1, 2} else GFX['locust']

    def move(self):
        self.pos += self.direction * self.speed
        self.rect = self.image.get_rect(center=tuple(self.pos))

        oob = self.rect.clamp(SCREENRECT)
        if oob != self.rect:  # If we have to move the rectangle to keep it within screen boundaries
            #self.direction.x = 0  # Stop moving to the side
            self.rect = oob
            self.pos = PVector.from_tuple(oob.center)

    def move_hitbox(self):
        if self.id in (1, 2):
            if 0 < self.direction.x <= 1:
                # Moving to the right, so hitbox has shifted to the right
                self.hitbox.rect.center = (self.pos.x + 4, self.pos.y + 5)
            elif -1 <= self.direction.x < 0:
                # Moving to the left, so hitbox has shifted to the left
                self.hitbox.rect.center = (self.pos.x - 4, self.pos.y + 5)
            else:
                self.hitbox.rect.center = (self.pos.x, self.pos.y + 5)
        elif self.id in (3, 4):
            if 0 < self.direction.x <= 1:
                self.hitbox.rect.center = (self.pos.x + 4, self.pos.y - 15)
            elif -1 <= self.direction.x < 0:
                self.hitbox.rect.center = (self.pos.x - 4, self.pos.y - 15)
            else:
                self.hitbox.rect.center = (self.pos.x, self.pos.y - 15)

    def keep_exploding(self):
        self.explosion_frame += 1
        if self.explosion_frame < 20:
            self.image = self.explosion_anim[self.explosion_frame // 2]
            self.rect = self.image.get_rect(center=tuple(self.pos))
        elif 20 <= self.explosion_frame < self.explosion_time:
            self.image = GFX['name0']  # Transparent blank image
        else:
            self.explosion_frame = 0
            self.lives -= 1
            self.weapon_level = 1
            Powerup(self.game, self.pos+PVector(0,-100))
            if self.lives > 0:
                self.invincible = True
                self.explosion = False
                self.pos = PVector(150, 700) if self.id in {1, 3} else PVector(450, 700)
                # Must be changed immediately otherwise Powerup will be collected next tick
                self.rect.center = tuple(self.pos)
                self.bomb_num = 3
            else:
                self.kill()

    def get_bullet_score(self):
        self.score += 10 + self.weapon_level

    def activate_bomb(self):
        if not self.bomb_on and not self.explosion and self.bomb_num >= 1:
            self.invincible = True
            self.bomb_num -= 1
            self.bomb_on = True
            BombEffect(self, self.game)

    def update(self):
        if not self.explosion:
            self.check_speed()
            self.fire_weapons()
            self.cycle_img()
            self.check_invincible()
            self.move()
            self.move_hitbox()
            # print(self.bullets)
        else:
            self.keep_exploding()
        self.bullets.update()

    def draw(self, surface):
        self.bullets.draw(surface)
        surface.blit(self.image, self.rect)

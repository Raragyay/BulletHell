# coding=utf-8
from typing import List, Dict

import pygame

from src.components.PVector import PVector
from src.player import Player
from src.states.state import State
from src.components.background import Background
from src.constants import MUSIC, MAPS
from src.enemies.enemy_dict import enemy_dict
from src.explosion.bullet_explosion import BulletExplosion


class Level(State):

    def __init__(self, level_num: int):
        super().__init__()
        self.players = pygame.sprite.Group()
        self.player_1: Player = pygame.sprite.Sprite()
        self.player_2: Player = pygame.sprite.Sprite()

        self.enemies = pygame.sprite.Group()
        self.enemy_hitboxes = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.special_effects = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.controls: Dict[str, int] = {}

        self.level_num: int = level_num
        self.background: Background = Background(self.level_num)

        self.frame = 0
        self.coins = 0

        self.enemy_spawn_dict: Dict = MAPS[f"map{level_num}"]

    def startup(self, persist: dict):

        self.players.empty()
        self.enemies.empty()
        self.enemy_hitboxes.empty()
        self.enemy_bullets.empty()
        self.special_effects.empty()
        self.items.empty()
        self.persist = persist
        self.controls = self.persist['controls']  # Guarantee will load
        self.coins = self.persist['coins']  # no need to do try except because player had to insert coins to start

        self.set_music()
        # TODO TEMP
        self.player_1 = Player(self, 1, PVector(150, 700), self.players)

        self.player_2 = Player(self, 4, PVector(450, 700), self.players)

    def update(self):
        self.frame += 1
        self.spawn_enemies()
        self.players.update()
        self.background.update()
        self.enemies.update()
        self.items.update()
        self.special_effects.update()
        self.enemy_bullets.update()
        self.collision_check()

    def draw(self, surface: pygame.Surface):

        # surface.fill((0, 0, 0))  # TODO switch to background
        self.background.draw(surface)
        [player.draw(surface) for player in self.players]
        self.enemies.draw(surface)
        self.enemy_bullets.draw(surface)
        self.items.draw(surface)
        self.special_effects.draw(surface)

    def set_music(self):
        if self.level_num == 1:
            pygame.mixer.music.load(MUSIC['01_-_speedway_0'])
        elif self.level_num == 2:
            pygame.mixer.music.load(MUSIC['02_-_chip_beach_0'])
        elif self.level_num == 3:
            pygame.mixer.music.load(MUSIC['03_-_press_any_key_to_continue_0'])
        elif self.level_num == 4:
            pygame.mixer.music.load(MUSIC['04_-_i_want_more_candy_0'])
        elif self.level_num == 5:
            pygame.mixer.music.load(MUSIC['05_-_rain_island_0'])
        # pygame.mixer.music.play(-1)

    def spawn_enemies(self):
        enemies = self.enemy_spawn_dict.get(str(self.frame))
        if enemies:
            for enemy in enemies:
                enemy_dict[enemy](self, enemies[enemy])

    def collision_check(self):
        self.bullet_hit_enemy_check()
        self.player_hit_item_check()
        self.enemy_hit_player_check()

    def bullet_hit_enemy_check(self):
        for player in self.players:
            collide_dict = pygame.sprite.groupcollide(player.bullets, self.enemy_hitboxes, True, False)
            for bullet, enemies in collide_dict.items():
                player.get_bullet_score()
                BulletExplosion(self, player.weapon_level, bullet.pos)
                for enemy in enemies:
                    enemy.body.take_damage(bullet)
                # Remove laser if it is past impact point
                if player.weapon_2:
                    for b in player.bullets:
                        if b.pos.y < bullet.pos.y:
                            b.kill()
        # if self.player_1.alive():
        #     collide_dict = pygame.sprite.groupcollide(self.player_1.bullets, self.enemy_hitboxes, True, False)
        #     for bullet, enemies in collide_dict.items():
        #         self.player_1.get_bullet_score()
        #         BulletExplosion(self, self.player_1.weapon_level, bullet.pos)
        #         for enemy in enemies:
        #             enemy.body.take_damage(bullet)
        #         # Remove laser if it is past impact point
        #         if self.player_1.weapon_2:
        #             for b in self.player_1.bullets:
        #                 if b.pos.y < bullet.pos.y:
        #                     b.kill()
        # if self.player_2.alive():
        #     collide_dict = pygame.sprite.groupcollide(self.player_2.bullets, self.enemy_hitboxes, True, False)
        #     for bullet, enemies in collide_dict.items():
        #         self.player_2.get_bullet_score()
        #         BulletExplosion(self, self.player_2.weapon_level, bullet.pos)
        #         for enemy in enemies:
        #             enemy.body.take_damage(bullet)
        #         # Remove laser if it is past impact point
        #         if self.player_2.weapon_2:
        #             for b in self.player_2.bullets:
        #                 if b.pos.y < bullet.pos.y:
        #                     b.kill()

    def player_hit_item_check(self):
        for player in self.players:
            if player.explosion:
                continue
            collide_dict = pygame.sprite.spritecollide(player, self.items, True)
            for item in collide_dict:
                item.apply_effect(player)

    def enemy_hit_player_check(self):
        for player in self.players:
            if pygame.sprite.spritecollideany(player.hitbox, self.enemy_hitboxes) or pygame.sprite.spritecollideany(
                    player.hitbox, self.enemy_bullets, collided=pygame.sprite.collide_circle):
                if not player.invincible:
                    player.explosion = True

    def event_process(self, events: List[pygame.event.Event]):
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['1p_button_a']:
                    if self.player_1.alive():  # Player 1 is actually playing
                        self.player_1.weapon_time = pygame.time.get_ticks()  # Counter for when to switch to strong
                        # weapon

                if event.key == self.controls['1p_button_b']:
                    if self.player_1.alive():
                        self.player_1.activate_bomb()

                if event.key == self.controls['2p_button_a']:
                    if self.player_2.alive():  # Player 1 is actually playing
                        self.player_2.weapon_time = pygame.time.get_ticks()  # Counter for when to switch to strong
                        # weapon

                if event.key == self.controls['2p_button_b']:
                    if self.player_2.alive():
                        self.player_2.activate_bomb()

            elif event.type == pygame.KEYUP:
                if event.key == self.controls['1p_button_a']:
                    if self.player_1.alive():
                        self.player_1.weapon_1 = False
                        self.player_1.weapon_2 = False

                if event.key == self.controls['2p_button_a']:
                    if self.player_2.alive():
                        self.player_2.weapon_1 = False
                        self.player_2.weapon_2 = False

        if self.player_1.alive():
            if keys[self.controls['1p_up']] and keys[self.controls['1p_down']]:
                self.player_1.direction.y = 0
            elif keys[self.controls['1p_up']]:
                self.player_1.direction.y = -1
            elif keys[self.controls['1p_down']]:
                self.player_1.direction.y = 1
            else:
                self.player_1.direction.y = 0

            if keys[self.controls['1p_left']] and keys[self.controls['1p_right']]:
                self.player_1.direction.x = 0
            elif keys[self.controls['1p_left']]:
                self.player_1.direction.x = -1
            elif keys[self.controls['1p_right']]:
                self.player_1.direction.x = 1
            else:
                self.player_1.direction.x = 0

            if keys[self.controls['1p_button_a']]:
                if pygame.time.get_ticks() - self.player_1.weapon_charge_up_time > self.player_1.weapon_time:
                    self.player_1.weapon_2 = True
                    self.player_1.weapon_1 = False
                else:
                    self.player_1.weapon_1 = True

        if self.player_2.alive():
            if keys[self.controls['2p_up']] and keys[self.controls['2p_down']]:
                self.player_2.direction.y = 0
            elif keys[self.controls['2p_up']]:
                self.player_2.direction.y = -1
            elif keys[self.controls['2p_down']]:
                self.player_2.direction.y = 1
            else:
                self.player_2.direction.y = 0

            if keys[self.controls['2p_left']] and keys[self.controls['2p_right']]:
                self.player_2.direction.x = 0
            elif keys[self.controls['2p_left']]:
                self.player_2.direction.x = -1
            elif keys[self.controls['2p_right']]:
                self.player_2.direction.x = 1
            else:
                self.player_2.direction.x = 0

            if keys[self.controls['2p_button_a']]:
                if pygame.time.get_ticks() - self.player_2.weapon_charge_up_time > self.player_2.weapon_time:
                    self.player_2.weapon_2 = True
                    self.player_2.weapon_1 = False
                else:
                    self.player_2.weapon_1 = True

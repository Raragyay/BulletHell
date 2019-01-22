# coding=utf-8
from random import randint
from typing import List, Dict

import pygame

from src.bullets.player_laser_bullet import PlayerLaserBullet
from src.components.PVector import PVector
from src.components.hud import Hud
from src.components.stage_transition import StageTransition
from src.enemies.enemy import Enemy
from src.player import Player
from src.states.state import State
from src.components.background import Background
from src.constants import MUSIC, MAPS, SFX
from src.enemies.enemy_dict import enemy_dict
from src.special_effects.bullet_explosion import BulletExplosion


class Level(State):
    event_block_limit = 180

    def __init__(self, level_num: int):
        super().__init__()
        self.players = pygame.sprite.Group()
        self.player_1: Player = pygame.sprite.Sprite()
        self.player_2: Player = pygame.sprite.Sprite()

        self.enemies = pygame.sprite.Group()
        self.enemy_hitboxes = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.boss: Enemy = pygame.sprite.Sprite()

        self.special_effects = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.controls: Dict[str, int] = {}
        self.event_block: bool = True  # No moving at the start

        self.level_num: int = level_num
        self.background: Background = Background(self.level_num)

        self.enemy_spawn_dict: dict = MAPS[f"map{level_num}"]

        # This is used if the player wants to join midway through the game, or if they die.
        self.player_1_choose: bool = False
        self.player_1_choose_time: int = 60 * 20  # 20 seconds to choose
        self.player_2_choose: bool = False
        self.player_2_choose_time: int = 60 * 20
        self.choice = {
            '1p': 0,
            '2p': 0}

        self.show_continue = False
        self.continue_time = 10 * 60  # 10 seconds to continue

        self.stage_transition = StageTransition(level_num)
        self.hud = Hud(self)

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
        # Player 1
        if 'player_1' in self.persist:
            self.player_1 = self.persist['player_1']
            if self.player_1.alive():  # If it's not just a base sprite
                # Reset position, hitbox and rect positions will be updated on next frame.
                self.player_1.pos = PVector(150, 700)
                self.player_1.game = self  # Make sure it's spawning bullets, etc in the right game.
                self.players.add(self.player_1)
        # If the player just instantiated a character from select screen
        elif 'choice' in self.persist and self.persist['choice']['1p']:
            self.player_1 = Player(self, self.persist['choice']['1p'], PVector(150, 700))
        else:  # Just create a raw sprite for .alive() checking
            self.player_1 = pygame.sprite.Sprite()

        # Player 2
        if 'player_2' in self.persist:
            self.player_2 = self.persist['player_2']
            if self.player_2.alive():  # If it's not just a base sprite
                # Reset position, hitbox and rect positions will be updated on next frame.
                self.player_2.pos = PVector(150, 700)
                self.player_2.game = self  # Make sure it's spawning bullets, etc in the right game.
                self.players.add(self.player_2)
        # If the player just instantiated a character from select screen
        elif 'choice' in self.persist and self.persist['choice']['2p']:
            self.player_2 = Player(self, self.persist['choice']['2p'], PVector(450, 700))
        else:  # Just create a raw sprite for .alive() checking
            self.player_2 = pygame.sprite.Sprite()

        self.set_music()

    def cleanup(self):
        persist = {
            'controls': self.controls,
            'coins'   : self.coins,
            'player_1': self.player_1,
            'player_2': self.player_2
        }
        return persist

    def update(self):
        if self.frame == self.event_block_limit:
            self.event_block = False
        self.stage_transition.update()
        self.check_continue()

        if not self.show_continue:
            # Game frames should only continue when the players are playing,
            # otherwise, enemies will all spawn, and boss will spawn as well.
            # One problem that could occur is that boss spawns when player is selecting ship, however. To remedy this,
            # To remedy this, only advance frames if there is at least one player playing.
            # This can be checked with self.players.
            if self.players:
                self.frame += 1
            # TODO check stage clear
            self.player_choose_update()
            self.background.update()
            self.spawn_enemies()  # Spawn enemies will not spawn duplicates when frame is frozen since key is deleted.
            self.players.update()
            self.enemies.update()
            self.items.update()
            self.special_effects.update()
            self.enemy_bullets.update()
            self.collision_check()
        else:
            pass
        self.hud.update()  # Always update hud to show remaining time.

    def draw(self, surface: pygame.Surface):
        self.background.draw(surface)
        # This calls the draw function instead of just blitting image at rect position.
        [player.draw(surface) for player in self.players]
        self.enemies.draw(surface)
        self.enemy_bullets.draw(surface)
        self.special_effects.draw(surface)
        self.items.draw(surface)
        self.hud.draw(surface)
        self.stage_transition.draw(surface)

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
        if self.frame % 300 == 1:
            enemy_dict[f'{randint(1,5)}'](self,PVector(randint(0,600),0))
            # enemy_dict[f'{6}'](self, PVector(randint(0, 600), 1000))
            pass
        enemies = self.enemy_spawn_dict.get(str(self.frame))
        if enemies:
            for enemy in enemies:
                enemy_dict[enemy](self, PVector.from_tuple(enemies[enemy]))
            self.enemy_spawn_dict.pop(str(self.frame))

            # This makes sure that the same enemy doesn't get spawned over and over again if the frame is frozen there.

    def collision_check(self):
        self.bullet_hit_enemy_check()
        self.player_hit_item_check()
        #self.enemy_hit_player_check() #TODO TO REMOVE GODMODE

    def bullet_hit_enemy_check(self):
        for player in self.players:
            collide_dict = pygame.sprite.groupcollide(player.bullets, self.enemy_hitboxes, True, False)
            for bullet, enemies in collide_dict.items():
                player.get_bullet_score()
                BulletExplosion(self, player.weapon_level, bullet.pos)
                for enemy in enemies:
                    enemy.body.take_damage(bullet)
                # Remove laser if it is past impact point
                if isinstance(bullet, PlayerLaserBullet):
                    # This is because homing bullets can take longer to hit something,
                    # and when they do, may cut off laser.
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

    def player_choose_update(self):
        if self.player_1_choose:
            self.player_1_choose_time -= 1
            if self.player_1_choose_time <= 0:
                self.player_1 = Player(self, self.choice['1p'], PVector(150, 700))
                self.player_1_choose = False
                self.player_1_choose_time = 20  # Redundant since keyboard input also resets choose time

        if self.player_2_choose:
            self.player_2_choose_time -= 1
            if self.player_2_choose_time <= 0:
                self.player_2 = Player(self, self.choice['2p'], PVector(450, 700))
                self.player_2_choose = False
                self.player_2_choose_time = 20  # Redundant since keyboard input also resets choose time

    def check_continue(self):
        if not self.players and self.player_1_choose == self.player_2_choose == False:
            # If everyone's dead and no one is spawning
            self.show_continue = True
            self.continue_time -= 1
            if self.continue_time <= 0:
                self.done = True
                self.next = 'GAME OVER'
        else:
            self.show_continue = False
            self.continue_time = 10 * 60

    def event_process(self, events: List[pygame.event.Event]):
        if self.event_block:
            return  # Don't take input if we are in stage transition territory
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in {self.controls['1p_coin'], self.controls['2p_coin']}:
                    SFX['coin'].play()
                    self.coins += 1

                if event.key == self.controls['1p_start']:
                    if not self.player_1.alive() and not self.player_1_choose and self.coins > 0:
                        self.coins -= 1
                        self.player_1_choose = True
                        self.choice['1p'] = 1

                if event.key == self.controls['2p_start']:
                    if not self.player_2.alive() and not self.player_2_choose and self.coins > 0:
                        self.coins -= 1
                        self.player_2_choose = True
                        self.choice['2p'] = 2

                if event.key in [self.controls[x] for x in ['1p_up', '1p_down', '1p_left', '1p_right']]:
                    if self.player_1_choose:
                        self.choice['1p'] = (self.choice['1p'] + 2) % 4  # Alternate between 1 and 3

                if event.key in [self.controls[x] for x in ['2p_up', '2p_down', '2p_left', '2p_right']]:
                    if self.player_1_choose:
                        self.choice['2p'] = self.choice['2p'] % 4 + 2  # Alternate between 2 and 4

                if event.key == self.controls['1p_button_a']:
                    if self.player_1.alive():  # Player 1 is actually playing
                        self.player_1.weapon_time = pygame.time.get_ticks()  # Counter for when to switch to strong
                        # weapon
                    if self.player_1_choose:
                        self.player_1 = Player(self, self.choice['1p'], PVector(150, 700))
                        self.player_1_choose = False
                        self.player_1_choose_time = 60 * 20

                if event.key == self.controls['1p_button_b']:
                    if self.player_1.alive():
                        self.player_1.activate_bomb()
                    if self.player_1_choose:
                        self.player_1 = Player(self, self.choice['1p'], PVector(150, 700))
                        self.player_1_choose = False
                        self.player_1_choose_time = 60 * 20

                if event.key == self.controls['2p_button_a']:
                    if self.player_2.alive():  # Player 1 is actually playing
                        self.player_2.weapon_time = pygame.time.get_ticks()  # Counter for when to switch to strong
                        # weapon
                    if self.player_2_choose:
                        self.player_2 = Player(self, self.choice['2p'], PVector(450, 700))
                        self.player_2_choose = False
                        self.player_2_choose_time = 60 * 20

                if event.key == self.controls['2p_button_b']:
                    if self.player_2.alive():
                        self.player_2.activate_bomb()
                    if self.player_2_choose:
                        self.player_2 = Player(self, self.choice['2p'], PVector(450, 700))
                        self.player_2_choose = False
                        self.player_2_choose_time = 60 * 20

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

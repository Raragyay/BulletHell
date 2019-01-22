# coding=utf-8
from itertools import cycle
from typing import List, Dict

import pygame

from src.components.PVector import PVector
from src.components.background import Background
from src.components.transition import Transition
from src.constants import GFX, WIDTH, SFX
from src.player import Player
from src.states.state import State


class Select(State):
    ship_img_start = 80
    ship_img_vert = 500
    spacing = 100

    showcase_weapon_level = 5

    def __init__(self):
        super().__init__()
        self.choice: Dict[str, int] = {
            '1p': 0,
            '2p': 0}
        self.controls: Dict[str, int] = {}

        self.player_1: Player = pygame.sprite.Sprite()
        self.player_2: Player = pygame.sprite.Sprite()
        self.players = pygame.sprite.Group()

        self.player_1_confirm = False
        self.player_2_confirm = False
        self.next = 'LEVEL 1'
        self.time_left = 20

        self.p1_ship_img: cycle = None  # Selecting between the two
        self.p2_ship_img: cycle = None
        self.p1_star_img: cycle = None
        self.p2_star_img: cycle = None
        self.p1_name_img: cycle = None
        self.p2_name_img: cycle = None
        self.p1_ship_img_rects: cycle = None
        self.p2_ship_img_rects: cycle = None
        self.p1_ship_sprites: cycle = None
        self.p2_ship_sprites: cycle = None

        self.p1_power_image: pygame.Surface = None
        self.p1_power_rect: pygame.Rect = None
        self.p1_speed_image: pygame.Surface = None
        self.p1_speed_rect: pygame.Rect = None
        self.p1_name_image: pygame.Surface = None
        self.p1_name_rect: pygame.Rect = None

        self.p2_power_image: pygame.Surface = None
        self.p2_power_rect: pygame.Rect = None
        self.p2_speed_image: pygame.Surface = None
        self.p2_speed_rect: pygame.Rect = None
        self.p2_name_image: pygame.Surface = None
        self.p2_name_rect: pygame.Rect = None

        self.p1_ship_image: pygame.Surface = None
        self.p1_ship_rect: pygame.Rect = None
        self.p2_ship_image: pygame.Surface = None
        self.p2_ship_rect: pygame.Rect = None

        self.mask: pygame.Surface = None

        self.background = Background(3)
        self.transition = Transition()

        self.load_images()

    def load_images(self):
        g = lambda key: GFX[key]
        r = lambda x, y: pygame.Rect(x, y, 70, 105)
        self.p1_ship_img = cycle((g('p1_1'), g('p1_2')))
        self.p2_ship_img = cycle((g('p2_1'), g('p2_2')))
        self.p1_star_img = cycle((g('star_r_1'), g('star_r_2')))
        self.p2_star_img = cycle((g('star_b_1'), g('star_b_2')))
        self.p1_name_img = cycle((g('name_r_1'), g('name_r_2')))
        self.p2_name_img = cycle((g('name_b_1'), g('name_b_2')))

        self.p1_ship_img_rects = cycle((r(150 - 75 - 35, 470 + 45 - 52.5), r(150 + 75 - 35, 470 + 45 - 52.5)))
        # 150 is ship middle,75 offset for ship center, 35 offset for left side.
        # 470 is small ship top, 45 offset for ship center, 52.5 offset for top side
        self.p2_ship_img_rects = cycle((r(450 - 75 - 35, 470 + 45 - 52.5), r(450 + 75 - 35, 470 + 45 - 52.5)))

        def p(id, x_pos):
            p = Player(self, id, PVector(x_pos, 400))
            p.kill()  # To avoid drawing multiple ships on top of each other, should kill when they are not active
            p.weapon_level = self.showcase_weapon_level
            return p

        self.p1_ship_sprites = cycle((p(1, 150), p(3, 150)))
        self.p2_ship_sprites = cycle((p(2, 450), p(4, 450)))

        # Player centerx for p1 is 150.
        # This means that centerx for name should also be 150.
        # So the left of name is 150-70/2=115
        # Similar logic for power and speed

        self.p1_power_image = g('star_r_0')  # ????? picture
        self.p1_power_rect = pygame.Rect(102, 670, 97, 17)
        self.p1_speed_image = g('star_r_0')  # ????? picture
        self.p1_speed_rect = pygame.Rect(102, 730, 97, 17)
        self.p1_name_image = g('name_blank')
        self.p1_name_rect = pygame.Rect(115, 580, 70, 60)

        self.p2_power_image = g('star_b_0')  # ????? picture
        self.p2_power_rect = pygame.Rect(402, 670, 97, 17)
        self.p2_speed_image = g('star_b_0')  # ????? picture
        self.p2_speed_rect = pygame.Rect(402, 730, 97, 17)
        self.p2_name_image = g('name_blank')
        self.p2_name_rect = pygame.Rect(415, 580, 70, 60)

        self.mask = g('player_select_gimp')

    def startup(self, persist: dict):
        # Reset p1_ship_images since they haven't indicated they want to play yet
        self.p1_ship_image: pygame.Surface = None
        self.p1_ship_rect: pygame.Rect = None
        self.p2_ship_image: pygame.Surface = None
        self.p2_ship_rect: pygame.Rect = None

        self.persist = persist
        self.choice = self.persist['choice']  # This denotes which player chose to start the game
        self.controls = self.persist['controls']
        self.coins = self.persist['coins']
        # Should always be done after controls initialized in "level" state where player actually starts giving input

    def cleanup(self):
        persist = {
            'coins'   : self.coins,
            'controls': self.controls,
            'choice'  : self.choice
        }
        return persist

    def update(self):
        self.transition.fade_in()
        self.fade_away = self.check_done()
        if self.fade_away:
            self.done = self.transition.fade_out()
        self.frame += 1
        self.update_time()
        self.players.update()
        self.background.update()

    def draw(self, surface):
        self.background.draw(surface)
        self.players.draw(surface)
        surface.blit(self.mask, (0, 0))
        if self.p1_ship_image:  # Image only gets initialized when player has indicated they want to play
            surface.blit(self.p1_ship_image, self.p1_ship_rect)
        surface.blit(self.p1_power_image, self.p1_power_rect)
        surface.blit(self.p1_speed_image, self.p1_speed_rect)
        surface.blit(self.p1_name_image, self.p1_name_rect)

        if self.p2_ship_image:  # Image only gets initialized when player has indicated they want to play
            surface.blit(self.p2_ship_image, self.p2_ship_rect)
        surface.blit(self.p2_power_image, self.p2_power_rect)
        surface.blit(self.p2_speed_image, self.p2_speed_rect)
        surface.blit(self.p2_name_image, self.p2_name_rect)

        self.transition.draw(surface)

    def set_player_1(self):
        self.player_1.kill()  # Kill then add because we want to remove the ship that is to be switched out. 
        self.player_1 = next(self.p1_ship_sprites)
        self.players.add(self.player_1)
        self.choice['1p'] = self.player_1.id
        self.p1_ship_image = next(self.p1_ship_img)
        self.p1_ship_rect = next(self.p1_ship_img_rects)
        self.p1_power_image = next(self.p1_star_img)
        self.p1_speed_image = next(self.p1_star_img)
        next(self.p1_star_img)  # This is so that the power and speed images alternate 5,4 -> 4,5 -> 5,4
        self.p1_name_image = next(self.p1_name_img)

    def set_player_2(self):
        self.player_2.kill()
        self.player_2 = next(self.p2_ship_sprites)
        self.players.add(self.player_2)
        self.choice['2p'] = self.player_2.id
        self.p2_ship_image = next(self.p2_ship_img)
        self.p2_ship_rect = next(self.p2_ship_img_rects)
        self.p2_power_image = next(self.p2_star_img)
        self.p2_speed_image = next(self.p2_star_img)
        next(self.p2_star_img)  # This is so that the power and speed images alternate 5,4 -> 4,5 -> 5,4
        self.p2_name_image = next(self.p2_name_img)

    def update_time(self):
        if self.frame % 60 == 0:
            self.time_left -= 1

    def check_done(self):
        if self.time_left <= 0:
            return True
        if not self.player_2.alive() and self.player_1_confirm:
            return True
        if not self.player_1.alive() and self.player_2_confirm:
            return True
        if self.player_1.alive() and self.player_2.alive() and self.player_1_confirm and self.player_2_confirm:
            return True
        return False

    def event_process(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in {self.controls['1p_coin'], self.controls['2p_coin']}:
                    SFX['coin'].play()
                    self.coins += 1

                if event.key == self.controls['1p_start']:
                    if not self.player_1.alive() and self.coins >= 1:
                        self.coins -= 1
                        self.time_left = 20
                        self.set_player_1()

                if event.key == self.controls['2p_start']:
                    if not self.player_2.alive() and self.coins >= 1:
                        self.coins -= 1
                        self.time_left = 20
                        self.set_player_2()

                if event.key in [self.controls[x] for x in {'1p_up', '1p_down', '1p_left', '1p_right'}]:
                    if self.player_1.alive() and not self.player_1_confirm:
                        self.set_player_1()
                        SFX['hint'].play()

                if event.key in [self.controls[x] for x in {'2p_up', '2p_down', '2p_left', '2p_right'}]:
                    if self.player_2.alive() and not self.player_2_confirm:
                        self.set_player_2()
                        SFX['hint'].play()

                if event.key in {self.controls['1p_button_a'], self.controls['1p_button_b']}:
                    if self.player_1.alive() and not self.player_1_confirm:
                        self.player_1_confirm = True
                        self.p1_ship_image = None  # Reset image, so that it is not drawn
                        
                if event.key in {self.controls['2p_button_a'], self.controls['2p_button_b']}:
                    if self.player_2.alive() and not self.player_2_confirm:
                        self.player_2_confirm = True
                        self.p2_ship_image = None  # Reset image, so that it is not drawn

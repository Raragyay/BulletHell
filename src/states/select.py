# coding=utf-8
from itertools import cycle
from typing import List, Dict

import pygame

from src.components.PVector import PVector
from src.components.background import Background
from src.components.transition import Transition
from src.constants import GFX, WIDTH
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

        self.background=Background(3)
        self.transition=Transition()

        self.load_images()

    def load_images(self):
        g = lambda key: GFX[key]

        self.p1_ship_img = cycle((g('p1_1'), g('p1_2')))
        self.p2_ship_img = cycle((g('p2_1'), g('p2_2')))
        self.p1_star_img = cycle((g('star_r_1'), g('star_r_2')))
        self.p2_star_img = cycle((g('star_b_1'), g('star_b_2')))
        self.p1_name_img = cycle((g('name_r_1'), g('name_r_2')))
        self.p2_name_img = cycle((g('name_b_1'), g('name_b_2')))
        self.p1_ship_img_rects = cycle((g('p1_1').get_rect(center=(self.ship_img_start, self.ship_img_vert)),
                                        g('p1_2').get_rect(
                                            center=(self.ship_img_start + self.spacing, self.ship_img_vert))))
        self.p2_ship_img_rects = cycle((g('p1_1').get_rect(center=(WIDTH - self.ship_img_start, self.ship_img_vert)),
                                        g('p1_2').get_rect(
                                            center=(WIDTH - self.ship_img_start - self.spacing, self.ship_img_vert))))

        def p(id, x_pos):
            p = Player(self, id, PVector(x_pos, 400))
            p.kill()  # To avoid drawing multiple ships on top of each other, should kill when they are not active
            p.weapon_level = self.showcase_weapon_level
            return p

        self.p1_ship_sprites = cycle((p(1, 150), p(3, 150)))
        self.p2_ship_sprites = cycle((p(2, 450), p(4, 150)))

    def startup(self, persist: dict):
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
        self.frame += 1
        self.update_time()
        self.players.update()
        self.background.update()

    def draw(self, surface):
        self.background.draw(surface)
        self.players.draw(surface)
        self.transition.draw(surface)

    def set_player_1(self):
        self.player_1.kill()
        self.player_1 = next(self.p1_ship_sprites)
        self.players.add(self.player_1)
        self.choice['1p'] = self.player_1.id

    def event_process(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls['1p_start']:
                    self.set_player_1()

    def update_time(self):
        if self.frame % 60 == 0:
            self.time_left -= 1

# coding=utf-8
from typing import List, Dict

import pygame

from src.player import Player
from src.states.state import State


class Select(State):
    def __init__(self):
        super().__init__()
        self.choice: Dict[str, int] = {}
        self.controls: Dict[str, int] = {}

        self.player_1: Player = pygame.sprite.Sprite()
        self.player_2: Player = pygame.sprite.Sprite()
        self.players = pygame.sprite.Group()
        self.next = 'LEVEL 1'
        self.time_left = 20

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
            'choice'  : self.choice}
        return persist

    def update(self):
        self.frame += 1
        self.update_time()


    def draw(self, surface):
        pass

    def event_process(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass

    def update_time(self):
        if self.frame % 60 == 0:
            self.time_left -= 1

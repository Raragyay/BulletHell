# coding=utf-8
from typing import Dict, List

import pygame

from src.states.state import State


class StateMachine:
    def __init__(self):
        self.state: State = None
        self.state_dict: Dict[str, State] = {}
        self.quit: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.fps = 60
        self.screen = pygame.display.get_surface()

    def init_states(self, state_dict: Dict[str, State], start_state: str):
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        self.state.startup({})

    def check_quit(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit = True

    def update(self):
        if self.state.quit:
            self.quit = True
        elif self.state.done:
            self.next_state()
        self.state.update()
        self.state.draw(self.screen)

    def next_state(self):
        persist = self.state.cleanup()
        # print(persist)
        next_state_name = self.state.next
        self.state = self.state_dict[next_state_name]
        self.state.startup(persist)

    def main(self):

        while not self.quit:
            self.clock.tick(self.fps)
            events = pygame.event.get()
            self.check_quit(events)
            self.state.event_process(events)

            self.update()
            pygame.display.flip()

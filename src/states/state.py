# coding=utf-8
from typing import List

import pygame


class State:
    """
    Base state class for all game states. Should not be created directly.

    A main loop for the state consists of two parts: event_process and update.
    Event process makes changes based on player input
    Update "ticks" a game state
    """

    def __init__(self):
        # Indicates if that "section" of the game has been completed.
        # When done, move on to next state, determined by self.next
        self.done: bool = False

        # Indicates the next state that should be created.
        # For instance, the next state of the first level might be the second level.
        self.next: str = None

        # Indicates if the user wants to quit the game.
        self.quit: bool = False

        # Any information carried on from the previous state. For example, the player's health.
        self.persist: dict = {}

    def startup(self, persist: dict):
        self.persist = persist

    def draw(self, surface):
        raise NotImplementedError("Do not create raw base class objects. ")

    def event_process(self, events: List[pygame.event.Event]):
        raise NotImplementedError("Do not create raw base class objects. ")

    def update(self):
        raise NotImplementedError("Do not create raw base class objects. ")

    def cleanup(self):
        return self.persist

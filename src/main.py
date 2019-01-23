# coding=utf-8
import sys

import pygame

from src import constants
from src.states.control import Control
from src.states.disclaimer import Disclaimer
from src.states.highscore import Highscore
from src.states.level import Level
from src.state_machine import StateMachine
from src.states.select import Select
from src.states.title import Title


def main():
    state_machine = StateMachine()
    states = {
        'DISCLAIMER': Disclaimer(),
        'TITLE'     : Title(),
        'CONTROL'   : Control(),
        'SELECT'    : Select(),
        'LEVEL 1'   : Level(1),
        'HIGHSCORE' : Highscore(),
    }
    state_machine.init_states(states, 'DISCLAIMER')
    # print('hi')
    state_machine.main()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

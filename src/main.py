# coding=utf-8
import sys

import pygame

from src import constants
from src.states.disclaimer import Disclaimer
from src.states.level import Level
from src.state_machine import StateMachine


def main():
    state_machine = StateMachine()
    states = {
        'DISCLAIMER': Disclaimer(),
        'LEVEL 1'   : Level(1)
    }
    state_machine.init_states(states, 'DISCLAIMER')
    # print('hi')
    state_machine.main()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

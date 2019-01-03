from unittest import TestCase

from src.components.PVector import PVector
from src.enemies.enemy import Enemy


class TestEnemy(TestCase):
    def test_find_target_pos(self):
        class Player:
            def __init__(self, pos):
                self.pos = pos

            def alive(self):
                return True

        class Game:
            def __init__(self, pos1, pos2):
                self.player_1 = Player(pos1)
                self.player_2 = Player(pos2)
                self.enemies = []
                self.enemy_hitboxes = []

        g = Game(PVector(150, 700), PVector(450, 700))
        e = Enemy(g, [600, 0])
        assert e.find_target_pos() == g.player_2.pos

from unittest import TestCase

from src.components.PVector import PVector


class TestPVector(TestCase):
    def test_dist_to(self):
        a = PVector(600, 0)
        b = PVector(150, 700)
        c = PVector(450, 700)
        assert a.dist_from(b) > a.dist_from(c)

    def test_tuple(self):
        a=PVector(1,2)
        assert a[0]==1
        assert a[1]==2

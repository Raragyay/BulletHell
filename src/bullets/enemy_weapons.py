# coding=utf-8
from src.bullets.second_lieutenant_bullet import SecondLieutenantBullet
from src.bullets.sergeant_bullet import SergeantBullet
from src.components.PVector import PVector


class SergeantWeapon0:
    def __init__(self, enemy, pos, target):
        SergeantBullet(-60, target, enemy.game, pos)
        SergeantBullet(-40, target, enemy.game, pos)
        SergeantBullet(-20, target, enemy.game, pos)
        SergeantBullet(20, target, enemy.game, pos)
        SergeantBullet(40, target, enemy.game, pos)
        SergeantBullet(60, target, enemy.game, pos)


class SergeantWeapon1:
    def __init__(self, enemy, pos, target):
        SergeantBullet(-60, target, enemy.game, pos)
        SergeantBullet(-30, target, enemy.game, pos)
        SergeantBullet(0, target, enemy.game, pos)
        SergeantBullet(30, target, enemy.game, pos)
        SergeantBullet(60, target, enemy.game, pos)


class SecondLieutenantWeapon0:
    def __init__(self, enemy, pos):
        SecondLieutenantBullet(enemy.game, pos + PVector(-43, 90), 180)
        SecondLieutenantBullet(enemy.game, pos + PVector(-43, 30), 180)
        SecondLieutenantBullet(enemy.game, pos + PVector(-43, -40), 180)
        SecondLieutenantBullet(enemy.game, pos + PVector(43, 90), 0)
        SecondLieutenantBullet(enemy.game, pos + PVector(43, 30), 0)
        SecondLieutenantBullet(enemy.game, pos + PVector(43, -40), 0)


class SecondLieutenantWeapon1:
    firing_angles = (0, 72, 72*2, 72*3, 72*4)  # Kind of like a rotating star

    def __init__(self, enemy, pos):
        for i in range(5):
            SecondLieutenantBullet(enemy.game, pos + PVector(0, enemy.firing_positions[i]),
                                   enemy.frame + self.firing_angles[i], 15)

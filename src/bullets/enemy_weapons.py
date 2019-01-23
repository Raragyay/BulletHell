# coding=utf-8
from src.bullets.boss_bullet_2 import BossBullet2
from src.bullets.colonel_bullet_0 import ColonelBullet0
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
    firing_angles = (0, 72, 72 * 2, 72 * 3, 72 * 4)  # Kind of like a rotating star

    def __init__(self, enemy, pos):
        for i in range(5):
            SecondLieutenantBullet(enemy.game, pos + PVector(0, enemy.firing_positions[i]),
                                   enemy.frame + self.firing_angles[i], 15)


class Boss1Pattern1:
    def __init__(self, enemy, pos):
        for i in range(0, 360, 20):
            BossBullet2(enemy.game, pos, i)


class Boss1Pattern2:
    def __init__(self, enemy, pos):  # Back and forth in all directions
        BossBullet2(enemy.game, pos, enemy.frame * 8)
        BossBullet2(enemy.game, pos, -enemy.frame * 8)


class ColonelWeapon1:
    def __init__(self, enemy, pos, type):
        if type == 1:
            ColonelBullet0(enemy.game, pos, 30, -90)

        if type == 2:
            ColonelBullet0(enemy.game, pos, 28, -85)
            ColonelBullet0(enemy.game, pos, 28, -95)

        if type == 3:
            ColonelBullet0(enemy.game, pos, 26, -80)
            ColonelBullet0(enemy.game, pos, 26, -90)
            ColonelBullet0(enemy.game, pos, 26, -100)

        if type == 4:
            ColonelBullet0(enemy.game, pos, 24, -75)
            ColonelBullet0(enemy.game, pos, 24, -85)
            ColonelBullet0(enemy.game, pos, 24, -95)
            ColonelBullet0(enemy.game, pos, 24, -105)

        if type == 5:
            ColonelBullet0(enemy.game, pos, 22, -70)
            ColonelBullet0(enemy.game, pos, 22, -80)
            ColonelBullet0(enemy.game, pos, 22, -90)
            ColonelBullet0(enemy.game, pos, 22, -100)
            ColonelBullet0(enemy.game, pos, 22, -110)
        if type == 6:
            ColonelBullet0(enemy.game, pos, 20, -65)
            ColonelBullet0(enemy.game, pos, 20, -75)
            ColonelBullet0(enemy.game, pos, 20, -85)
            ColonelBullet0(enemy.game, pos, 20, -95)
            ColonelBullet0(enemy.game, pos, 20, -105)
            ColonelBullet0(enemy.game, pos, 20, -115)
        if type == 1:
            ColonelBullet0(enemy.game, pos, 18, -60)
            ColonelBullet0(enemy.game, pos, 18, -70)
            ColonelBullet0(enemy.game, pos, 18, -80)
            ColonelBullet0(enemy.game, pos, 18, -90)
            ColonelBullet0(enemy.game, pos, 18, -100)
            ColonelBullet0(enemy.game, pos, 18, -110)
            ColonelBullet0(enemy.game, pos, 18, -120)

class ColonelWeapon2:
    def __init__(self, enemy, pos, type):
        if type == 1:
            ColonelBullet0(enemy.game, pos, 30, -90,5)

        if type == 2:
            ColonelBullet0(enemy.game, pos, 28, -85,5/1.1)
            ColonelBullet0(enemy.game, pos, 28, -95,5/1.1)

        if type == 3:
            ColonelBullet0(enemy.game, pos, 26, -80,5/1.3)
            ColonelBullet0(enemy.game, pos, 26, -90,5/1.3)
            ColonelBullet0(enemy.game, pos, 26, -100,5/1.3)

        if type == 4:
            ColonelBullet0(enemy.game, pos, 24, -75,5/1.4)
            ColonelBullet0(enemy.game, pos, 24, -85,5/1.4)
            ColonelBullet0(enemy.game, pos, 24, -95,5/1.4)
            ColonelBullet0(enemy.game, pos, 24, -105,5/1.4)

        if type == 5:
            ColonelBullet0(enemy.game, pos, 22, -70,5/1.5)
            ColonelBullet0(enemy.game, pos, 22, -80,5/1.5)
            ColonelBullet0(enemy.game, pos, 22, -90,5/1.5)
            ColonelBullet0(enemy.game, pos, 22, -100,5/1.5)
            ColonelBullet0(enemy.game, pos, 22, -110,5/1.5)
        if type == 6:
            ColonelBullet0(enemy.game, pos, 20, -65,5/1.6)
            ColonelBullet0(enemy.game, pos, 20, -75,5/1.6)
            ColonelBullet0(enemy.game, pos, 20, -85,5/1.6)
            ColonelBullet0(enemy.game, pos, 20, -95,5/1.6)
            ColonelBullet0(enemy.game, pos, 20, -105,5/1.6)
            ColonelBullet0(enemy.game, pos, 20, -115,5/1.6)
        if type == 1:
            ColonelBullet0(enemy.game, pos, 18, -60,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -70,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -80,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -90,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -100,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -110,5/1.7)
            ColonelBullet0(enemy.game, pos, 18, -120,5/1.7)

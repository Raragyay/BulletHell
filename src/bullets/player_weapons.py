# coding=utf-8
from src.bullets.player_homing_bullet import PlayerHomingBullet
from src.components.PVector import PVector
from src.bullets.player_bullet import PlayerBullet
from src.bullets.player_laser_bullet import PlayerLaserBullet

front_weapon = PVector(9, 0)
back_weapon = PVector(24, 0)
back_offset = PVector(0, 20)


class PlayerWeapon1:
    def __init__(self, player):
        p = player
        level = p.weapon_level
        if level == 1:  # TODO Add more levels
            PlayerBullet(p, 90, front_weapon, 1)
            PlayerBullet(p, 90, -front_weapon, 1)
        elif level == 2:
            PlayerBullet(p, 90, front_weapon, 1)
            PlayerBullet(p, 90, -front_weapon, 1)
            PlayerBullet(p, 90, back_weapon + back_offset, 1)
            PlayerBullet(p, 90, -back_weapon + back_offset, 1)
        elif level == 3:
            PlayerBullet(p, 80, front_weapon, 1)
            PlayerBullet(p, 100, front_weapon, 1)
            PlayerBullet(p, 80, -front_weapon, 1)
            PlayerBullet(p, 100, -front_weapon, 1)
            PlayerBullet(p, 90, back_weapon + back_offset, 1)
            PlayerBullet(p, 90, -back_weapon + back_offset, 1)
        elif level == 4:
            PlayerBullet(p, 80, front_weapon, 1)
            PlayerBullet(p, 100, front_weapon, 1)
            PlayerBullet(p, 80, -front_weapon, 1)
            PlayerBullet(p, 100, -front_weapon, 1)
            PlayerBullet(p, 90, back_weapon + back_offset, 2)
            PlayerBullet(p, 90, -back_weapon + back_offset, 2)
            HomingWeapon1(p)
        elif level == 5:
            PlayerBullet(p, 75, front_weapon, 1)
            PlayerBullet(p, 90, front_weapon, 2)
            PlayerBullet(p, 105, front_weapon, 1)
            PlayerBullet(p, 75, -front_weapon, 1)
            PlayerBullet(p, 90, -front_weapon, 2)
            PlayerBullet(p, 105, -front_weapon, 1)
            PlayerBullet(p, 90, back_weapon + back_offset, 2)
            PlayerBullet(p, 90, -back_weapon + back_offset, 2)
            HomingWeapon1(p)
        elif level == 6:
            PlayerBullet(p, 70, front_weapon, 1)
            PlayerBullet(p, 80, front_weapon, 1)
            PlayerBullet(p, 90, front_weapon, 2)
            PlayerBullet(p, 100, front_weapon, 1)
            PlayerBullet(p, 110, front_weapon, 1)
            PlayerBullet(p, 70, -front_weapon, 1)
            PlayerBullet(p, 80, -front_weapon, 1)
            PlayerBullet(p, 90, -front_weapon, 2)
            PlayerBullet(p, 100, -front_weapon, 1)
            PlayerBullet(p, 110, -front_weapon, 1)
            PlayerBullet(p, 90, back_weapon + back_offset, 2)
            PlayerBullet(p, 90, -back_weapon + back_offset, 2)
            HomingWeapon2(p)
        elif level==7:
            PlayerBullet(p, 70, front_weapon, 2)
            PlayerBullet(p, 80, front_weapon, 1)
            PlayerBullet(p, 90, front_weapon, 2)
            PlayerBullet(p, 100, front_weapon, 1)
            PlayerBullet(p, 110, front_weapon, 2)
            PlayerBullet(p, 70, -front_weapon, 2)
            PlayerBullet(p, 80, -front_weapon, 1)
            PlayerBullet(p, 90, -front_weapon, 2)
            PlayerBullet(p, 100, -front_weapon, 1)
            PlayerBullet(p, 110, -front_weapon, 2)
            PlayerBullet(p, 90, back_weapon + back_offset, 3)
            PlayerBullet(p, 90, -back_weapon + back_offset, 3)
            HomingWeapon2(p)


class HomingWeapon:
    cooldown = 4

    def __init__(self, player):
        HomingWeapon.cooldown -= 1
        if HomingWeapon.cooldown <= 0:
            self.fire(player)
            HomingWeapon.cooldown = 4

    def fire(self, player):
        raise NotImplementedError("Do not create a raw homing weapon")


class HomingWeapon1(HomingWeapon):
    def __init__(self, player):
        super().__init__(player)

    def fire(self, player):
        PlayerHomingBullet(player, back_weapon + back_offset, 2)
        PlayerHomingBullet(player, -back_weapon + back_offset, 2)


class HomingWeapon2(HomingWeapon):
    def __init__(self, player):
        super().__init__(player)

    def fire(self, player):
        PlayerHomingBullet(player, back_weapon + back_offset, 3)
        PlayerHomingBullet(player, -back_weapon + back_offset, 3)

class PlayerWeapon2:
    def __init__(self, player):
        PlayerLaserBullet(player)

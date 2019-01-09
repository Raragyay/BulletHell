# coding=utf-8
import pygame

from src.components.PVector import PVector


class Enemy(pygame.sprite.Sprite):
    """
    Base enemy class.
    """

    def __init__(self, game, pos):
        super().__init__(game.enemies)
        self.tag = 'enemy'
        self.health = 0
        self.speed = 0
        self.game = game
        self.pos:PVector = pos  # It's a list, but still an iterable
        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.hitbox: pygame.sprite.Sprite = pygame.sprite.Sprite(game.enemy_hitboxes)
        self.hitbox.body = self  # When checking for sprite collision, pointer from hitbox to enemy object
        self.frame = 0

    def find_target_pos(self):
        p1 = self.game.player_1
        p2 = self.game.player_2
        if p1.alive() and p2.alive():
            return min(p1.pos, p2.pos, key=lambda x: self.pos.dist_from(x))
        elif p1.alive():
            return p1.pos
        elif p2.alive():
            return p2.pos
        else:
            return self.pos

    def take_damage(self, bullet):
        self.health -= bullet.damage

    def take_bomb_damage(self):
        self.health -= 15

    def update(self):
        self.frame += 1
        self.move()
        self.update_img()
        self.check_shoot()
        self.check_death()
        self.custom_action()

    def move(self):
        pass

    def update_img(self):
        pass

    def check_death(self):
        pass

    def custom_action(self):
        pass

    def check_shoot(self):
        pass

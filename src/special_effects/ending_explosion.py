import pygame


class EndingExplosion(pygame.sprite.Sprite):
    def __init__(self, game):
        super(EndingExplosion, self).__init__(game.special_effects)
        self.game = game
        self.image = pygame.Surface((600, 800), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.frame = 0

    def update(self):
        self.frame += 1
        if self.frame >= 254:
            self.game.stage_clear = True
            self.kill()
        self.image.fill((255, 255, 255, self.frame))

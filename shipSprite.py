import pygame, os
from pygame.locals import *

class ShipSprite(pygame.sprite.Sprite):
    
    def __init__(self):
        """ Init the Ship Sprite """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ship.png')
        self.image.convert()
        self.rect = self.image.get_rect()

    def keypress(self, key):
        if key == K_DOWN:
            self.rect.move_ip(0, 1)
        elif key == K_UP:
            self.rect.move_ip(0, -1)
        elif key == K_LEFT:
            self.image= pygame.transform.rotate(self.image, 0.5)
            self.rect.move_ip(-1, 0)
            self.rect = self.image.get_rect()
        elif key == K_RIGHT:
            self.image= pygame.transform.rotate(self.image, -0.5)
            self.rect.move_ip(1, 0)
            self.rect = self.image.get_rect()

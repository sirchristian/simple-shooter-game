import os
import random
import pygame
from pygame.locals import *

class BadGuySprite(pygame.sprite.Sprite):
    
    def __init__(self, gameSurface):
        """ Init a bad guy """
        pygame.sprite.Sprite.__init__(self)
        badGuyImages = os.listdir('badguysprites')
        badGuyToUse = random.randint(1, len(badGuyImages))
        self.image = pygame.image.load(
                os.path.join('badguysprites', badGuyImages[badGuyToUse-1]))
        self.image.convert()
        self.rect = self.image.get_rect()


    def update(self):
        """ Handles the update call.
            - moves around the screen"""
        self.rect.move_ip(random.randint(2, 5), random.randint(2, 5))

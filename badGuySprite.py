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
        self.surface = gameSurface
        self.gameRect = self.surface.get_rect()
        self.h_direction = random.randint(0,1)
        if self.h_direction == 0:
            self.h_direction = -1
        self.v_direction = random.randint(0,1)
        if self.v_direction == 0:
            self.v_direction = -1


    def update(self):
        """ Handles the update call.
            - moves around the screen"""
        if self.rect.left < self.gameRect.left or self.rect.right > self.gameRect.right:
            self.h_direction = -self.h_direction
        if self.rect.top < self.gameRect.top:
            self.v_direction = -self.v_direction

        # we can be removed if we exit the bottom of the screen
        if self.rect.top > self.gameRect.bottom:
            return False
        
        self.rect.move_ip(self.h_direction, self.v_direction)
        return True

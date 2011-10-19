import pygame
import datetime
from pygame.locals import *

class ShipSprite(pygame.sprite.Sprite):
    
    def __init__(self, gameSurface):
        """ Init the Ship Sprite """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ship.png')
        self.image.convert()
        self.rect = self.image.get_rect()
        self.surface = gameSurface
        self.gameRect = self.surface.get_rect()
        self.bullets = []
        self.lastFire = datetime.datetime.now()

    def keypress(self, key):
        """ Handles the keypress events """
        # we don't want all key events all the time so keep track
        # of the datetime.  
        now = datetime.datetime.now()

        if key == K_LEFT and self.rect.left > self.gameRect.left:
            self.rect.move_ip(-1, 0)
        elif key == K_RIGHT and self.rect.right < self.gameRect.right:
            self.rect.move_ip(1, 0)
        elif key == K_SPACE and (now - self.lastFire).total_seconds() >= 0.25:
            self._fire(now)

    def _fire(self, now):
        """ Fires a bullet """
        bullet = pygame.image.load('bullet.png')
        bullet_rect = bullet.get_rect()
        bullet_rect = bullet_rect.move(self.rect.centerx, self.rect.top)
        self.bullets.append((bullet, bullet_rect))
        self.lastFire = now

    def update(self):
        for bullet,bullet_rect in self.bullets:
            bullet_rect.move_ip(0, -1)
            self.surface.blit(bullet, bullet_rect)

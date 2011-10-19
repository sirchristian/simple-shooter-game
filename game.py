import pygame
import sys
from pygame.locals import *

import shipSprite
from shipSprite import ShipSprite

# setup the game
pygame.init()
gameSurface = pygame.display.set_mode((640,480))
pygame.display.set_caption('Fun game')
pygame.key.set_repeat(1, 1)

#Create The Backgound
background = pygame.Surface(gameSurface.get_size())
background = background.convert()
background.fill((250, 250, 250))

#Display The Background
gameSurface.blit(background, (0, 0))
pygame.display.flip()

# setup the sprites
ship = ShipSprite(background)
ship.rect = ship.rect.move(0, gameSurface.get_height()-ship.rect.height)
allsprites = pygame.sprite.RenderPlain((ship,))

# game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            ship.keypress(event.key)
    
    # update UI
    gameSurface.blit(background, (0, 0))
    ship.update()
    allsprites.draw(gameSurface)
    pygame.display.update()

import random
import sys
import pygame
from pygame.locals import *

import shipSprite
from shipSprite import ShipSprite

import badGuySprite
from badGuySprite import BadGuySprite

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

# setup the ship
ship = ShipSprite(gameSurface)
ship.rect = ship.rect.move(0, gameSurface.get_height()-ship.rect.height)
sprites = [ship,]

def CreateBadGuy():
    badGuy = BadGuySprite(gameSurface)
    badGuy.rect = badGuy.rect.move(
        random.randint(0, gameSurface.get_width()),
        random.randint(20, gameSurface.get_height()))
    baddies.append(badGuy)
    sprites.append(badGuy)
        
# setup the baddies
numBaddies = 2
baddies = []
for baddie in range(numBaddies):
    CreateBadGuy()

allsprites = pygame.sprite.RenderPlain(sprites)

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
    for baddie in baddies[:]:
        if baddie.update() == False:
            baddies.remove(baddie)
            CreateBadGuy()
            allsprites = pygame.sprite.RenderPlain(sprites)
    allsprites.draw(gameSurface)
    pygame.display.flip()

import random
import sys
import pygame
import pygame._view # needed to turn to an exe
from pygame.locals import *

import shipSprite
from shipSprite import ShipSprite

import badGuySprite
from badGuySprite import BadGuySprite

def CreateBadGuy():
    badGuy = BadGuySprite(gameSurface)
    badGuy.rect = badGuy.rect.move(
        random.randint(0, gameSurface.get_width()),
        random.randint(20, gameSurface.get_height()))
    baddies.append(badGuy)
    sprites.append(badGuy)

def doRectsOverlap(rect1, rect2):
    for a, b in [(rect1, rect2), (rect2, rect1)]:
        # Check if a's corners are inside b
        if ((isPointInsideRect(a.left, a.top, b)) or
            (isPointInsideRect(a.left, a.bottom, b)) or
            (isPointInsideRect(a.right, a.top, b)) or
            (isPointInsideRect(a.right, a.bottom, b))):
            return True
    return False

def isPointInsideRect(x, y, rect):
    if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
        return True
    else:
        return False

def DisplayEndGame(lost):
    endPage = pygame.Surface(gameSurface.get_size())
    endPage = endPage.convert()
    endPage.fill((150, 150, 150))
    font = pygame.font.SysFont('Comic Sans MS', 36)
    text = font.render('Game Over', 1, (10, 10, 10))
    textpos = text.get_rect(centerx=welcomePage.get_width()/2, centery = 20)
    if lost:
        text2 = font.render('Bad guys got you 5 times', 1, (10, 10, 10))
    else:
        text2 = font.render('You won!!!', 1, (10, 10, 10))\
                
    textpos2 = text2.get_rect(centerx=welcomePage.get_width()/2, centery = 60)
    #text3 = font.render('Press \'r\' to replay', 1, (10, 10, 10))
    #textpos3 = text3.get_rect(centerx=welcomePage.get_width()/2, centery = 120)
    endPage.blit(text, textpos)
    endPage.blit(text2, textpos2)
    #endPage.blit(text3, textpos3)
    gameSurface.blit(endPage, (0, 0))
    pygame.display.flip()
    
# setup the game
pygame.init()
gameSurface = pygame.display.set_mode((1024,786))
pygame.display.set_caption('Fun game')
pygame.key.set_repeat(1, 1)

#Create The Splash page
welcomePage = pygame.Surface(gameSurface.get_size())
welcomePage = welcomePage.convert()
welcomePage.fill((150, 150, 150))
font = pygame.font.SysFont('Comic Sans MS', 36)
text = font.render('Silly shooter type game.  Use space to shoot, arrows to move', 1, (10, 10, 10))
textpos = text.get_rect(centerx=welcomePage.get_width()/2, centery = 20)
text2 = font.render('Press space to begin', 1, (10, 10, 10))
textpos2 = text2.get_rect(centerx=welcomePage.get_width()/2, centery = 60)
welcomePage.blit(text, textpos)
welcomePage.blit(text2, textpos2)
gameSurface.blit(welcomePage, (0, 0))
pygame.display.flip()

# wait for the space to be pressed.
startGame = False
while not startGame:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            startGame = True
            
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

# setup the baddies
numBaddies = 7
baddies = []
for baddie in range(numBaddies):
    CreateBadGuy()

allsprites = pygame.sprite.RenderPlain(sprites)

numLivesLeft = 5

# game loop
gameOver = False
while not gameOver:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # handle input
    ship.handleKeyInput(pygame.key.get_pressed())
    
    # update UI
    gameSurface.blit(background, (0, 0))
    ship.update()
    for baddie in baddies[:]:
        if baddie.update() == False:
            baddies.remove(baddie)
            CreateBadGuy()
            allsprites = pygame.sprite.RenderPlain(sprites)
        if doRectsOverlap(ship.rect, baddie.rect):
            ship.rect.move_ip(-ship.rect.left, 0)
            # hack to stop the baddie and the ship from colliding
            # more than once. I'm sure there is a better way
            baddie.rect.move_ip(-1000, -1000)
            baddies.remove(baddie)
            numLivesLeft = numLivesLeft - 1
        for b,bullet in ship.bullets:
            if doRectsOverlap(baddie.rect, bullet):
                baddie.kill()
                sprites.remove(baddie)
                baddies.remove(baddie)

    allsprites.draw(gameSurface)
    pygame.display.flip()

    # see if we are at an end state
    if len(baddies) == 0:
        gameOver = True
        DisplayEndGame(False)
    elif numLivesLeft == 0:
        gameOver = True
        DisplayEndGame(True)

# disable key repeat
pygame.key.set_repeat()

# wait for user to end the game
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            pygame.quit()
            sys.exit()

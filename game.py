# system imports
import random
import sys
import pygame
import pygame._view # needed to turn to an exe

# local imports
import shipSprite
import badGuySprite

# specific imports
from pygame.locals import *
from shipSprite import ShipSprite
from badGuySprite import BadGuySprite

# cxfreeze didn't work with the default python font so using this one
FONT = 'Comic Sans MS' 
NUMLIVES = 5
NUMBADGUYS = 7

def createBadGuy(gameSurface):
    badGuy = BadGuySprite(gameSurface)
    badGuy.rect = badGuy.rect.move(
        random.randint(0, gameSurface.get_width()),
        random.randint(20, gameSurface.get_height()))
    return badGuy

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

def renderTextOnPage(textFontTuples, surface, fontColor, initialy = 20):
    for t, f in textFontTuples:
        initialy += 20
        if f == None:
            continue
        line = f.render(t, True, fontColor)
        textpos = line.get_rect(
                centerx = surface.get_width()/2, 
                centery = initialy)
        surface.blit(line, textpos)

def displayEndGame(lost, gameSurface):
    bigfont = pygame.font.SysFont(FONT, 128)
    smallfont = pygame.font.SysFont(FONT, 18)
    if lost:
        text = 'You Lost!'
    else:
        text = 'You WON!!!!'

    textFont = [
            (text, bigfont), 
            ('', None),
            ('', None),
            ('', None),
            ('', None),
            ('', None),
            ('Press <R> to restart.', smallfont), 
            ('Press <ESC> to quit.', smallfont)
        ]
    renderTextOnPage(textFont, gameSurface, (10, 10, 210), 
            gameSurface.get_height()/2 - 50)

def displayWelcome(gameSurface):
    # create the splash page
    welcomePage = pygame.Surface(gameSurface.get_size())
    welcomePage = welcomePage.convert()
    welcomePage.fill((190, 190, 190))
    bigfont = pygame.font.SysFont(FONT, 36)
    smallfont = pygame.font.SysFont(FONT, 16)
    fontColor = (0, 0, 200)
    text = [
            ('',None),
            ('Rocket Fire!!!', bigfont), 
            ('',None),
            ('Goal: Remove all bad guys from the screen.', smallfont),
            ('Controls- ', smallfont),
            ('  Use left and right arrows to move.', smallfont),
            ('  Use space to shoot.', smallfont),
            ('',None),
            ('',None),
            ('Hit <SPACE> to begin.', bigfont)
           ]

    renderTextOnPage(text, welcomePage, fontColor)

    welcomeImage = pygame.image.load('ship.png')
    welcomeImageRect = welcomeImage.get_rect()
    welcomeImageRect = welcomeImageRect.move(
            welcomePage.get_width()/2 - welcomeImageRect.width/2, 
            welcomePage.get_height()/2 - welcomeImageRect.height/2)
    welcomePage.blit(welcomeImage, welcomeImageRect)

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

def main(showWelcome):
    # setup the game
    pygame.init()
    gameSurface = pygame.display.set_mode((1024,786))
    pygame.display.set_caption('Fun game')
    pygame.key.set_repeat(1, 1)

    if showWelcome:
        displayWelcome(gameSurface)

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
    shipSprite = pygame.sprite.GroupSingle(ship)

    # setup the baddies
    numBaddies = NUMBADGUYS
    baddies = []
    for baddie in range(numBaddies):
        badguy = createBadGuy(gameSurface)
        baddies.append(badguy)

    badGuySprites = pygame.sprite.RenderPlain(baddies)

    numLivesLeft = NUMLIVES 

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
                # baddie is off the screen
                # remove the old sprite and spawn a new baddie
                badGuySprites.remove(baddie)
                baddies.remove(baddie)
                newbaddie = createBadGuy(gameSurface)
                badGuySprites.add(newbaddie)
                baddies.append(newbaddie)
            if doRectsOverlap(ship.rect, baddie.rect):
                # move the ship to the start
                ship.rect.move_ip(-ship.rect.left, 0)

                # remove the collided bad guy
                badGuySprites.remove(baddie)
                baddies.remove(baddie)

                # spawn a new bad guy
                newbaddie = createBadGuy(gameSurface)
                badGuySprites.add(newbaddie)
                baddies.append(newbaddie)

                # update the number of lives
                numLivesLeft = numLivesLeft - 1
            for b,bullet in ship.bullets:
                # see if any of the bullets hit
                if doRectsOverlap(baddie.rect, bullet):
                    # on a hit remove the baddie
                    badGuySprites.remove(baddie)
                    baddies.remove(baddie)

        # update the display
        badGuySprites.draw(gameSurface)
        shipSprite.draw(gameSurface)

        # see if we are at an end state
        if len(baddies) == 0:
            gameOver = True
            displayEndGame(False, gameSurface)
        elif numLivesLeft == 0:
            gameOver = True
            displayEndGame(True, gameSurface)

        pygame.display.flip()

    # disable key repeat
    pygame.key.set_repeat()

    # wait for user to end the game
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            elif event.type == KEYDOWN and event.key == K_r:
                return True 

if __name__ == "__main__":
    if main(True):
        while main(False):
            pass
    pygame.quit()


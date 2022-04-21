import pygame
import sys
import os
import random

pygame.init() #Initialize Pygame
defaultFont = pygame.font.get_default_font()
scoreFont = pygame.font.Font(defaultFont, 40)

WIN_SIZE = 1000 #Window height and width
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))#Create a window
pygame.display.set_caption('Doodle Hop') #Set title of game on window
""" windowIcon = pygame.image.load("/home/noah/Documents/Python/Projects/Doodle Hop/img/doodleHopIcon.jpg") #Load icon from file
pygame.display.set_icon(windowIcon) #Set loaded icon as window icon """

"""Player Class holds coordinates, size, and velocity of the player."""
class Player(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left,top,width,height)

        self.isJumping = False
        self.isFalling = False
        self.changeY = 0
    
    def getCoords(self):
        return (self.left, self.top)


"""Spawn a new platform. If there are no arguments, spawn them anywhere. If there is a tuple arguement, use first value as range for new platform and second value as number of platforms to spawn."""
def newPlatform():
    if len(platList) == 0:
        newPlat = pygame.Rect(random.randint(0, WIN_SIZE-50), random.randint(795, 812), 55, 13)
        platList.append(newPlat)
    else:
        newPlat = pygame.Rect(random.randint(0, WIN_SIZE-50), random.randint(platList[-1].top - 150, platList[-1].top-40), 55, 13)
        platList.append(newPlat)


def checkJump():
    if player.isJumping == True:
        if player.changeY > 0:
            player.top -= player.changeY
            player.changeY -= .4
        elif player.changeY <= 0:
            player.isJumping = False
            player.isFalling = True
    
def checkFalling():
    if player.isFalling == True:
            player.top += player.changeY
            player.changeY += .5

def checkCollision():
    global score
    global scoreUP
    global setFall

    if player.isJumping == True: return 0

    for rect in platList:
        if player.clipline((rect.topleft), (rect.topright)):
            player.update(player.left, rect.top - 48, 50, 50 )
            player.isJumping = False
            player.isFalling = False
            player.changeY = 0
            if scoreUP == True:
                score += 1
                scoreUP = False
            break
        elif player.top < setFall:
            player.isFalling = True

def checkScroll():
    if player.top > 300: return 0
    
    for plat in platList:
        plat.update(plat.left, plat.top + player.changeY, plat.width, plat.height)
        if plat.top > 1000:
            platList.remove(plat)
    
def endGame():
    global canJump

    platList.clear()

    screen.fill((255,255,255))
    gameOverFont = pygame.font.Font(defaultFont, 125)
    gameOverText = gameOverFont.render('GAME OVER', True, (255, 0, 0))
    screen.blit(gameOverText, (110,425))
    scoreOverFont = pygame.font.Font(defaultFont, 75)
    gameOverScore = scoreOverFont.render("Score: " + str(score), True, (255,0,0))
    screen.blit(gameOverScore, (350, 575))

    player.top = 1010
    canJump = False


"""Initialization of all needed objects"""
running = True

player = Player(475, 825, 50, 50)
platList = []

jumpHeight = 15
canJump = True
setFall = 825

score = 0
scoreUP = True

jumpSound = pygame.mixer.Sound(os.path.join('sound', 'jumpSound.wav'))

"""MAIN GAME LOOP"""
while running:
    #Background color
    screen.fill((255,255,255))
    showScore = scoreFont.render(str(score), True, (125,125,125))
    screen.blit(showScore, (25,25))

    for event in pygame.event.get():
        #Close game
        if event.type == pygame.QUIT: sys.exit()

        #Jump Reset
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                canJump = True

    #Gets all keys pressed. Used to iterate through and find specific key presses.
    pressed = pygame.key.get_pressed()

    #Start Jump
    if pressed[pygame.K_SPACE]:
        if canJump == True:
            if player.isJumping == True or player.isFalling == True:
                pass
            else:
                player.isJumping = True
                player.isFalling = False
                player.changeY = jumpHeight
                canJump = False
                scoreUP = True
                setFall = 1000
                pygame.mixer.Sound.play(jumpSound)
        else:
            pass

    #Player move right
    if pressed[pygame.K_d] and player.left <= WIN_SIZE-55: player.left += 5
    elif pressed[pygame.K_d]: player.left = WIN_SIZE-50

    #Player move left
    if pressed[pygame.K_a] and player.left >= 10: player.left -= 5
    elif pressed[pygame.K_a]: player.left = 0


    #Draw player
    pygame.draw.rect(screen, (0,0,0), (pygame.Rect(player.getCoords(), (50,50))))

    #Limit max platforms to 20
    while len(platList) < 20:
        newPlatform()
    
    #Draw all platforms
    for plat in platList:
        pygame.draw.rect(screen, (0,0,0), (plat))

    #Do all checks for current game state
    checkCollision()
    checkJump()
    checkFalling()
    checkScroll()

    if player.isFalling == True and player.top > 1000:
        endGame()

    #Framerate
    pygame.time.Clock().tick(144)

    #update the current drawing of the screen
    pygame.display.update()

import pygame
import sys
import os
import random

pygame.init()  # Initialize Pygame
default_font = pygame.font.get_default_font()
score_font = pygame.font.Font(default_font, 40)

WIN_SIZE = 1000  # Window height and width
screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))  # Create a window
pygame.display.set_caption('Doodle Hop')  # Set title of game on window
"""windowIcon = pygame.image.load("/PATH TO WINDOW ICON HERE") #Load icon 
pygame.display.set_icon(windowIcon) #Set loaded icon as window icon """


# Player Class holds coordinates, size, and velocity of the player.
class Player(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)

        self.is_jumping = False
        self.is_falling = False
        self.change_y = 0

    def get_coords(self):
        return self.left, self.top


# Spawn a new platform. If there are no arguments, spawn them anywhere. If there is a tuple argument,
# use first value as range for new platform and second value as number of platforms to spawn.
def new_platform():
    if len(plat_list) == 0:
        new_plat = pygame.Rect(random.randint(0, WIN_SIZE - 50), random.randint(795, 812), 55, 13)
        plat_list.append(new_plat)
    else:
        new_plat = pygame.Rect(random.randint(0, WIN_SIZE - 50),
                               random.randint(plat_list[-1].top - 150, plat_list[-1].top - 40), 55, 13)
        plat_list.append(new_plat)


def check_jump():
    if player.is_jumping:
        if player.change_y > 0:
            player.top -= player.change_y
            player.change_y -= .4
        elif player.change_y <= 0:
            player.is_jumping = False
            player.is_falling = True


def check_falling():
    if player.is_falling:
        player.top += player.change_y
        player.change_y += .5


def check_collision():
    global score
    global score_up
    global set_fall

    if player.is_jumping:
        return 0

    for rect in plat_list:
        if player.clipline(rect.topleft, rect.topright):
            player.update(player.left, rect.top - 48, 50, 50)
            player.is_jumping = False
            player.is_falling = False
            player.change_y = 0
            if score_up:
                score += 1
                score_up = False
            break
        elif player.top < set_fall:
            player.is_falling = True


def check_scroll():
    if player.top > 300:
        return 0
    for current_plat in plat_list:
        current_plat.update(current_plat.left, current_plat.top + player.change_y, current_plat.width,
                            current_plat.height)
        if current_plat.top > 1000:
            plat_list.remove(current_plat)


def end_game():
    global can_jump

    plat_list.clear()

    screen.fill((255, 255, 255))
    game_over_font = pygame.font.Font(default_font, 125)
    game_over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(game_over_text, (110, 425))
    score_over_font = pygame.font.Font(default_font, 75)
    game_over_score = score_over_font.render("Score: " + str(score), True, (255, 0, 0))
    screen.blit(game_over_score, (350, 575))

    player.top = 1010
    can_jump = False


"""Initialization of all needed objects"""
running = True

player = Player(475, 825, 50, 50)
plat_list = []

jump_height = 15
can_jump = True
set_fall = 825

score = 0
score_up = True

jump_sound = pygame.mixer.Sound(os.path.join('sound', 'jumpSound.wav'))

"""MAIN GAME LOOP"""
while running:
    # Background color
    screen.fill((255, 255, 255))
    show_score = score_font.render(str(score), True, (125, 125, 125))
    screen.blit(show_score, (25, 25))

    for event in pygame.event.get():
        # Close game
        if event.type == pygame.QUIT:
            sys.exit()

        # Jump Reset
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                can_jump = True

    # Gets all keys pressed. Used to iterate through and find specific key presses.
    pressed = pygame.key.get_pressed()

    # Start Jump
    if pressed[pygame.K_SPACE]:
        if can_jump:
            if player.is_jumping or player.is_falling:
                pass
            else:
                player.is_jumping = True
                player.is_falling = False
                player.change_y = jump_height
                can_jump = False
                score_up = True
                set_fall = 1000
                pygame.mixer.Sound.play(jump_sound)
        else:
            pass

    # Player move right
    if pressed[pygame.K_d] and player.left <= WIN_SIZE - 55:
        player.left += 5
    elif pressed[pygame.K_d]:
        player.left = WIN_SIZE - 50

    # Player move left
    if pressed[pygame.K_a] and player.left >= 10:
        player.left -= 5
    elif pressed[pygame.K_a]:
        player.left = 0

    # Draw player
    pygame.draw.rect(screen, (0, 0, 0), (pygame.Rect(player.get_coords(), (50, 50))))

    # Limit max platforms to 20
    while len(plat_list) < 20:
        new_platform()

    # Draw all platforms
    for plat in plat_list:
        pygame.draw.rect(screen, (0, 0, 0), plat)

    # Do all checks for current game state
    check_collision()
    check_jump()
    check_falling()
    check_scroll()

    if player.is_falling and player.top > 1000:
        end_game()

    # Frame-rate
    pygame.time.Clock().tick(144)

    # update the current drawing of the screen
    pygame.display.update()

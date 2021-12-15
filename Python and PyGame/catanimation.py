import pygame, sys
from pygame.locals import *

pygame.init()

# frame per second setting
FPS = 30
fpsClock = pygame.time.Clock()

#Set up window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

# Defining important variables
WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

#main loop
while True:
    #fill board white
    DISPLAYSURF.fill(WHITE)


    #Seeing if direction is right
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    #Seeing if direction is down
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'

    #Seeing if direction is left
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    #Seeing if direction is up
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    #Display Image
    DISPLAYSURF.blit(catImg, (catx, caty))

    #Events Loop
    for event in pygame.event.get():
        #Seeing if the window is closed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Displaying changes and pausing
    pygame.display.update()
    fpsClock.tick(FPS)


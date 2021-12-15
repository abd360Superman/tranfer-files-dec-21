import pygame, sys
from pygame.locals import *

pygame.init()

#Setup the window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Drawing')

# setup the colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Change fill of window
DISPLAYSURF.fill(WHITE)

#Draw a polygon
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# Draw Lines
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)

#Draw a cricle
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 50), 20, 0)

# Draw an ellipse
pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)

#Draw a rectangle
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

#Pixel Object to change colours of pixels
pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
del pixObj

#Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()




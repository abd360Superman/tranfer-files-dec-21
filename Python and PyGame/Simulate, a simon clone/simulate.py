# Simulate, a Simon clone
# By Darsh Choudhary darshchoudhary171@gmail.com
# Made with PyGame

# importing modules
import random, sys, time, pygame
from pygame.locals import *
# CONSTANTS
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FLASHSPEED = 500 # milliseconds
FLASHDELAY = 200 # milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed

# colors           R    G    B
WHITE          = (255, 255, 255)
BLACK          = ( 0 ,  0 ,  0 )
BRIGHTRED      = (255,  0 ,  0 )
RED            = (155,  0 ,  0 )
BRIGHTGREEN    = ( 0 , 255,  0 )
GREEN          = ( 0 , 155,  0 )
BRIGHTBLUE     = ( 0 ,  0 , 255)
BLUE           = ( 0 ,  0 , 155)
BRIGHTYELLOW   = (255, 255,  0 )
YELLOW         = (155, 155,  0 )
DARKGRAY       = ( 40,  40,  40)
bgColor = BLACK
# x and y margins
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect objects for each of the four buttons
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

def main(): # main func
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4
    # initialize window
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16) # init font
    # info surf
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)
    # load sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # initialize variables for a new game
    pattern = [] # stores the pattern of colours
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0

    waitingForInput = False # when False, the pattern is playing. when True, waiting for the player to click a button

    while True: # main game loop
        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN or BLUE)
        DISPLAYSURF.fill(bgColor)
        drawButtons()
        # show text
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP: # mouse press
                mousex, mousey = event.pos
                clickedButton = getButtonClicked(mousex,mousey) # get button user clicked
            elif event.type == KEYDOWN: # key pressed
                if event.key == K_q: # q
                    clickedButton = YELLOW
                elif event.key == K_w: # w
                    clickedButton = BLUE
                elif event.key == K_a: # a
                    clickedButton = RED
                elif event.key == K_s: # s
                    clickedButton = GREEN


        # play the audio if not waiting for user input
        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN))) # append a random color to pattern
            for button in pattern:
                flashButtonAnimation(button) # flash button color and sound
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            # wait for person to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time() # change last click time

                if currentStep == len(pattern):
                    # last button clicked
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False # play sounds again
                    currentStep = 0 # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed incorrect button or is timed out
                gameOverAnimation()
                # reset variables
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# function when runs to terminate program
def terminate():
    pygame.quit()
    sys.exit()

# check when to quit game
def checkForQuit():
    for event in pygame.event.get(QUIT): # get all QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

# flash button animation function
def flashButtonAnimation(color, animationSpeed=50):
    if color == YELLOW: # changing everything according to yellow
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE: # changing everything according to blue
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED: # changing everything according to red
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN: # changing everything according to green
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    # animating
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play() # play the sound
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

# draw the buttons
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE, BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED, REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN, GREENRECT)

# change the background animation
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) # random bgcolor

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons() # redraw buttons on top of tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

# animation when game is over
def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time, roughly
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop
            # to go from 0 to 255, the second from 255 to 0.
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency. 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


# get which button was clicked
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None


if __name__ == '__main__':
    main()

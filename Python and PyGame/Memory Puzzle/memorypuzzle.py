# Memory Puzzle
# By Darsh Choudhary darshchoudhary171@gmail.com
# Made with PyGame

#Imports
import random, pygame, sys
from pygame.locals import *
# CONSTANTS
FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # window's width in pixels
WINDOWHEIGHT = 480 # window's height in pixels
REVEALSPEED = 8 # Speed boxes slide to uncover
BOXSIZE = 40 # width and height of box
GAPSIZE = 10 # size of gap between boxes
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches' # Confirming that we will have even number of icons
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2) # X MARGIN of the board
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2) # Y MARGIN of the board

# colours      R    G    B
GRAY       = (100, 100, 100)
NAVYBLUE   = ( 60,  60, 100)
WHITE      = (255, 255, 255)
RED        = (255,  0 ,  0 )
GREEN      = ( 0 , 255,  0 )
BLUE       = ( 0 ,  0 , 255)
YELLOW     = (255, 255,  0 )
ORANGE     = (255, 128,  0 )
PURPLE     = (255,  0 , 255)
CYAN       = ( 0 , 255, 255)
# Assigning colours to constants
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
# Shapes
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'
#Seeing whether the board is big enough to hold all icons
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too big for the number of shapes/colors defined'
# Main Function
def main():
    global FPSCLOCK, DISPLAYSURF # Globalization of two variables
    pygame.init() # Initializing PyGame window
    FPSCLOCK = pygame.time.Clock() # Setting up timer
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Setting up game board size

    mousex = 0 # Used to store x coordinate of mouse event
    mousey = 0 # Used to store y coordinate of mouse event
    pygame.display.set_caption('Memory Game') # Setting up gameboard caption
    #Setting 2D List, acting like Gameboard
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard) # animating the game board

    while True: # main loop
        mouseClicked = False # initializing mouse click to false per round
        # drawing the board
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE): # quitting the game
                pygame.quit() 
                sys.exit()
            elif event.type == MOUSEMOTION: # Seeing if mouse was moving
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP: # seeing if mouse was clicked
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey) # Getting whether box is at pixel
        if boxx != None and boxy != None: # Only executing if the box is at the pixel

            if not revealedBoxes[boxx][boxy]: # Seeing if the box has not been clicked
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked: # seeing if mouse was clicked on a not yet revealed box
                revealBoxesAnimation(mainBoard, [(boxx, boxy)]) # Playing animation when box is revealed
                revealedBoxes[boxx][boxy] = True # set box as "revealed"
                if firstSelection == None: # the current box was the first one clicked
                    firstSelection = (boxx, boxy)
                else: # The current box was the second one clicked
                    # check if the two icons match
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1]) # Getting first clicked shape and color
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy) # Getting second clicked shape and color

                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons ain't matchin' nobody. Re-cover them
                        pygame.time.wait(1000) # Waiting for a second
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)]) # Cover the wrong boxes clicked
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
# Setting first clicked box to not revealed
                        revealedBoxes[boxx][boxy] = False # Setting the second clicked box to not revealed
                    elif hasWon(revealedBoxes): # Check if all boxes found
                        gameWonAnimation(mainBoard) # Game won animation
                        pygame.time.wait(2000)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show fullt unrevealed board
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        #Replay Start Game Animation
                        startGameAnimation(mainBoard)
                    firstSelection = None # Reset the firstselection to None

        # Redraw the screen and wait a second
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Get revealed boxes
def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT) # Generating rows and colums to store data
    return revealedBoxes

# Generating Randomized Board
def getRandomizedBoard():
    # Get list of every shape in every color possible
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color)) # Nesting For Loop to get all combination of shape and color

    random.shuffle(icons) # Shuffling the icons
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # Calculate number of icons needed
    icons = icons[:numIconsUsed] * 2 # Make two of each icon
    random.shuffle(icons)

    # Create the board data structure with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = [] # Creating column variable
        for y in range(BOARDHEIGHT):
            column.append(icons[0]) # Adding the icon to column
            del icons[0] # remov icon after assigning
        board.append(column) # Adding column of icons to board
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into lists of lists, where the inner lists have at most groupSize number of items

    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN # Get left coordinate
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN # Get top coordunate
    return (left, top)

# Return the box at pixel
def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy) # Get the top and left coordinates
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE) # Making a pygame rectangle
            if boxRect.collidepoint(x, y): # Seeing if the rectangle is at the position to return boxx, boxy
                return (boxx, boxy)
    return (None, None)

# Draw the icon
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # Quarter of box size
    half = int(BOXSIZE * 0.5) # Half of box size

    left, top = leftTopCoordsOfBox(boxx, boxy)
    # Draw Shapes
    if shape == DONUT: # Draw a donut
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE: # Draw a square
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND: # Draw a diamond
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES: # Draw lines
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL: # Draw an oval
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

# get shape and color of icon
def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list of two-item lists, which have the x & y spot of the box

    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1]) # Get shape and color
        drawIcon(shape, color, box[0], box[1]) # Draw the icon
        if coverage > 0: # only draw the cover if there is a coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

# Reveal Boxes Animation
def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

# Cover boxes animation
def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

# Drawing the board
def drawBoard(board, revealed):
    # Draw all the boxes in their covered or revealed state
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the revealed icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

# Draw a highlighted box
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

# Start the main game animation
def startGameAnimation(board):
    # Randomly reveal 8 boxes
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y)) # Get all boxes
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes) # Split boxes into groups of 8

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups: # Looping over boxGroups
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

# Game won animation
def gameWonAnimation(board):
    # flash the background color when player wins
    coveredBoxes = generateRevealBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    # Loop through colours to flash
    for i in range(13):
        color1, color2 = color2, color1 # swap colours
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

# Plaser has won
def hasWon(revealedBoxes):
    # Returns true if all boxes are revealed, otherwise false
    for i in revealedBoxes:
        if False in i:
            return False # 1 or more boxes covered
    return True

# Run main()
if __name__ == '__main__':
    main()
    

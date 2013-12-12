import pygame
import Shape

__author__ = 'Rich'
#set the proper mouse values
LEFT = 1
RIGHT = 3

#set up the window, set the background
BACKGROUND = pygame.image.load('Images/breakout_bg.png')
BALL = Shape.Shape(320,360,25,25,pygame.image.load('Images/ball.png'))
BUMPER = Shape.Shape(320,430,125,35,pygame.image.load('Images/bumper.png'))
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
BLOCKSROW = 10 #number of blocks in a row
BLOCKSCOLUMN = 5 #number of blocks in a column
BLOCKWIDTH = 35 #sprite is 40 pixels by 40 pixels
BLOCKHEIGHT = 35 #height of the block
BALLWIDTH = 25 #width of the ball
BALLHEIGHT = 25 #height of the ball
SCOREWIDTH = 100 #width of the score box
SCORES_FILE = "hs.dat" #file in which to store high scores
HSROWS = 10 #number of rows of high scores
HSHEIGHT = 40 #height in pixels of each letter in the high score
HSMARGIN = 5 #margin between scores
HSGAP = 20 #gap between name/score/date
#margin from the sides in pixels
XMARGIN = int((WINDOWWIDTH - (BLOCKSROW*BLOCKWIDTH))/2)
YMARGIN = 80 #margin from the top in pixels
WHITE = (255,255,255)
BUMPERWIDTH = 125 #width of the bumper
BUMPERHEIGHT = 35 #height of the bumper
POINTERWIDTH = 40 #width of the pointer at the start screen
POINTERHEIGHT = 40 #height of the pointer at the start screen
#shorter constants so I don't have to type the strings
DR = 'downright'
DL = 'downleft'
UR = 'upright'
UL = 'upleft'
#set the FPS
FPS = 30
fpsClock = pygame.time.Clock()
import sys
import math
import random
import Screens
from Constants import *

#cPickle is used to serialize the high scores
try:
    import cPickle as pickle
except:
    import pickle

#Dict to match alphanumeric characters to their filenames
ALPHA = {}
for x in range(65,91):
    a = str(chr(x))
    ALPHA[a] = 'Alphabet/' + a + '.png'
for x in range(10):
    ALPHA[str(x)] = 'Alphabet/' + str(x) + '.png'

#this method checks to see whether the ball has hit the bumper
def hitBumper2(direction):
    #bumperx is the left coordinate of the bumper
    #ballx is the left coordinate of the ball
    if BALL.x>=BUMPER.x and (BALL.x<=(BUMPER.x + BUMPER.width) and (direction=='downleft' or direction=='downright')):
        #bally should be approaching from the top, so its y-coordinate will be LESS than the y-coordinate of the bumper
        if BALL.y-BUMPER.y >=-15 and BALL.y-BUMPER.y<=0:
            return True
    return False

def hitBumper(ballx, bally,bumperx,bumpery,direction):
    #bumperx is the left coordinate of the bumper
    #ballx is the left coordinate of the ball
    if ballx>=bumperx and (ballx<=(bumperx + BUMPERWIDTH) and (direction=='downleft' or direction=='downright')):
        #bally should be approaching from the top, so its y-coordinate will be LESS than the y-coordinate of the bumper
        if bally-bumpery >=-15 and bally-bumpery<=0:
            return True
    return False

'''
def generateBlocks():
    #the blocks array will be false if it HAS been hit
    #so, we'll draw it if it's true
    blocks = [[True for boxx in range(BLOCKSROW)] for boxy in range(BLOCKSCOLUMN)]
    return blocks
'''

def generateBlocks():
    #the blocks array will be false if it HAS been hit
    #so, we'll draw it if it's true
    blocks = []
    for boxx in range(BLOCKSROW):
        blocks.append([])
        for boxy in range(BLOCKSCOLUMN):
            left, top = topLeftCoords(boxx,boxy)
            blocks[boxx].append(Shape.Block(left,top,BLOCKWIDTH,BLOCKHEIGHT,'Images/block.png'))
    return blocks

def drawBlocks(blocks):
    for boxx in range(BLOCKSROW):
        for boxy in range(BLOCKSCOLUMN):
            b = blocks[boxx][boxy]
            if b.alive:
                block_img = pygame.image.load(b.img)
                DISPLAYSURF.blit(block_img,(b.x,b.y))
    

def topLeftCoords(blockx,blocky):
    #blockx should be in the range of 0 to BLOCKSROW
    #blocky should be in the range of 0 to BLOCKSCOLUMN
    left = blockx*BLOCKWIDTH + XMARGIN
    top = blocky*BLOCKHEIGHT + YMARGIN
    return left, top

def hitBlock(ballx, bally, blocks,direction):
    for boxx in range(BLOCKSROW):
        for boxy in range(BLOCKSCOLUMN):
            b = blocks[boxx][boxy]
            if b.alive:
                left, top = b.x,b.y
                blockRect = pygame.Rect(left,top,b.width,b.height)
                ballRect = pygame.Rect(ballx,bally,BALLWIDTH,BALLHEIGHT)
                if blockRect.colliderect(ballRect):
                    direction = block_direction_change(ballx,bally,left,top,direction)
                    return boxy,boxx, direction
    return -1,-1, direction

def leftDist(ballRect, blockRect):
    return math.fabs(blockRect.left-ballRect.left)

def rightDist(ballRect, blockRect):
    return math.fabs(blockRect.right-ballRect.right)

def topDist(ballRect, blockRect):
    return math.fabs(blockRect.top-ballRect.top)

def bottomDist(ballRect, blockRect):
    return math.fabs(blockRect.bottom-ballRect.bottom)

#I commented out the old code just in case I ever wanted to see how I originally designed it
def gameOver():
    '''
    gameOverFont = pygame.font.Font('freesansbold.ttf',120)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/4)
    #the +30 will leave 20 pixels between "Game" and "Over"
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT/4 + gameRect.height + 30)
    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    pygame.display.update()
    pygame.time.wait(3000)
    '''
    GAME = pygame.image.load("Images/Game.png")
    OVER = pygame.image.load("Images/over.png")
    game_rect = GAME.get_rect()
    game_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/4)
    over_rect = OVER.get_rect()
    over_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/4 + game_rect.height + 15)
    DISPLAYSURF.blit(GAME,game_rect)
    DISPLAYSURF.blit(OVER,over_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    return

#not sure I'm crazy about how this method works
#it produces correct direction changes 95% of the time
#the other 5% sucks though
def block_direction_change(ballx, bally, leftBox, topBox, direction):
    block_rect = pygame.Rect(leftBox,topBox,BLOCKWIDTH,BLOCKHEIGHT)
    ball_rect = pygame.Rect(ballx,bally,BALLWIDTH,BALLHEIGHT)
    #if the ball is going down and to the right
    #it can hit the left or the top
    if direction == DR:
        if topDist(ball_rect,block_rect) >= rightDist(ball_rect,block_rect):
            direction = UR
        else:
            direction = DL
    #if the ball is going down and to the left
    #it can hit the right or the top
    elif direction == DL:
        if topDist(ball_rect,block_rect) >= leftDist(ball_rect,block_rect):
            direction = UL
        else:
            direction = DR
    #if the ball is going up and to the right
    #it can hit the left or the bottom
    elif direction == UR:
        if bottomDist(ball_rect,block_rect) >= leftDist(ball_rect,block_rect):
            direction = DR
        else:
            direction = UL
    #if the ball is going up and to the left
    #it can hit the right or the bottom
    elif direction == UL:
        if bottomDist(ball_rect,block_rect) >= rightDist(ball_rect,block_rect):
            direction = DL
        else:
            direction = UR
    return direction

def move(ballx, bally, bumperx, bumpery, direction):
    #returns the x and y positions of the ball, and the direction
    #if the y coordinate of the ball hits the bottom of the screen
    #then the method returns -1
    if hitBumper(ballx, bally, bumperx, bumpery,direction):
        if direction == DR:
            direction = UR
        elif direction == DL:
            direction = UL
    if direction== DR:
        ballx+=speed
        bally+=speed
        if ballx>=620:
            direction=DL
        #if the y coordinate of the ball is this far, it should be game over
        elif bally>=460:
            direction=-1
    elif direction==DL:
        ballx-=speed
        bally+=speed
        if ballx<=-5:
            direction=DR
        elif bally>=460:
        #if the y coordinate of the ball is this far, it should be game over
            direction=-1
    elif direction== UR:
        ballx+=speed
        bally-=speed
        if ballx>=620:
            direction=UL
        elif bally<=-5:
            direction=DR
    elif direction== UL:
        ballx-=speed
        bally-=speed
        if ballx<=-5:
            direction=UR
        elif bally<=-5:
            direction=DL
    
    return ballx, bally, direction

def resetBoard():
    blocks = generateBlocks()
    drawBlocks(blocks)
    return blocks

def runGame():
    score = 0
    ballx = 320
    bally = 360
    #use a random number to tell which way to start the ball off
    randVal = random.random()
    if(randVal<=.5):
        direction = DL
    else:
        direction = DR
    start = False
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    #define the beginning ball values
    ballImg = pygame.image.load('Images/ball.png')
    scoreImage = pygame.image.load('Images/score.png')
    scoreFont = pygame.font.Font('freesansbold.ttf',37)
    bumperImg = pygame.image.load('Images/bumper.png')
    #add the ball to the screen
    DISPLAYSURF.blit(ballImg, (ballx,bally))

    #define the beginning bumper values
    bumperx = 320
    bumpery = 430
    #add the bumper to the screen
    DISPLAYSURF.blit(bumperImg,(bumperx,bumpery))

    #define the beginning block values
    blocks = generateBlocks()
    blocksDestroyed = 0
    #draw blocks to the screen
    drawBlocks(blocks)
    
    while True:
        if start:
            ballx,bally,direction = move(ballx,bally,bumperx,bumpery,direction)
            #if the ball hit the bottom of the screen, game over
            if direction == -1:
                Screens.gameOver(DISPLAYSURF)
                Screens.highScoreScreen(DISPLAYSURF, score)
                return
            blockHitY, blockHitX, direction = hitBlock(ballx,bally,blocks,direction)
            if blockHitX>=0 and blockHitY>=0:
                blocks[blockHitX][blockHitY].alive = False
                blocksDestroyed+=1
                score += 10
                if blocksDestroyed >= BLOCKSROW*BLOCKSCOLUMN:
                    blocks = resetBoard()
                    blocksDestroyed = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                start = not start
            elif event.type == pygame.MOUSEMOTION:
                #the y of the bumper isn't going to move, so let's just ignore its return value
                tempx, tempy = pygame.mouse.get_pos()
                #if it's less than 63 or greater than 578, don't let it run off the screen
                if tempx <= BUMPERWIDTH/2:
                    bumperx = -2
                elif tempx >= WINDOWWIDTH - (BUMPERWIDTH/2):
                    bumperx = 520
                #the 63 centers it - the sprite is approximately 125 pixels wide
                else:
                    bumperx = tempx-(BUMPERWIDTH/2)
        
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        DISPLAYSURF.blit(bumperImg,(bumperx,bumpery))
        DISPLAYSURF.blit(ballImg, (ballx,bally))
        DISPLAYSURF.blit(scoreImage, (440,20))
        scoreSurface = scoreFont.render(str(score), True, WHITE)
        scoreRect = scoreSurface.get_rect()
        scoreRect.topleft = (445+SCOREWIDTH, 25)
        DISPLAYSURF.blit(scoreSurface,scoreRect)
        drawBlocks(blocks)
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    pygame.init()
    global speed
    speed = 5
    Screens.drugScreen(DISPLAYSURF)
    while True:
        Screens.startScreen(DISPLAYSURF)
        runGame()
    

if __name__ == '__main__':
    main()

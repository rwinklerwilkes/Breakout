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

#this method checks to see whether the ball has hit the bumper
def hitBumper(ball,bumper,direction):
    #bumperx is the left coordinate of the bumper
    #ballx is the left coordinate of the ball
    if ball.x>=bumper.x and (ball.x<=(bumper.x + BUMPERWIDTH) and (direction=='downleft' or direction=='downright')):
        #bally should be approaching from the top, so its y-coordinate will be LESS than the y-coordinate of the bumper
        if ball.y-bumper.y >=-15 and ball.y-bumper.y<=0:
            return True
    return False

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
                DISPLAYSURF.blit(block_img, (b.x, b.y))

def topLeftCoords(blockx,blocky):
    #blockx should be in the range of 0 to BLOCKSROW
    #blocky should be in the range of 0 to BLOCKSCOLUMN
    left = blockx*BLOCKWIDTH + XMARGIN
    top = blocky*BLOCKHEIGHT + YMARGIN
    return left, top

def hitBlock(ball, blocks,direction):
    for boxx in range(BLOCKSROW):
        for boxy in range(BLOCKSCOLUMN):
            b = blocks[boxx][boxy]
            if b.alive:
                left, top = b.x,b.y
                blockRect = pygame.Rect(left,top,b.width,b.height)
                ballRect = pygame.Rect(ball.x,ball.y,ball.width,ball.height)
                if blockRect.colliderect(ballRect):
                    direction = block_direction_change(ball,left,top,direction)
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

#not sure I'm crazy about how this method works
#it produces correct direction changes 95% of the time
#the other 5% sucks though
def block_direction_change(ball, leftBox, topBox, direction):
    block_rect = pygame.Rect(leftBox,topBox,BLOCKWIDTH,BLOCKHEIGHT)
    ball_rect = pygame.Rect(ball.x,ball.y,ball.width,ball.height)
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

def move(ball, bumper, direction):
    #returns the direction
    #if the y coordinate of the ball hits the bottom of the screen
    #then the method returns -1
    if hitBumper(ball,bumper,direction):
        if direction == DR:
            direction = UR
        elif direction == DL:
            direction = UL
    if direction== DR:
        ball.x+=ball.speed
        ball.y+=ball.speed
        if ball.x>=620:
            direction=DL
        #if the y coordinate of the ball is this far, it should be game over
        elif ball.y>=460:
            direction=-1
    elif direction==DL:
        ball.x-=ball.speed
        ball.y+=ball.speed
        if ball.x<=-5:
            direction=DR
        elif ball.y>=460:
        #if the y coordinate of the ball is this far, it should be game over
            direction=-1
    elif direction== UR:
        ball.x+=ball.speed
        ball.y-=ball.speed
        if ball.x>=620:
            direction=UL
        elif ball.y<=-5:
            direction=DR
    elif direction== UL:
        ball.x-=ball.speed
        ball.y-=ball.speed
        if ball.x<=-5:
            direction=UR
        elif ball.y<=-5:
            direction=DL

    return direction

def resetBoard():
    blocks = generateBlocks()
    drawBlocks(blocks)
    return blocks

def setup():
    #add the ball to the screen
    ball = Shape.Ball(320,360,BALLWIDTH,BALLHEIGHT,pygame.image.load('Images/ball.png'))
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    DISPLAYSURF.blit(ball.img, (ball.x,ball.y))
    #define the beginning bumper values
    bumper = Shape.Shape(320,430,BUMPERWIDTH,BUMPERHEIGHT,pygame.image.load('Images/bumper.png'))
    #add the bumper to the screen
    DISPLAYSURF.blit(bumper.img,(bumper.x,bumper.y))
    #define the beginning block values
    blocks = resetBoard()
    return ball,bumper,blocks

def runGame():
    ball,bumper,blocks = setup()
    score = 0
    blocksDestroyed = 0
    #use a random number to tell which way to start the ball off
    randVal = random.random()
    if(randVal<=.5):
        direction = DL
    else:
        direction = DR
    start = False

    #define the beginning ball values
    scoreImage = pygame.image.load('Images/score.png')
    scoreFont = pygame.font.Font('freesansbold.ttf',37)
    
    while True:
        if start:
            direction = move(ball,bumper,direction)
            #if the ball hit the bottom of the screen, game over
            if direction == -1:
                Screens.gameOver()
                Screens.highScoreScreen(score)
                return
            blockHitY, blockHitX, direction = hitBlock(ball,blocks,direction)
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
                    bumper.x = -2
                elif tempx >= WINDOWWIDTH - (BUMPERWIDTH/2):
                    bumper.x = 520
                #the 63 centers it - the sprite is approximately 125 pixels wide
                else:
                    bumper.x = tempx-(BUMPERWIDTH/2)
        
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(BACKGROUND,(0,0))
        DISPLAYSURF.blit(bumper.img,(bumper.x,bumper.y))
        DISPLAYSURF.blit(ball.img, (ball.x,ball.y))
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
    Screens.drugScreen()
    while True:
        Screens.startScreen()
        runGame()

if __name__ == '__main__':
    main()
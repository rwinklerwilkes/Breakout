import pygame, sys, math

pygame.init()

#set the FPS
FPS = 30
fpsClock = pygame.time.Clock()

#set the proper mouse values
LEFT = 1
RIGHT = 3

#set up the window, set the background
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BLOCKSROW = 10 #number of blocks in a row
BLOCKSCOLUMN = 5 #number of blocks in a column
BLOCKWIDTH = 35 #sprite is 40 pixels by 40 pixels
BLOCKHEIGHT = 35
BALLWIDTH = 25
BALLHEIGHT = 25
#margin from the sides in pixels
XMARGIN = int((WINDOWWIDTH - (BLOCKSROW*BLOCKWIDTH))/2)
YMARGIN = 80 #margin from the top in pixels
WHITE = (255,255,255)
BUMPERWIDTH = 125
BUMPERHEIGHT = 35

#this method checks to see whether the ball has hit the bumper
def hitBumper(ballx, bally,bumperx,bumpery,direction):
    #bumperx is the left coordinate of the bumper
    #ballx is the left coordinate of the ball
    if ballx>=bumperx and (ballx<=(bumperx + BUMPERWIDTH) and (direction=='downleft' or direction=='downright')):
        #bally should be approaching from the top, so its y-coordinate will be LESS than the y-coordinate of the bumper
        if bally-bumpery >=-15 and bally-bumpery<=0:
            return True
    return False

def generateBlocks():
    #the blocks array will be false if it HAS been hit
    #so, we'll draw it if it's true
    blocks = [[True for boxx in range(BLOCKSROW)] for boxy in range(BLOCKSCOLUMN)]
    return blocks

def drawBlocks(blocks):
    blockImg = pygame.image.load('block.png')
    for boxy in range(BLOCKSCOLUMN):
        for boxx in range(BLOCKSROW):
            if blocks[boxy][boxx]==True:
                left, top = topLeftCoords(boxx,boxy)
                DISPLAYSURF.blit(blockImg,(left,top))
    

def topLeftCoords(blockx,blocky):
    #blockx should be in the range of 0 to BLOCKSROW
    #blocky should be in the range of 0 to BLOCKSCOLUMN
    left = blockx*BLOCKWIDTH + XMARGIN
    top = blocky*BLOCKHEIGHT + YMARGIN
    return left, top

#this method will someday check to see whether the ball has hit a block
def hitBlock(ballx, bally, blocks,direction):
    for boxy in range(BLOCKSCOLUMN):
        for boxx in range(BLOCKSROW):
            if blocks[boxy][boxx]==True:
                left, top = topLeftCoords(boxx,boxy)
                blockRect = pygame.Rect(left,top,BLOCKWIDTH,BLOCKHEIGHT)
                ballRect = pygame.Rect(ballx,bally,BALLWIDTH,BALLHEIGHT)
                if blockRect.colliderect(ballRect):
                    direction = blockDirectionChange(ballx,bally,left,top,direction)
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

def blockDirectionChange(ballx, bally, leftBox, topBox, direction):
    blockRect = pygame.Rect(leftBox,topBox,BLOCKWIDTH,BLOCKHEIGHT)
    ballRect = pygame.Rect(ballx,bally,BALLWIDTH,BALLHEIGHT)
    #if the ball is going down and to the right
    #it can hit the left or the top
    if direction == 'downright':
        if topDist(ballRect,blockRect) >= rightDist(ballRect,blockRect):
            direction = 'upright'
        else:
            direction = 'downleft'
    #if the ball is going down and to the left
    #it can hit the right or the top
    elif direction == 'downleft':
        if topDist(ballRect,blockRect) >= leftDist(ballRect,blockRect):
            direction = 'upleft'
        else:
            direction = 'downright'
    #if the ball is going up and to the right
    #it can hit the left or the bottom
    elif direction == 'upright':
        if bottomDist(ballRect,blockRect) >= leftDist(ballRect,blockRect):
            direction = 'downright'
        else:
            direction = 'upleft'
    #if the ball is going up and to the left
    #it can hit the right or the bottom
    elif direction == 'upleft':
        if bottomDist(ballRect,blockRect) >= rightDist(ballRect,blockRect):
            direction = 'downleft'
        else:
            direction = 'upright'
    return direction

def moveOrDirectionChange(ballx, bally, bumperx, bumpery, direction):
    if hitBumper(ballx, bally, bumperx, bumpery,direction):
        if direction == 'downright':
            direction = 'upright'
        elif direction == 'downleft':
            direction = 'upleft'
    if direction== 'downright':
        ballx+=speed
        bally+=speed
        if ballx>=620:
            direction='downleft'
        elif bally>=460:
            direction='upright'
    elif direction=='downleft':
        ballx-=speed
        bally+=speed
        if ballx<=-5:
            direction='downright'
        elif bally>=460:
            direction='upleft'
    elif direction== 'upright':
        ballx+=speed
        bally-=speed
        if ballx>=620:
            direction='upleft'
        elif bally<=-5:
            direction='downright'
    elif direction== 'upleft':
        ballx-=speed
        bally-=speed
        if ballx<=-5:
            direction='upright'
        elif bally<=-5:
            direction='downleft'
    
    return ballx, bally, direction

def main():
    global DISPLAYSURF
    global speed
    speed = 5
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BACKGROUND = pygame.image.load('breakout_bg.png')
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    #define the beginning ball values
    ballImg = pygame.image.load('ball.png')
    ballx = 320
    bally = 360
    direction = 'downleft'
    start = False
    #add the ball to the screen
    DISPLAYSURF.blit(ballImg, (ballx,bally))
    
    #define the beginning bumper values
    bumperImg = pygame.image.load('bumper.png')
    bumperx = 320
    bumpery = 430
    #add the bumper to the screen
    DISPLAYSURF.blit(bumperImg,(bumperx,bumpery))

    #define the beginning block values
    blocks = generateBlocks()
    #draw blocks to the screen
    drawBlocks(blocks)
    
    while True:
        if start:
            ballx,bally,direction = moveOrDirectionChange(ballx,bally,bumperx,bumpery,direction)
            blockHitY, blockHitX, direction = hitBlock(ballx,bally,blocks,direction)
            if blockHitX>=0 and blockHitY>=0:
                blocks[blockHitY][blockHitX] = False

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
        drawBlocks(blocks)
            
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()

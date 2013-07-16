import pygame, sys, math



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
#shorter constants so I don't have to type the strings
DR = 'downright'
DL = 'downleft'
UR = 'upright'
UL = 'upleft'

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

def gameOver():
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
    pygame.time.wait(1000)
    return

def blockDirectionChange(ballx, bally, leftBox, topBox, direction):
    blockRect = pygame.Rect(leftBox,topBox,BLOCKWIDTH,BLOCKHEIGHT)
    ballRect = pygame.Rect(ballx,bally,BALLWIDTH,BALLHEIGHT)
    #if the ball is going down and to the right
    #it can hit the left or the top
    if direction == DR:
        if topDist(ballRect,blockRect) >= rightDist(ballRect,blockRect):
            direction = UR
        else:
            direction = DL
    #if the ball is going down and to the left
    #it can hit the right or the top
    elif direction == DL:
        if topDist(ballRect,blockRect) >= leftDist(ballRect,blockRect):
            direction = UL
        else:
            direction = DR
    #if the ball is going up and to the right
    #it can hit the left or the bottom
    elif direction == UR:
        if bottomDist(ballRect,blockRect) >= leftDist(ballRect,blockRect):
            direction = DR
        else:
            direction = UL
    #if the ball is going up and to the left
    #it can hit the right or the bottom
    elif direction == UL:
        if bottomDist(ballRect,blockRect) >= rightDist(ballRect,blockRect):
            direction = DL
        else:
            direction = UR
    return direction

def moveOrDirectionChange(ballx, bally, bumperx, bumpery, direction):
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
    BACKGROUND = pygame.image.load('breakout_bg.png')
    ballImg = pygame.image.load('ball.png')
    bumperImg = pygame.image.load('bumper.png')
    ballx = 320
    bally = 360
    DISPLAYSURF.blit(ballImg, (ballx,bally))
    direction = 'downleft'
    start = False
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    #define the beginning ball values
    ballImg = pygame.image.load('ball.png')
    bumperImg = pygame.image.load('bumper.png')
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
            ballx,bally,direction = moveOrDirectionChange(ballx,bally,bumperx,bumpery,direction)
            #if the ball hit the bottom of the screen, game over
            if direction == -1:
                gameOver()
                return
            blockHitY, blockHitX, direction = hitBlock(ballx,bally,blocks,direction)
            if blockHitX>=0 and blockHitY>=0:
                blocks[blockHitY][blockHitX] = False
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
        drawBlocks(blocks)
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    pygame.init()
    global DISPLAYSURF
    global speed
    speed = 5
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    while True:
        runGame()
    

if __name__ == '__main__':
    main()

import pygame
import sys
import math
import time
import datetime
import os
#cPickle is used to serialize the high scores
try:
    import cPickle as pickle
except:
    import pickle

#set the FPS
FPS = 30
fpsClock = pygame.time.Clock()

#set the proper mouse values
LEFT = 1
RIGHT = 3

#set up the window, set the background
BACKGROUND = pygame.image.load('breakout_bg.png')
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
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

#Dict to match alphanumeric characters to their filenames
ALPHA = {}
for x in range(65,91):
    a = str(chr(x))
    ALPHA[a] = 'Alphabet/' + a + '.png'
for x in range(10):
    ALPHA[str(x)] = 'Alphabet/' + str(x) + '.png'

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
    GAME = pygame.image.load("Game.png")
    OVER = pygame.image.load("over.png")
    game_rect = GAME.get_rect()
    game_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/4)
    over_rect = OVER.get_rect()
    over_rect.midtop = (WINDOWWIDTH/2, WINDOWHEIGHT/4 + game_rect.height + 15)
    DISPLAYSURF.blit(GAME,game_rect)
    DISPLAYSURF.blit(OVER,over_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    return

def drugScreen():
    #alpha info from:
    #http://stackoverflow.com/questions/12879225/pygame-applying-transparency-to-an-image-with-alpha
    DRUGS = pygame.image.load("drugs.png").convert(24)
    DRUGS.set_alpha(0)
    FADEDURATION = 1.0 #1 second fade in
    HOLDDURATION = 2 #2 second hold at the opaque screen
    #I have to change this method to use pygame's timing function
    #in order to keep consistent with other code
    start_time = time.clock()
    #fade in
    ratio = 0.0 #alpha value as a float, ranges from 0 to 1
    while ratio < 1.0:
        current_time = time.clock()
        ratio = (current_time-start_time)/FADEDURATION
        if ratio > 1.0: #oops, went too far!
            ratio = 1.0
        #alpha value - 0 is completely transparent, 255 completely opaque
        DRUGS.set_alpha(ratio*255)
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(DRUGS,(0,0))
        pygame.display.update()
    #wait for a couple seconds
    pygame.time.wait(HOLDDURATION*1000)
    #then fade out
    start_time = time.clock()
    ratio = 0.0 #alpha value as a float, ranges from 0 to 1
    while ratio < 1.0:
        current_time = time.clock()
        ratio = (current_time-start_time)/FADEDURATION
        if ratio > 1.0: #oops, went too far!
            ratio = 1.0
        #alpha value - 0 is completely transparent, 255 completely opaque
        DRUGS.set_alpha((1.0-ratio)*255)
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(DRUGS,(0,0))
        pygame.display.update()
    return

def startScreen():
    INTRO = pygame.image.load("breakout_intro.png")
    IND = pygame.image.load("pointer.png")
    START = 0
    QUIT = 1
    #PLACES defines the two coordinate positions that the pointer can be in
    #the first tuple is the Start Game position, the second tuple is the Exit position
    PLACES = [(220,265),(220,320)]
    #visible indicates if the pointer is currently visible or not
    visible = True
    #pos indicates which item the pointer is by, starting with 0
    position = 0
    #this time will control whether the pointer is visible or not
    start_time = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #we don't want to go past the possible position values
                #so this limits it to 0 or 1
                if event.key==pygame.K_DOWN:
                    position = (position+1)%2
                elif event.key==pygame.K_UP:
                    position = (position-1)%2
                elif event.key==pygame.K_RETURN:
                    #if they want to start, return to main
                    if position==START:
                        return
                    #if they want to quit, let them!
                    elif position==QUIT:
                        pygame.quit()
                        sys.exit()
        current_time = pygame.time.get_ticks()
        if (current_time - start_time) >= 500:
            visible = not visible
            start_time = current_time
        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(INTRO,(0,0))
        if visible:
            DISPLAYSURF.blit(IND,PLACES[position])
        pygame.display.update()

def highScoreScreen(score):
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    hsList = readHighScores()
    ind = checkScore(hsList,score)
    for x in range(HSROWS):
        writeScore(hsList[x],x)
        pygame.display.update()
    if ind>=0:
        #prompt for initials
        for x in range(HSROWS):
            writeScore(hsList[x],x)
        pygame.display.update()
        #update the list
        #display the scores
        #write the new scores
        #return
    pygame.time.wait(5000)
    return

def writeScore(score, row):
    dash = pygame.image.load("Alphabet/dash.png")
    #deal with the initials first
    y = (row+1)*HSMARGIN + row*HSHEIGHT
    x = 10 #start 10 pixels from the left part of the screen
    for z in score[0]:
        letter = pygame.image.load(ALPHA[z])
        DISPLAYSURF.blit(letter,(x,y))
        x += (HSHEIGHT-5)
    x+=60
    counter = 0
    for z in str(score[1]):
        number = pygame.image.load(ALPHA[z])
        DISPLAYSURF.blit(number,(x,y))
        counter+=1
        x += (HSHEIGHT-5)
    if counter<5:
        x+= (HSHEIGHT-5)*(5-counter)
    x+=30
    #Uppercase because I only have uppercase letters
    for z in score[2].upper():
        if z==' ':
            DISPLAYSURF.blit(dash,(x,y+3))
            x+=10
        else:
            letter = pygame.image.load(ALPHA[z])
            DISPLAYSURF.blit(letter,(x,y))
            x+= (HSHEIGHT-15)
    return

def readHighScores():
    #if the file doesn't yet exist, create it
    #the high scores will be stored in CSV, and will be passed as
    #a list of tuples, each containing 3 initials and a date
    if not os.path.isfile(SCORES_FILE):
        today_date = datetime.date.today()
        hs_list = [("AEB","1000",today_date.strftime("%m %d %Y")) for x in range(10)]
        writeHighScores(hs_list)
        return hs_list
    with open(SCORES_FILE, 'rb') as f:
        scores = pickle.load(f)
    return scores


def writeHighScores(scores):
    with open(SCORES_FILE,'wb') as f:
        pickle.dump(scores,f)

def checkScore(high_scores, score):
    #this checks to see if the user got a high score
    #scores are stored as a string in the 2nd spot in the tuple
    #in this method, score will be an integer
    hs = -1
    #local copy of the scores, don't want to mess anything up
    lowest = None
    lowest = min(high_scores,key=lambda item: int(item[1]))
    if score > int(lowest[1]):
        hs = index(lowest)
    return hs

def updateScores(high_scores, score, index):
    temp_high_scores = high_scores[:]
    temp_high_scores.insert(index,score)
    #if we added one to the list, we want the list to stay as 10
    temp_high_scores.pop()
    return temp_high_scores

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
    ballImg = pygame.image.load('ball.png')
    bumperImg = pygame.image.load('bumper.png')
    scoreImage = pygame.image.load('score.png')
    scoreFont = pygame.font.Font('freesansbold.ttf',37)
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
                highScoreScreen(score)
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
    global DISPLAYSURF
    global speed
    speed = 5
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    drugScreen()
    while True:
        startScreen()
        runGame()
    

if __name__ == '__main__':
    main()

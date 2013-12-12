import time
import datetime
import os
import sys
from Constants import *
#cPickle is used to serialize the high scores
try:
    import cPickle as pickle
except:
    import pickle
__author__ = 'Rich'

WHITE = (255,255,255)

def startScreen():
    INTRO = pygame.image.load("Images/breakout_intro.png")
    IND = pygame.image.load("Images/pointer.png")
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

def gameOver():
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

def drugScreen():
    #alpha info from:
    #http://stackoverflow.com/questions/12879225/pygame-applying-transparency-to-an-image-with-alpha
    DRUGS = pygame.image.load("Images/drugs.png").convert(24)
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

#fix_initials writes the list of initials to the screen
def fix_initials(hsList, userScore,ind):
    counter = 0
    for x in hsList[:ind]:
        writeScore(x,counter)
        counter+=1
        #using # as a sentinel, I just want to write empty spaces for now
    writeScore(userScore,ind)
    counter+=1
    for x in hsList[ind+1:-1]:
        writeScore(x,counter)
        counter+=1

#This method controls the writing of the high scores to the screen
def highScoreScreen(score):
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(BACKGROUND,(0,0))
    hsList = readHighScores()
    ind = checkScore(hsList,score)
    today_date = datetime.date.today().strftime("%m %d %Y")
    if ind>=0:
        fix_initials(hsList,("###",score,today_date), ind)
        initials = ""
        entered = False
        while not entered:
            DISPLAYSURF.fill(WHITE)
            DISPLAYSURF.blit(BACKGROUND,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #if the user hits enter, accept their high score initials
                    #if the user hits backspace, delete one initial
                    #if the user CAN enter more initials, let them
                    if event.key==pygame.K_RETURN:
                        entered = True
                    elif event.key==pygame.K_BACKSPACE:
                        if len(initials)>0:
                            initials = initials[:-1]
                    elif event.unicode.isalpha() and len(initials)<3:
                        initials += event.unicode
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            counter = 0
            while len(initials)<3:
                initials+="#"
                counter+=1
            fix_initials(hsList, (initials.upper(), score, today_date), ind)
            if counter > 0:
                initials = initials[:-counter]
            pygame.display.update()
            fpsClock.tick(FPS)
        hsList = updateScores(hsList,(initials.upper(), score, today_date),ind)
        writeHighScores(hsList)
    else:
        for x in range(HSROWS):
            writeScore(hsList[x],x)
        pygame.display.update()
    pygame.time.wait(3000)
    return

#This method writes the individual high scores to the screen
def writeScore(score, row):
    dash = pygame.image.load("Alphabet/dash.png")
    #deal with the initials first
    HSHEIGHT = 40 #height in pixels of each letter in the high score
    HSMARGIN = 5 #margin between scores
    y = (row+1)*HSMARGIN + row*HSHEIGHT
    x = 10 #start 10 pixels from the left part of the screen
    #score[0] holds the initials, e.g. AAA
    ALPHA = {}
    for x in range(65,91):
        a = str(chr(x))
        ALPHA[a] = 'Alphabet/' + a + '.png'
    for x in range(10):
        ALPHA[str(x)] = 'Alphabet/' + str(x) + '.png'
    for z in score[0]:
        #dealing with displaying the score before initials are typed
        # '#' is a sentinel value - if we come across that, then
        #we just want to put an "empty letter" there
        if z=="#":
            x+=(HSHEIGHT-5)
        else:
            letter = pygame.image.load(ALPHA[z])
            DISPLAYSURF.blit(letter,(x,y))
            x += (HSHEIGHT-5)
    x+=60
    counter = 0
    #score[1] holds the actual score, e.g. 1430
    for z in str(score[1]):
        number = pygame.image.load(ALPHA[z])
        DISPLAYSURF.blit(number,(x,y))
        counter+=1
        x += (HSHEIGHT-5)
    if counter<5:
        x+= (HSHEIGHT-5)*(5-counter)
    x+=30
    #Uppercase because I only have uppercase letters
    #score[2] holds the date
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
    SCORES_FILE = "hs.dat" #file in which to store high scores
    if not os.path.isfile(SCORES_FILE):
        today_date = datetime.date.today()
        hs_list = [("AEB","1000",today_date.strftime("%m %d %Y")) for x in range(10)]
        writeHighScores(hs_list,SCORES_FILE)
        return hs_list
    with open(SCORES_FILE, 'rb') as f:
        scores = pickle.load(f)
    return scores


def writeHighScores(scores,SCORES_FILE):
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
        hs = high_scores.index(lowest)
    return hs

def updateScores(high_scores, score, index):
    temp_high_scores = high_scores[:]
    temp_high_scores.insert(index,score)
    #if we added one to the list, we want the list to stay as 10
    temp_high_scores.pop()
    return temp_high_scores
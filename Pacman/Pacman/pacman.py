#pacman.py
#Sulayman and Jathushan 
from pygame import *
from pprint import*
from random import choice
from math import *

def running():
    ''' check the event queue for an quit as well as the keyboard
        for the escape key. return false if either are seen true
        if we make it to the end.
    '''

    for evnt in event.get():
        if evnt.type == QUIT:
            return False
        
    keys = key.get_pressed()
    if keys[27]:
        return False
    return True

def wallCheck(x,y,mask):                                 
    'checks for pixels and colors'

    if x-mazedistx<0 or x-mazedistx >= mask.get_width() or y-mazedisty<0 or y-mazedisty >= mask.get_height():#checks for wall
        return False                                                                                                                                                                            #first checks if x and y coordinates are bigger or smaller than 
    else:                                                                                                                                                                                           #the picture
        return mask.get_at((x-mazedistx,y-mazedisty))[ :3] != WALL                                                                                      #then for color of mask
    #userinput
def valid(maze, moves):
    for x, pos in enumerate(maze[0]):
        if pos == "S":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1 

        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == 1):
            return False

    return True


def findEnd(maze, moves):
    for x, pos in enumerate(maze[0]):
        if pos == "S":
            start = x

    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1

        elif move == "R":   
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1

    if maze[j][i] == "F":
        print("Found: " + moves)
        #printMaze(maze, moves)
        return True

    return False

def movePick(pacman, playerspeed):
    'move player'                                                                                                    

    if keys[K_RIGHT]:                   #before changing [MOVE] x and y must be on a grid, and there cant be a wall
        if (pacman[X] - mazedistx) %squarewidth == 0 and (pacman[Y]-mazedisty) %squarewidth == 0 and wallCheck(pacman[X]+squarewidth+playerspeed,pacman[Y]+pacrad, mazemask):     
            pacman[MOVE] = right  #subtracting distance from the maze and checking 0 remainder so its on a grid point.              Pacman blitts on top right corner so checking tip of pacman where
        else:                                                                                                                                                                                       #he faces, add width of the grid quadrant to x value and radius      
            pacman[NXTMOVE] = right #queueing a direction till possible                                                                                         #to y value 
    if keys[K_LEFT]:
        if (pacman[X] - mazedistx) %squarewidth == 0 and (pacman[Y]-mazedisty) %squarewidth == 0 and wallCheck(pacman[X]-playerspeed,pacman[Y]+pacrad, mazemask): 
            pacman[MOVE] = left
        else:
            pacman[NXTMOVE] = left
    if keys[K_DOWN]:
        if (pacman[X]-mazedistx) %squarewidth == 0 and (pacman[Y]-mazedisty) %squarewidth == 0 and wallCheck(pacman[X]+pacrad,pacman[Y]+playerspeed+squarewidth, mazemask):
            pacman[MOVE] = down
        else:
            pacman[NXTMOVE] = down
    if keys[K_UP]:
        if (pacman[X]-mazedistx) %squarewidth == 0 and (pacman[Y]-mazedisty) %squarewidth == 0 and wallCheck(pacman[X]+pacrad,pacman[Y]-playerspeed-pacrad, mazemask):
            pacman[MOVE] = up
        else:
            pacman[NXTMOVE] = up

def movePacman(pacman,playerspeed):
    'moves pacman based on direction and walls'
    
    if pacman[MOVE] == right and wallCheck(pacman[X]+squarewidth+playerspeed,pacman[Y]+pacrad, mazemask): #check for walls each time movement is made
        pacman[X] += playerspeed
    elif pacman[MOVE] == left and wallCheck(pacman[X]-playerspeed,pacman[Y]+pacrad, mazemask):
        pacman[X] -= playerspeed
    elif pacman[MOVE] == up and wallCheck(pacman[X]+pacrad,pacman[Y]-playerspeed, mazemask):
        pacman[Y] -= playerspeed
    elif pacman[MOVE] == down and wallCheck(pacman[X]+pacrad,pacman[Y]+squarewidth+playerspeed, mazemask):
        pacman[Y] += playerspeed
    else:
        pacman[FRAME] = 1 #if no movement deducting a frame
    pacman[FRAME] = pacman[FRAME]+.5
    if pacman[FRAME] == 4:
        pacman[FRAME] = 0
    if pacman[MOVE]==right and pacman [X] == 602:#teleporting to ther side 
        pacman[X] = 65
    if pacman[MOVE] == left and pacman[X] == 65:
        pacman[X] = 602

def nxtMove (pacman):
    'checks queued direction variable if available'

    if pacman[NXTMOVE] == up and wallCheck(pacman[X]+pacrad,pacman[Y]-playerspeed, mazemask) and (pacman[X]-mazedistx) %30 == 0 and (pacman[Y]-mazedisty) %30 == 0: 
        pacman[MOVE] = up                                   #checking dist
    if pacman[NXTMOVE] == down and wallCheck(pacman[X]+pacrad,pacman[Y]+squarewidth+playerspeed, mazemask) and (pacman[X]-mazedistx) %30 == 0 and (pacman[Y]-mazedisty) %30 == 0:
        pacman[MOVE] = down
    if pacman[NXTMOVE] == right and wallCheck(pacman[X]+squarewidth+playerspeed,pacman[Y]+pacrad, mazemask) and (pacman[X]-mazedistx) %30 == 0 and (pacman[Y]-mazedisty) %30 == 0:
        pacman[MOVE] = right
    if pacman[NXTMOVE] == left and wallCheck(pacman[X]-playerspeed, pacman[Y]+pacrad, mazemask) and (pacman[X]-mazedistx) %30 == 0 and (pacman[Y]-mazedisty) %30 == 0:
        pacman[MOVE] = left

def moveGhost(ghosts, ghostspeed): #ghosts = [350,320,(randint(0,3)]
    'moves ghosts randomly'
    global startX
    global startY
    dirchoice = [0,1,2,3]
    #moves indices for pacman list
    for ghost in range(len(ghosts)):
        distX = abs(ghosts[ghost][X]-startX)
        distY = abs(ghosts[ghost][Y]-startY)
        if ghosts[ghost][MOVE] == right and wallCheck(ghosts[ghost][X]+pacrad+ghostspeed,ghosts[ghost][Y], ghostmask):
            ghosts[ghost][X] += ghostspeed
        elif ghosts[ghost][MOVE] == left and wallCheck(ghosts[ghost][X]-pacrad-ghostspeed,ghosts[ghost][Y], ghostmask):
            ghosts[ghost][X] -= ghostspeed
        elif ghosts[ghost][MOVE] == up and wallCheck(ghosts[ghost][X],ghosts[ghost][Y]-pacrad-ghostspeed, ghostmask):
            ghosts[ghost][Y] -= ghostspeed
        elif ghosts[ghost][MOVE] == down and wallCheck(ghosts[ghost][X],ghosts[ghost][Y]+pacrad+ghostspeed, ghostmask):
            ghosts[ghost][Y] += ghostspeed
        if ghosts [ghost][MOVE] == right:
            if wallCheck(ghosts[ghost][X]+pacrad+ghostspeed,ghosts[ghost][Y],ghostmask) and (ghosts[ghost][X]-80) %30 == 0 and (ghosts[ghost][Y]-50) %30 == 0 and distX >= 120 or wallCheck(ghosts[ghost][X]+pacrad+ghostspeed,ghosts[ghost][Y],ghostmask) == False:
                dirchoice.remove(2)
                ghosts [ghost][MOVE] = choice(dirchoice)
                startX = ghosts[ghost][X]
                startY = ghosts[ghost][Y]
        if ghosts[ghost][MOVE] == up:
            if wallCheck(ghosts[ghost][X],ghosts[ghost][Y]-pacrad-ghostspeed,ghostmask) and (ghosts[ghost][X]-80) %30 == 0 and (ghosts[ghost][Y]-50) %30 == 0 and distY >= 120 or wallCheck(ghosts[ghost][X],ghosts[ghost][Y]-pacrad-ghostspeed, ghostmask) == False:
                dirchoice.remove(1)
                ghosts [ghost][MOVE] = choice(dirchoice)
                startX = ghosts[ghost][X]
                startY = ghosts[ghost][Y]
                dirchoice.remove
        if ghosts[ghost][MOVE] == down:
            if wallCheck(ghosts[ghost][X],ghosts[ghost][Y]+pacrad+ghostspeed,ghostmask) and (ghosts[ghost][X]-80) %30 == 0 and (ghosts[ghost][Y]-50) %30 == 0 and distY >= 120 or wallCheck(ghosts[ghost][X],ghosts[ghost][Y]+pacrad+ghostspeed,ghostmask) == False:
                dirchoice.remove(3)
                ghosts [ghost][MOVE] = choice(dirchoice)
                startX = ghosts[ghost][X]
                startY = ghosts[ghost][Y]
        if ghosts[ghost][MOVE] == left:
            if wallCheck(ghosts[ghost][X]-pacrad-ghostspeed,ghosts[ghost][Y],ghostmask) and (ghosts[ghost][X]-80) %30 == 0 and (ghosts[ghost][Y]-50) %30 == 0 and distX>= 120 or wallCheck(ghosts[ghost][X]-pacrad-ghostspeed,ghosts[ghost][Y],ghostmask) == False:
                dirchoice.remove(0)
                ghosts [ghost][MOVE] = choice(dirchoice)
                startX = ghosts[ghost][X]
                startY = ghosts[ghost][Y]
        #dirchoice.remove(ghosts[ghost][MOVE])
        dirchoice = [0,1,2,3]

    
def ghosthit(ghosts,pacman):
    'checks collisions with ghosts by seeing if same grid spot'
    for g in range (len(ghosts)):
        if coordReverse(ghosts[g][X],ghosts[g][Y], ghosts[g][MOVE]) == coordReverse(pacman[X],pacman[Y], pacman[MOVE]) and pacman[LIVES] > 0:
            return True
    return False

                   
    
def coordReverse(x,y,move):
    nx = (x - 65) //30
    ny = (y - 35) //30
    if pacman[move] == right or ghosts[move] == right:
        nx += 1
    if pacman [move] == down or ghosts[move] == down:
        ny += 1
    return (nx,ny)
def checkCoinhits(pacman,coinList,coinList2):
    'checks pacman coin collisions and modifies list accordingly'

    global CoinCounter
    #get pacman 2dlist coordinate
    pacXj = (pacman[X]-65)//30
    pacYi = (pacman[Y]-35)//30
    if pacman[MOVE] == right:
        pacXj += 1
    if pacman[MOVE] == down:
        pacYi+=1
    if pacman[MOVE] == right and (pacman[X]+squarewidth,pacman[Y]+pacrad) == coinList2[pacYi][pacXj] and coinList[pacYi][pacXj] == 1 or pacman[MOVE] == left and (pacman[X],pacman[Y]+pacrad) == coinList2[pacYi][pacXj] and coinList[pacYi][pacXj] == 1 or pacman[MOVE] == down and (pacman[X]+pacrad,pacman[Y]+squarewidth) == coinList2[pacYi][pacXj] and coinList[pacYi][pacXj] == 1 or pacman[MOVE] == up and (pacman[X]+pacrad, pacman[Y]) == coinList2[pacYi][pacXj] and coinList[pacYi][pacXj] == 1:
        coinList[pacYi][pacXj] = 0
        CoinCounter += 10
def listConvert(x,y):
    'converting the index on grid to coordinates on screen'

    x =30*x+80#each square is 30x30 p, so multiply index by pixels and add distance of grid from outside of screen, 65 anis 30d 15 so its central
    y = 30*y+50#adding 50 because 35(distance from screen vertically)+15
    return (x,y)
    #draweverything

def empty(List):
    'checks if the given list has a certain value in it'
    for i in range(len(List)):
        for j in range(len(List[i])):
            if List[i][j] != 0:
                return False
    return True

def loadScreen():
    "Blits the loading screen"

    loadscreenPic = "loadingscreen.jpg"
    loadscreen = image.load(loadscreenPic)
    LSP = transform.smoothscale(loadscreen,(WIDTH,HEIGHT))
    screen.blit(LSP,(0,0))
    JTSS = mainfont.render("Sulayman and Jathushan's Pacman Game",True,(WHITE))            #the loading/introduction screen
    screen.blit(JTSS,(40,120))
    PRSP = mainfont.render("Press Space to Continue",True,(WHITE))
    screen.blit(PRSP,(160,600))

def menu():
    "The menu page's code"
    
    draw.rect(screen,(0,0,0),(0,0,800,700))


    draw.rect(screen,(255,204,0),(settingsRect))
    settingsPic = "settings.png"
    settings = image.load(settingsPic)
    SETP = transform.scale(settings,(50,50))                                         #Setting up the work for the layout of the menu
    screen.blit(SETP,(740,10))

    draw.rect(screen,(255,204,0),(instructionRect))
    instrPic = image.load('question.png')
    INSTRP = transform.scale(instrPic,(50,50))
    screen.blit(INSTRP,(740,70))

    draw.rect(screen,(255,204,0),(playRect))
    playPic = playfont.render("PLAY",True,(WHITE))
    screen.blit(playPic,(260,115))

    draw.rect(screen,(255,204,0),(levelsRect))
    levelsPic = customfont.render("LEVELS",True,(WHITE))
    screen.blit(levelsPic,(255,330))
    
    draw.rect(screen,(255,204,0),(customRect))
    customPic = customfont.render("CUSTOMS",True,(WHITE))
    screen.blit(customPic,(230,530))

def instruction():
    "The instructions page's code"
    
    draw.rect(screen,(0,0,0),(0,0,800,700))
    
    draw.rect(screen,WHITE,(homeRect))
    HOMP = transform.scale(home,(50,50))
    screen.blit(HOMP,(10,10))
    
    instructionPic = instrfont.render("INSTRUCTIONS",True,(WHITE))
    screen.blit(instructionPic,(200,50))
    
    Ainstructions = mainfont.render("Arrow Key Pad to Move in Game",True,(WHITE))
    screen.blit(Ainstructions,(110,150))
    
    C1instructions = mainfont.render("Customize characters in",True,(WHITE))                #Explaining how to play the game and what you can do to make the game
    screen.blit(C1instructions,(160,200))                                                           #      more appealing to yourself
    
    C2instructions = mainfont.render("customizations page",True,(WHITE))
    screen.blit(C2instructions,(200,230))
    
    G1instructions = mainfont.render("Collect all the coins",True,(WHITE))
    screen.blit(G1instructions,(180,300))
    
    G2instructions = mainfont.render("without getting eaten by ghosts",True,(WHITE))
    screen.blit(G2instructions,(95,350))
    
    draw.rect(screen,WHITE,(250,450,300,150))
    arrowsPic="arrows.png"
    arrows = image.load(arrowsPic)
    ARRP = transform.scale(arrows,(300,200))
    screen.blit(ARRP,(250,450))
    
    DES1P = transform.scale(design1,(100,200))
    screen.blit(DES1P,(100,400))
    
    DES2P = transform.scale(design2,(100,200))
    screen.blit(DES2P,(600,400))
    
def settings():
    "The settings page's code"
    
    draw.rect(screen,(0,0,0),(0,0,800,700))
    
    ONcolor = (0,225,0)
    ONtext = (0,255,0)
    OFFcolor = (255,0,0)
    OFFtext = (200,0,0)

    draw.rect(screen,WHITE,(homeRect))
    HOMP = transform.scale(home,(50,50))
    screen.blit(HOMP,(10,10))
    
    draw.rect(screen,(255,204,0),(50,100,400,75))
    draw.rect(screen,(ONcolor),(OnRect))
    draw.rect(screen,(OFFcolor),(OffRect))
    
    MUSIC = playfont.render("MUSIC:",True,(WHITE))
    screen.blit(MUSIC,(57,102))
    ON = instrfont.render("ON",True,(ONtext))
    screen.blit(ON,(495,122))
    OFF = instrfont.render("OFF",True,(OFFtext))
    screen.blit(OFF,(630,122))

def custom():
    "The custom screen's code"
    
    draw.rect(screen,(0,0,0),(0,0,800,700))
    
    draw.rect(screen,WHITE,(homeRect))
    HOMP = transform.scale(home,(50,50))
    screen.blit(HOMP,(10,10))
    
    custom = instrfont.render("CUSTOMS",True,(WHITE))
    screen.blit(custom,(275,10))
     
    cus1exp = mainfont.render("PICK THE MAZE AND OR PACMAN",True,(WHITE))                   #Code for the work that tells the player the options
    screen.blit(cus1exp,(125,80))                                                                       # they have to choose from
    
    cus2exp = mainfont.render("OF YOUR CHOICE",True,(WHITE))
    screen.blit(cus2exp,(250,105))
    
    cho1 = mainfont.render("MAZE",True,(WHITE))
    screen.blit(cho1,(10,200))
    
    cho2 = mainfont.render("PACMAN",True,(WHITE))
    screen.blit(cho2,(10,350))

    
    Maze = image.load("maze2.png")
    M2P = transform.scale(Maze,(75,75))
    screen.blit(M2P,(75,250))

    MazePurple = image.load("mazepurple.png")                                               # Showing the user the different mazes
    MPP = transform.scale(MazePurple,(75,75))                                               #         they can choose from
    screen.blit(MPP,(175,250))
    
    MazeOrange = image.load("mazeorange.png")
    MOP = transform.scale(MazeOrange,(75,75))
    screen.blit(MOP,(275,250))

    MazeTurquiose = image.load("mazeturqoise.png")
    MTP = transform.scale(MazeTurquiose,(75,75))
    screen.blit(MTP,(375,250))

    MazeGreen = image.load("mazegreen.png")
    MGP = transform.scale(MazeGreen,(75,75))
    screen.blit(MGP,(475,250))
    
    MazeSaad = image.load("mazesaad.png")
    MSP = transform.scale(MazeSaad,(75,75))
    screen.blit(MSP,(575,250))

    MazeMix = image.load("mazemix.png")
    MMP = transform.scale(MazeMix,(75,75))
    screen.blit(MMP,(675,250))

    draw.rect(screen,(255,242,0),(ypacRect))                                                #Showing the user the different colours of Pacman they can play with
    
    draw.rect(screen,(187,248,249),(bpacRect))

    draw.rect(screen,(163,73,164),(ppacRect))

    draw.rect(screen,(0,255,0),(gpacRect))

    draw.rect(screen,(245,47,151),(mpacRect))

    draw.rect(screen,WHITE,(wpacRect))

def levels():
    'the screen which appears and lets you change between levels'

    draw.rect(screen,(0,0,0),(0,0,800,700))

    draw.rect(screen,WHITE,(homeRect))
    HOMP = transform.scale(home,(50,50))
    screen.blit(HOMP,(10,10))
    
    draw.rect(screen,(255,204,0),(playRect))
    LVL1 = customfont.render("LEVEL 1",True,(WHITE))
    screen.blit(LVL1,(232,130))
    
    draw.rect(screen,(255,204,0),(levelsRect))
    LVL2 = customfont.render("LEVEL 2",True,(WHITE))
    screen.blit(LVL2,(232,330))
    
    draw.rect(screen,(255,204,0),(customRect))
    LVL3 = customfont.render("LEVEL 3",True,(WHITE))
    screen.blit(LVL3,(232,530))
    
def Winning1():
    'what happens if you win the game'

    draw.rect(screen,(0,0,0),(200,175,400,350))
    
    UW = mainfont.render("CONGRATULATIONS",True,(WHITE))
    screen.blit(UW,(250,180))

    draw.rect(screen,(255,204,0),(WplayARect))
    PLAYA1 = instrfont.render("PLAY",True,(WHITE))
    screen.blit(PLAYA1,(337,235))
    PLAYA2 = instrfont.render("AGAIN",True,(WHITE))
    screen.blit(PLAYA2,(320,275))
    
    draw.rect(screen,(255,204,0),(WplayNRect))
    PLAYN1 = instrfont.render("NEXT",True,(WHITE))
    screen.blit(PLAYN1,(337,325))
    PLAYN2 = instrfont.render("LEVEL",True,(WHITE))
    screen.blit(PLAYN2,(320,365))
    
    draw.rect(screen,(255,204,0),(WmenuRect))
    MENU = instrfont.render("MENU",True,(WHITE))
    screen.blit(MENU,(335,435))


def Winning2():
    'what happens if you beat the final level'
    
    draw.rect(screen,(0,0,0),(200,175,400,350))
    UW = mainfont.render("CONGRATULATIONS",True,(WHITE))
    screen.blit(UW,(250,180))

    draw.rect(screen,(255,204,0),(LplayRect))
    PLAY = customfont.render("PLAY",True,(WHITE))
    screen.blit(PLAY,(300,240))
    AGAIN = customfont.render("AGAIN",True,(WHITE))
    screen.blit(AGAIN,(280,290))

    draw.rect(screen,(255,204,0),(LmenuRect))
    MENU = customfont.render("MENU",True,(WHITE))
    screen.blit(MENU,(303,405))
    
def Losing():
    'what happens if you lose all three lives'
    
    draw.rect(screen,(0,0,0),(200,175,400,350))
    UL = mainfont.render("YOU LOSE",True,(WHITE))
    screen.blit(UL,(320,180))

    draw.rect(screen,(255,204,0),(LplayRect))
    PLAY = customfont.render("PLAY",True,(WHITE))
    screen.blit(PLAY,(300,240))
    AGAIN = customfont.render("AGAIN",True,(WHITE))
    screen.blit(AGAIN,(280,290))

    draw.rect(screen,(255,204,0),(LmenuRect))
    MENU = customfont.render("MENU",True,(WHITE))
    screen.blit(MENU,(303,405))
    
def mazePicload (mazepic,mazewidth,mazeheight):
    'blitts maze'                                 

    screen.blit(transform.scale(mazepic,(mazewidth,mazeheight)),(mazedistx,mazedisty))
def grid (squareX,squareY):
    'draws grid'

    for x in range (19):
        draw.line(screen,GREY,(squareX,squareY),(squareX,squareY+mazeheight),1)
        squareX += squarewidth
    squareX -= (squarewidth*18)          #resetting x value
    for y in range (21):
        draw.line(screen,GREY, (squareX-squarewidth,squareY), (squareX+mazewidth-squarewidth,squareY),1)
        squareY += squarewidth
def drawLives (pacman):
    "Displays the amount of lives that pacman has"
    x,y = 650,570
    for i in range (pacman[LIVES]):
        screen.blit(transform.scale(livespic,(50,50)),(x,y))
        x += 55
def drawCoins (coinList):
    'draws coins from list'

    for i in range (len(coinList)):
        for j in range (len(coinList[i])):
            if coinList[i][j] == 1:
                draw.circle(screen,GOLD,(j*squarewidth+80,i*squarewidth+50),3)

def drawPacman(pacman,pacmanframes):
    'drawsPacman blitting frames to the location'

    move = pacman[MOVE]
    frame = int(pacman[FRAME])
    pic = pacmanframes[move][frame]
    screen.blit(transform.scale(pic,(26,26)),(pacman[X]+1,pacman[Y]+1))

def drawGhosts(ghosts,ghostframes):
    'draws ghosts'
    for i in range (len(ghosts)):
        move = ghosts[i][MOVE]
        pic = ghostframes[i][move]        
        screen.blit(transform.scale(pic,(26,26)),(ghosts[i][X]-15,ghosts[i][Y]-15))

def drawScene(mazepic,mazepicW,mazepicH, ghosts):
    'draws everything'
    screen.fill(0)
    mazePicload(maze,mazewidth,mazeheight)
    drawCoins(coinList)
    drawLives(pacman)
    #grid (mazedistx,mazedisty)    
    drawPacman(pacman,pacmanframes)
    drawGhosts(ghosts,ghostframes)
def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1): 
            move.append(image.load("%s/%s%03d.png" % (name,name,i)))
    return move        

    

#variables

#time
myClock = time.Clock()  
#screen
WIDTH,HEIGHT = 810,700
screen = display.set_mode((WIDTH,HEIGHT)) #setting displays
#preset colors
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (107,107,107)
YELLOW = (255,255,0)
GOLD = (212,175,55)
PURPLE = (204,65,239)
WHITE = (255,255,255)
WALL = (237,28,36)
Screen = "Loading"
select = "play"
statusR = 0
statusL = 0
MouseC = 0
Music = "OFF"
MAZE = "Blue"
#Rectangles                                                          The rectangles that are used throughout the game 
playRect = Rect(200,75,400,150)
levelsRect = Rect(200,275,400,150)
customRect = Rect(200,475,400,150)
settingsRect = Rect(740,10,50,50)
instructionRect = Rect(740,70,50,50)
blueRect = Rect(75,250,75,75)
purpleRect = Rect(175,250,75,75)
orangeRect = Rect(275,250,75,75)
turquioseRect = Rect(375,250,75,75)
greenRect = Rect(475,250,75,75)
saadRect = Rect(575,250,75,75)
mixRect = Rect(675,250,75,75)                                  
ypacRect = Rect(75,400,75,75)
bpacRect = Rect(175,400,75,75)
ppacRect = Rect(275,400,75,75)
gpacRect = Rect(375,400,75,75)
mpacRect = Rect(475,400,75,75)
wpacRect = Rect(575,400,75,75)
homeRect = Rect(10,10,50,50)
LplayRect = Rect(275,230,250,120)
LmenuRect = Rect(275,370,250,120)
WplayARect = Rect(275,230,250,80)
WplayNRect = Rect(275,320,250,80)
WmenuRect = Rect(275,410,250,80)
#Loading pictures that are used multiple times
homePic = "home.png"
home = image.load(homePic)
design1Pic = "design1.png"
design1 = image.load(design1Pic)
design2Pic = "design2.png"
design2 = image.load(design2Pic)
#music

OnRect = Rect(455,100,145,75)
OffRect = Rect(605,100,145,75)


#maze
maze = image.load('maze2.png')
mazemask = image.load('pacmanmask.png')
ghostmask = image.load('ghostmask.png')
mazewidth,mazeheight = 570,630 #dimesnsions maze is blitted
#grid
squarewidth = 30
#mazedistfromtopleft
mazedistx,mazedisty = 65,35
mazeList =[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],     #2d list representation of maze
                     [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],     #used to check if player is in contact with wall
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],     #if 1 its a wall and you can't go there
                     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],      #middle
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                     [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
                     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],     #0 is open spot
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
                     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                     [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                     [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] 
                                                    #m                  
                                                    #i
                                                    #d
                                                    #d
                                                    #l
                                                    #e 
#pacman location
#movement
playerspeed = 3

#dimensions
pacrad = 15 #gets middlepoint of pacman

#sprites
SPRITES = "pacmancharacter"
pacmanframes = []
pacmanframes.append(makeMove(SPRITES,1,5))     #right
pacmanframes.append(makeMove(SPRITES,6,10))   #down
pacmanframes.append(makeMove(SPRITES,11,15)) #left
pacmanframes.append(makeMove(SPRITES,16,20)) #up
pprint(pacmanframes)

#moves indices for pacman list
right = 0
down = 1
left = 2
up = 3

#pacMan spot
X = 0#indices for pacman list
Y = 1
MOVE = 2
FRAME = 3
NXTMOVE = 4
LIVES = 5
pacman = [335,605, 2, 0, 0, 3]
livespic = image.load('pacmanpic.png')
#ghost columns
ghostframes = []                                #appending 2dlist of frames
ghostframes.append(makeMove('bluedude',1,4))    #blue
ghostframes.append(makeMove('orangeguy',1,4))   #orange
ghostframes.append(makeMove('pinky',1,4))       #pink 
ghostframes.append(makeMove('redguy',1,4))      #red
print(ghostframes)
X = 0
Y = 1
MOVE = 2
COLOR = 3
ghosts = [[350,320,3],                #blue
          [350,320,3],                #orange
          [350,320,3],                #pink
          [350,320,3]]                #red
ghostspeed = 2
startX,startY = 350,320
ox,oy = 350,320
#coins
CoinCounter = 0
HOMP=transform.scale(home,(50,50))
#font
font.init()
mainfont = font.Font("mainfont.TTF",20)
playfont = font.Font("mainfont.TTF",75)
instrfont = font.Font("mainfont.TTF",34)
customfont = font.Font("mainfont.TTF",50)
#coins
coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
coinList2 = [[0]*19 for i in range(21)]
for i in range (len(coinList)):
    for j in range(len(coinList[i])):
        coinList2[i][j] = listConvert(j,i)

        
while running():


    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()
    keys=key.get_pressed()
    
    if mb[0] == 1:
        MouseC = 1
    if keys[K_RIGHT]:
        statusR = 1
        
    if keys[K_LEFT]:
        statusL = 1



    if (keys[K_LSHIFT] or keys[K_RSHIFT]) and (keys[K_h] or keys[K_m]):
        Screen = "menu"
    
    if Screen == 'Loading':
        loadScreen()
    if keys[K_SPACE] and Screen == "Loading":
        Screen = "menu"


    if Screen == "menu":
        menu()

 
            
        if select == "play":
            draw.rect(screen,WHITE,(playRect),5)
            if (keys[K_RIGHT] == False ) and statusR == 1:
                statusR = 0
                select = "levels"
            if (keys[K_LEFT] ==  False ) and statusL == 1:
                statusL = 0
                select = "settings"
                
                
        elif select == "levels":
            draw.rect(screen,WHITE,(levelsRect),5)
            if (keys[K_RIGHT]==False) and statusR == 1:
                statusR = 0
                select = "custom"
            if (keys[K_LEFT] == False) and statusL == 1:
                statusL = 0
                select = "play"

        elif select == "custom":
            draw.rect(screen,WHITE,(customRect),5)
            if (keys[K_RIGHT] == False) and statusR == 1:
                statusR = 0
                select = "settings"
            if (keys[K_LEFT] == False) and statusL == 1:
                statusL = 0
                select = "levels"
 

        elif select == "settings":
            draw.rect(screen,WHITE,(settingsRect),5)
            if (keys[K_RIGHT] == False) and statusR == 1:
                statusR = 0
                select = "instruction"
            if (keys[K_LEFT] == False) and statusL == 1:
                statusL = 0
                select = "custom"

        elif select == "instruction":
            draw.rect(screen,WHITE,(instructionRect),5)
            if (keys[K_RIGHT] == False) and statusR == 1:
                statusR = 0
                select = "play"
            if (keys[K_LEFT] == False) and statusL == 1:
                statusL = 0
                select = "settings"
                           
        if mb[0] == 1 and playRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "play"
        if mb[0] == False and levelsRect.collidepoint(mx,my) and MouseC == 1:
            MouseC = 0
            Screen = "levels"
        if mb[0] == 1 and settingsRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "settings"
        if mb[0] == 1 and customRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "custom"
        if mb[0] == 1 and instructionRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "instruction"

        if select == "play" and keys[K_RETURN]:
            Screen = "play"
        if select == "levels" and keys[K_RETURN]:
            Screen = "levels"
        if select == "custom" and keys[K_RETURN]:
            Screen = "custom"
        if select == "settings" and keys[K_RETURN]:
            Screen = "settings"
        if select == "instructions" and keys[K_RETURN]:
            Screen = "instructions"
            
    elif Screen == "play":            
        movePick(pacman,playerspeed)
        movePacman(pacman,playerspeed)
        nxtMove(pacman)
        moveGhost(ghosts, ghostspeed)
        checkCoinhits(pacman,coinList,coinList2)
        if ghosthit(ghosts,pacman):
            pacman[LIVES] -= 1
            pacman[X],pacman[Y] = 335,605 
            for g in range (len(ghosts)):
                ghosts[g][X],ghosts[g][Y] = ox,oy
              
        drawScene(maze,mazewidth,mazeheight, ghosts)
        COINCOUNTER = str(CoinCounter)
        COINS = mainfont.render(COINCOUNTER,True,(GOLD))
        screen.blit(COINS,(640,500))
        draw.rect(screen,WHITE,(homeRect))
        screen.blit(HOMP,(10,10))
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"

        if empty(coinList) == True:
            Screen = "Winning1"
            pacman[LIVES] = 3
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        if pacman[LIVES] == 0:
            Screen = "Losing"
            pacman[LIVES] = 3
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    elif Screen == "level2":
        pacman[LIVES] = 2
        movePick(pacman,playerspeed)
        movePacman(pacman,playerspeed)
        nxtMove(pacman)
        moveGhost(ghosts, ghostspeed)
        checkCoinhits(pacman,coinList,coinList2)
        if ghosthit(ghosts,pacman):
            pacman[LIVES] -= 1
            pacman[X],pacman[Y] = 335,605 
            for g in range (len(ghosts)):
                ghosts[g][X],ghosts[g][Y] = ox,oy
              
        drawScene(maze,mazewidth,mazeheight, ghosts)
        COINCOUNTER = str(CoinCounter)
        COINS = mainfont.render(COINCOUNTER,True,(GOLD))
        screen.blit(COINS,(640,500))
        draw.rect(screen,WHITE,(homeRect))
        screen.blit(HOMP,(10,10))
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"

        if empty(coinList) == True:
            Screen = "Winning2"
            pacman[LIVES] = 2
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        if pacman[LIVES] == 0:
            Screen = "Losing2"
            pacman[LIVES] = 2
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    elif Screen == "level3":
        pacman[LIVES] = 1
        movePick(pacman,playerspeed)
        movePacman(pacman,playerspeed)
        nxtMove(pacman)
        moveGhost(ghosts, ghostspeed)
        checkCoinhits(pacman,coinList,coinList2)
        if ghosthit(ghosts,pacman):
            pacman[LIVES] -= 1
            pacman[X],pacman[Y] = 335,605 
            for g in range (len(ghosts)):
                ghosts[g][X],ghosts[g][Y] = ox,oy
              
        drawScene(maze,mazewidth,mazeheight, ghosts)
        COINCOUNTER = str(CoinCounter)
        COINS = mainfont.render(COINCOUNTER,True,(GOLD))
        screen.blit(COINS,(640,500))
        draw.rect(screen,WHITE,(homeRect))
        screen.blit(HOMP,(10,10))
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"
        if empty(coinList) == True:
            Screen = "Winning2"
            pacman[LIVES] = 1
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        if pacman[LIVES] == 0:
            Screen = "Losing2"
            pacman[LIVES] = 1
            coinList = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
             [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    
    elif Screen == "instruction":
        instruction()
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"
        
    elif Screen == "settings":
        settings()
        if mb[0] == 1 and OnRect.collidepoint(mx,my):
            Music = "ON"
        if mb[0] == 1 and OffRect.collidepoint(mx,my):
            Music = "OFF"
        
        if Music == "ON":
            init()
            intromusic = mixer.music.load('intromusic.mp3')
            mixer.music.play()
            draw.rect(screen,WHITE,(OnRect),5)
        elif Music == "OFF":
            draw.rect(screen,WHITE,(OffRect),5)
            
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"
    elif Screen == "custom":
        custom()
        
        if mb[0] == 1 and blueRect.collidepoint(mx,my):
            MAZE = "Blue"
        if mb[0] == 1 and purpleRect.collidepoint(mx,my):
            MAZE = "Purple"
        if mb[0] == 1 and orangeRect.collidepoint(mx,my):
            MAZE = "Orange"
        if mb[0] == 1 and turquioseRect.collidepoint(mx,my):
            MAZE = "Turquiose"
        if mb[0] == 1 and greenRect.collidepoint(mx,my):
            MAZE = "Green"
        if mb[0] == 1 and saadRect.collidepoint(mx,my):
            MAZE = "Saad"
        if mb[0] == 1 and mixRect.collidepoint(mx,my):
            MAZE = "Mix"

        if MAZE == "Blue":
            maze = image.load('maze2.png')
            draw.rect(screen,WHITE,(blueRect),3)                                 #Drawing a rect around the maze which is selected is just to make the game more user friendly
        elif MAZE == "Purple":
            maze = image.load("mazepurple.png")
            draw.rect(screen,WHITE,(purpleRect),3)
        elif MAZE == "Orange":
            maze = image.load("mazeorange.png")
            draw.rect(screen,WHITE,(orangeRect),3)
        elif MAZE == "Turquiose":
            maze = image.load("mazeturqoise.png")
            draw.rect(screen,WHITE,(turquioseRect),3)
        elif MAZE == "Green":
            maze = image.load("mazegreen.png")
            draw.rect(screen,WHITE,(greenRect),3) 
        elif MAZE == "Saad":
            maze = image.load("mazesaad.png")
            draw.rect(screen,WHITE,(saadRect),3)
        elif MAZE == "Mix":
            maze = image.load("mazemix.png")
            draw.rect(screen,WHITE,(mixRect),3)

        if mb[0] == 1 and ypacRect.collidepoint(mx,my):
            SPRITES = "pacmancharacter"

        if mb[0] == 1 and bpacRect.collidepoint(mx,my):
            SPRITES = "bpacman"

        if mb[0] == 1 and ppacRect.collidepoint(mx,my):
            SPRITES = "ppacman"

        if mb[0] == 1 and gpacRect.collidepoint(mx,my):
            SPRITES = "gpacman"
            
        if mb[0] == 1 and mpacRect.collidepoint(mx,my):
            SPRITES = "mpacman"

        if mb[0] == 1 and wpacRect.collidepoint(mx,my):
            SPRITES = "wpacman"
            
        if SPRITES == "pacmancharacter":
            draw.rect(screen,GOLD,(ypacRect),3)

        elif SPRITES == "bpacman":
            draw.rect(screen,GOLD,(bpacRect),3)

        elif SPRITES == "ppacman":
            draw.rect(screen,GOLD,(ppacRect),3)

        elif SPRITES == "gpacman":
            draw.rect(screen,GOLD,(gpacRect),3)

        elif SPRITES == "mpacman":
            draw.rect(screen,GOLD,(mpacRect),3)

        elif SPRITES == "wpacman":
            draw.rect(screen,GOLD,(wpacRect),3)
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"


        pacmanframes = []
        pacmanframes.append(makeMove(SPRITES,1,5))     #right
        pacmanframes.append(makeMove(SPRITES,6,10))   #down
        pacmanframes.append(makeMove(SPRITES,11,15)) #left
        pacmanframes.append(makeMove(SPRITES,16,20)) #up

    elif Screen == "levels":
        levels()
        if mb[0] == 1 and homeRect.collidepoint(mx,my):
            Screen = "menu"
        
        if mb[0] == 1 and playRect.collidepoint(mx,my):
            Screen = "play"
        if mb[0] == 1 and levelsRect.collidepoint(mx,my):
            Screen = "level2"
        if mb[0] == 1 and customRect.collidepoint(mx,my):
            Screen = "level3"

    elif Screen == "Losing":
        Losing()
        if mb[0] == 1 and LplayRect.collidepoint(mx,my):
            Screen = "play"
        if mb[0] == 1 and LmenuRect.collidepoint(mx,my):
            Screen = "menu"

    elif Screen == "Winning1":
        Winning1()
        if mb[0] == 1 and WplayARect.collidepoint(mx,my):
            Screen = "play"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and WplayNRect.collidepoint(mx,my):
            Screen = "level2"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and WmenuRect.collidepoint(mx,my):
            Screen = "menu"

    elif Screen == "Losing2":
        Losing()
        if mb[0] == 1 and LplayRect.collidepoint(mx,my):
            Screen = "level2"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and LmenuRect.collidepoint(mx,my):
            Screen = "menu"

    elif Screen == "Winning2":
        Winning1()
        if mb[0] == 1 and WplayARect.collidepoint(mx,my):
            MouseC = 0
            Screen = "level2"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and WplayNRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "level3"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and WmenuRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "menu"

    elif Screen == "Winning3":
        Winning2()
        if mb[0] == 1 and LplayRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "level3"
        if mb[0] == 1 and LmenuRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "menu"

    elif Screen == "Losing3":
        Losing()
        if mb[0] == 1 and LplayRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "level3"
            pacman[0] = 335
            pacman[1] = 605
        if mb[0] == 1 and LmenuRect.collidepoint(mx,my):
            MouseC = 0
            Screen = "menu"


    display.flip()
quit()



'''''''''''''''''''''''''''''''''''''''
            import modules
'''''''''''''''''''''''''''''''''''''''

import numpy as np
import pygame
import sys
import math
import tkinter as tk
import json
import os

pygame.init()
pygame.display.set_caption('Connect Four - Global Offensive')

'''''''''''''''''''''''''''''''''''''''
         define global variables
'''''''''''''''''''''''''''''''''''''''

#Casual Leaderboards
if not os.path.isfile('nleader.txt'):
    nleaderboard = {'1':'', '2':'', '3':'', '4':'','5':'','6':'','7':''}

    nleaderboard['1'] = '_____________'
    nleaderboard['2'] = '_____________'
    nleaderboard['3'] = '_____________'
    nleaderboard['4'] = '_____________'
    nleaderboard['5'] = '_____________'
    nleaderboard['6'] = '_____________'
    nleaderboard['7'] = '_____________'

    with open('nleader.txt','w') as fp:
        json.dump(nleaderboard, fp)          
else:
    with open('nleader.txt', 'r') as fp:
        nleaderboard = json.load(fp)

if not os.path.isfile('sleader.txt'):
    sleaderboard = {'1':'', '2':'', '3':'', '4':'','5':'','6':'','7':''}

    sleaderboard['1'] = '__'
    sleaderboard['2'] = '__'
    sleaderboard['3'] = '__'
    sleaderboard['4'] = '__'
    sleaderboard['5'] = '__'
    sleaderboard['6'] = '__'
    sleaderboard['7'] = '__'

    with open('sleader.txt','w') as fp:
        json.dump(sleaderboard, fp)
else:
    with open('sleader.txt', 'r') as fp:
        sleaderboard = json.load(fp)

#Competitive Leaderboards
if not os.path.isfile('cnleader.txt'):
    cnleaderboard = {'1':'', '2':'', '3':'', '4':'','5':'','6':'','7':''}

    cnleaderboard['1'] = '             '
    cnleaderboard['2'] = '             '
    cnleaderboard['3'] = '    !Under!  '
    cnleaderboard['4'] = '             '
    cnleaderboard['5'] = ' !Construction!'
    cnleaderboard['6'] = '             '
    cnleaderboard['7'] = '             '

    with open('cnleader.txt','w') as fp:
        json.dump(cnleaderboard, fp)   
else:
    with open('cnleader.txt', 'r') as fp:
        cnleaderboard = json.load(fp)

if not os.path.isfile('csleader.txt'):
    csleaderboard = {'1':'', '2':'', '3':'', '4':'','5':'','6':'','7':''}

    csleaderboard['1'] = '  '
    csleaderboard['2'] = '  '
    csleaderboard['3'] = '  '
    csleaderboard['4'] = '  '
    csleaderboard['5'] = '  '
    csleaderboard['6'] = '  '
    csleaderboard['7'] = '  '

    with open('csleader.txt','w') as fp:
        json.dump(csleaderboard, fp)   
else:
    with open('csleader.txt', 'r') as fp:
        csleaderboard = json.load(fp)


#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)
BEIGE = (204, 201, 192)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (200,0,200)
CYAN = (0,255,255)
DRED = (94,25,20)

colorIn = {
    "Red" : RED,
    "Green" : GREEN,
    "Blue" : BLUE,
    "Yellow" : YELLOW,
    "Purple" : PURPLE,
    "Cyan" : CYAN
}

winfont = pygame.font.SysFont("monospace", 75)
leadfont = pygame.font.SysFont('monospace', 50)
C4font = pygame.font.SysFont("Comicsans", 100)
GEfont = pygame.font.SysFont("Comicsans", 60)

exit_game = False

WIN_REQ = 4
ROW_COUNT = 6
COLUMN_COUNT = 7

P1col = ""
P2col = ""

nav = "home"
lnav = 'casual'
winner = 0
score = 0
winnername = ''
p1p2entcol = False
p1entcol = False
p2entcol = False
p1p2entsamecol = False
nmm = False

if P1col in colorIn:
    P1col = colorIn[P1col]

if P2col in colorIn:
    P2col = colorIn[P2col]

SQUARESIZE = 100
boardWidth = COLUMN_COUNT * SQUARESIZE
boardHeight = (ROW_COUNT + 1) * SQUARESIZE
screenWidth = boardWidth
screenHeight = boardHeight
size = (screenWidth,screenHeight)
screenCenterH = screenWidth/2
screenCenterV = screenHeight/2
radius = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

'''''''''''''''''''''''''''''''''''''''
       define button properties  
'''''''''''''''''''''''''''''''''''''''

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline):
        #Call this method to draw the button on the screen

        pygame.draw.rect(win, outline, (self.x-3,self.y-3,self.width+6,self.height+6),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

buttonW = 250
buttonH = 100
buttonVcenter = screenCenterV - buttonH/2
buttonWcenter = screenCenterH - buttonW/2
playbutton = button(WHITE, buttonWcenter,(buttonVcenter-30),buttonW,buttonH,"Play")
leaderboardbutton = button(WHITE, (buttonWcenter-25), (buttonVcenter+100), (buttonW + 50), buttonH, "Leaderboard")
backbutton = button(WHITE, 20, (screenHeight-120), 150, 100, "Back")
quitGamebutton = button(WHITE, (screenWidth - buttonW - 20), (screenHeight-120), buttonW, 100, "Quit Game")
clearBoardbutton = button(WHITE, (screenWidth - buttonW - 20 - 20), (screenHeight-120), (buttonW+20), 100, "Clear Board")
StartGamebutton = button(WHITE, (buttonWcenter-25), (buttonVcenter+280), (buttonW + 50), buttonH, "Start Game")
rarrowbutton = button(WHITE, (screenWidth - 100), 25, 70, 70, ">")
larrowbutton = button(WHITE, 30, 25, 70, 70, "<")
continuebutton = button(WHITE, screenCenterH - 200/2, screenCenterV + 23, 200, 75, 'Continue')

colbuttonW = 90
colbuttonH = 60

redp1 = button(RED, (screenCenterH/4 - colbuttonW/2 - 20), 360, colbuttonW, colbuttonH, "")
greenp1 = button(GREEN, (screenCenterH/2 - colbuttonW/2), 360, colbuttonW, colbuttonH, "")
bluep1 = button(BLUE, ((3*screenCenterH)/4 - colbuttonW/2 + 20), 360, colbuttonW, colbuttonH, "")
blackp1 = button(BLACK, (screenCenterH/4 - colbuttonW/2 - 20), 450, colbuttonW, colbuttonH, "")
purplep1 = button(PURPLE, (screenCenterH/2 - colbuttonW/2), 450, colbuttonW, colbuttonH, "")
whitep1 = button(WHITE, ((3*screenCenterH)/4 - colbuttonW/2 + 20), 450, colbuttonW, colbuttonH, "")

redp2 = button(RED, ((5*screenCenterH)/4 - colbuttonW/2 - 20), 360, colbuttonW, colbuttonH, "")
greenp2 = button(GREEN, ((3*screenCenterH)/2 - colbuttonW/2), 360, colbuttonW, colbuttonH, "")
bluep2 = button(BLUE, ((7*screenCenterH)/4 - colbuttonW/2 + 20), 360, colbuttonW, colbuttonH, "")
blackp2 = button(BLACK, ((5*screenCenterH)/4 - colbuttonW/2 - 20), 450, colbuttonW, colbuttonH, "")
purplep2 = button(PURPLE, ((3*screenCenterH)/2 - colbuttonW/2), 450, colbuttonW, colbuttonH, "")
whitep2 = button(WHITE, ((7*screenCenterH)/4 - colbuttonW/2 + 20), 450, colbuttonW, colbuttonH, "")

'''''''''''''''''''''''''''''''''''''''
         define text input sequences  
'''''''''''''''''''''''''''''''''''''''
#must be less than 13 characters


'''''''''''''''''''''''''''''''''''''''
         define main sequences  
'''''''''''''''''''''''''''''''''''''''

def game_intro():
    screen.fill(BEIGE)
    pygame.draw.circle(screen, BLACK, (int(screenCenterH), int(screenCenterV)),300)
    pygame.draw.circle(screen, BEIGE, (int(screenCenterH), int(screenCenterV)),290)
    BarW = 540
    pygame.draw.rect(screen, BLACK, (int(screenCenterH - BarW/2), int(screenCenterH - 130), BarW,20))
    pygame.draw.rect(screen, BLACK, (int(screenCenterH - BarW/2), int(screenCenterH + 110), BarW,20))
    C4 = C4font.render("Connect Four", 1, BLACK)
    GE = GEfont.render("Global Offensive", 1, BLACK)
    c4W = C4.get_width()
    goW = GE.get_width()
    screen.blit(C4, (int(screenCenterH - c4W/2),290))
    screen.blit(GE, (int(screenCenterH -goW/2),380))
    pygame.display.update()
    pygame.time.wait(3000)

def home_page():
    global nav
    nav = "home"
    screen.fill(BEIGE)
    C4 = C4font.render("Connect Four", 1, BLACK)
    GE = GEfont.render("Global Offensive", 1, BLACK)
    c4W = C4.get_width()
    goW = GE.get_width()
    screen.blit(C4, (int(screenCenterH - c4W/2),40))
    screen.blit(GE, (int(screenCenterH -goW/2),120))
    playbutton.draw(screen,(0,0,0))
    leaderboardbutton.draw(screen, (0,0,0))
    quitGamebutton.draw(screen, BLACK)
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if playbutton.isOver(pos):
                nav = 'casual'
            if leaderboardbutton.isOver(pos):
                nav = 'leaderboard'
            if quitGamebutton.isOver(pos):
                nav = 'quit'
   
        if event.type == pygame.MOUSEMOTION:
            if playbutton.isOver(pos):
                playbutton.color = GREY
            elif leaderboardbutton.isOver(pos):
                leaderboardbutton.color = GREY
            elif quitGamebutton.isOver(pos):
                quitGamebutton.color = GREY
            else:
                playbutton.color = WHITE
                leaderboardbutton.color = WHITE
                quitGamebutton.color = WHITE

def leaderboard_screen():
    global nav
    global lnav
    lnav = 'casual'
    while lnav == 'casual':
        casual_leaderboard_screen()
    while lnav == 'competitive':
        competitive_leaderboard_screen()


def casual_leaderboard_screen():
    global nav
    global lnav
    screen.fill(BEIGE)
    Leaderboard = GEfont.render("Casual Leaderboard", 1 , BLACK)
    lW = Leaderboard.get_width()
    screen.blit(Leaderboard, ((screenCenterH - lW/2),40))

    #Numbers

    One = leadfont.render('1', 1, BLACK)
    Two = leadfont.render('2', 1, BLACK)
    Three = leadfont.render('3', 1, BLACK)
    Four = leadfont.render('4', 1, BLACK)
    Five = leadfont.render('5', 1, BLACK)
    Six = leadfont.render('6', 1, BLACK)
    Seven = leadfont.render('7', 1, BLACK)
    screen.blit(One, (40,120))
    screen.blit(Two, (40,180))
    screen.blit(Three, (40,240))
    screen.blit(Four, (40,300))
    screen.blit(Five, (40,360))
    screen.blit(Six, (40,420))
    screen.blit(Seven, (40,480))

    #Names

    nOne = leadfont.render(nleaderboard['1'], 1, BLACK)
    nTwo = leadfont.render(nleaderboard['2'], 1, BLACK)
    nThree = leadfont.render(nleaderboard['3'], 1, BLACK)
    nFour = leadfont.render(nleaderboard['4'], 1, BLACK)
    nFive = leadfont.render(nleaderboard['5'], 1, BLACK)
    nSix = leadfont.render(nleaderboard['6'], 1, BLACK)
    nSeven = leadfont.render(nleaderboard['7'], 1, BLACK)
    screen.blit(nOne, (140,120))
    screen.blit(nTwo, (140,180))
    screen.blit(nThree, (140,240))
    screen.blit(nFour, (140,300))
    screen.blit(nFive, (140,360))
    screen.blit(nSix, (140,420))
    screen.blit(nSeven, (140,480))

    #Scores

    sOne = leadfont.render(sleaderboard['1'], 1, BLACK)
    sTwo = leadfont.render(sleaderboard['2'], 1, BLACK)
    sThree = leadfont.render(sleaderboard['3'], 1, BLACK)
    sFour = leadfont.render(sleaderboard['4'], 1, BLACK)
    sFive = leadfont.render(sleaderboard['5'], 1, BLACK)
    sSix = leadfont.render(sleaderboard['6'], 1, BLACK)
    sSeven = leadfont.render(sleaderboard['7'], 1, BLACK)
    screen.blit(sOne, ((screenWidth - 100),120))
    screen.blit(sTwo, ((screenWidth - 100),180))
    screen.blit(sThree, ((screenWidth - 100),240))
    screen.blit(sFour, ((screenWidth - 100),300))
    screen.blit(sFive, ((screenWidth - 100),360))
    screen.blit(sSix, ((screenWidth - 100),420))
    screen.blit(sSeven, ((screenWidth - 100),480))
    
    
    backbutton.draw(screen, BLACK)
    rarrowbutton.draw(screen, BLACK)
    clearBoardbutton.draw(screen, BLACK)
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if backbutton.isOver(pos):
                nav  = 'home'
                lnav = 'out'
            if rarrowbutton.isOver(pos):
                lnav = 'competitive'
            if clearBoardbutton.isOver(pos):
                nleaderboard['1'] = '_____________'
                nleaderboard['2'] = '_____________'
                nleaderboard['3'] = '_____________'
                nleaderboard['4'] = '_____________'
                nleaderboard['5'] = '_____________'
                nleaderboard['6'] = '_____________'
                nleaderboard['7'] = '_____________'
                
                sleaderboard['1'] = '__'
                sleaderboard['2'] = '__'
                sleaderboard['3'] = '__'
                sleaderboard['4'] = '__'
                sleaderboard['5'] = '__'
                sleaderboard['6'] = '__'
                sleaderboard['7'] = '__'

                with open('nleader.txt','w') as fp:
                    json.dump(nleaderboard, fp)
                with open('sleader.txt','w') as fp:
                    json.dump(sleaderboard, fp)
                casual_leaderboard_screen()

            
        if event.type == pygame.MOUSEMOTION:
            if backbutton.isOver(pos):
                backbutton.color = GREY
            else:
                backbutton.color = WHITE
            if clearBoardbutton.isOver(pos):
                clearBoardbutton.color = GREY
            else:
                clearBoardbutton.color = WHITE
            if rarrowbutton.isOver(pos):
                rarrowbutton.color = GREY
            else:
                rarrowbutton.color = WHITE
            
def competitive_leaderboard_screen():
    global nav
    global lnav
    screen.fill(BEIGE)
    Leaderboard = GEfont.render("Comp Leaderboard", 1 , BLACK)
    lW = Leaderboard.get_width()
    screen.blit(Leaderboard, ((screenCenterH - lW/2),40))

    #Numbers

    One = leadfont.render('1', 1, BLACK)
    Two = leadfont.render('2', 1, BLACK)
    Three = leadfont.render('3', 1, BLACK)
    Four = leadfont.render('4', 1, BLACK)
    Five = leadfont.render('5', 1, BLACK)
    Six = leadfont.render('6', 1, BLACK)
    Seven = leadfont.render('7', 1, BLACK)
    screen.blit(One, (40,120))
    screen.blit(Two, (40,180))
    screen.blit(Three, (40,240))
    screen.blit(Four, (40,300))
    screen.blit(Five, (40,360))
    screen.blit(Six, (40,420))
    screen.blit(Seven, (40,480))

    #Names

    nOne = leadfont.render(cnleaderboard['1'], 1, BLACK)
    nTwo = leadfont.render(cnleaderboard['2'], 1, BLACK)
    nThree = leadfont.render(cnleaderboard['3'], 1, BLACK)
    nFour = leadfont.render(cnleaderboard['4'], 1, BLACK)
    nFive = leadfont.render(cnleaderboard['5'], 1, BLACK)
    nSix = leadfont.render(cnleaderboard['6'], 1, BLACK)
    nSeven = leadfont.render(cnleaderboard['7'], 1, BLACK)
    screen.blit(nOne, (140,120))
    screen.blit(nTwo, (140,180))
    screen.blit(nThree, (140,240))
    screen.blit(nFour, (140,300))
    screen.blit(nFive, (140,360))
    screen.blit(nSix, (140,420))
    screen.blit(nSeven, (140,480))

    #Scores

    sOne = leadfont.render(csleaderboard['1'], 1, BLACK)
    sTwo = leadfont.render(csleaderboard['2'], 1, BLACK)
    sThree = leadfont.render(csleaderboard['3'], 1, BLACK)
    sFour = leadfont.render(csleaderboard['4'], 1, BLACK)
    sFive = leadfont.render(csleaderboard['5'], 1, BLACK)
    sSix = leadfont.render(csleaderboard['6'], 1, BLACK)
    sSeven = leadfont.render(csleaderboard['7'], 1, BLACK)
    screen.blit(sOne, ((screenWidth - 100),120))
    screen.blit(sTwo, ((screenWidth - 100),180))
    screen.blit(sThree, ((screenWidth - 100),240))
    screen.blit(sFour, ((screenWidth - 100),300))
    screen.blit(sFive, ((screenWidth - 100),360))
    screen.blit(sSix, ((screenWidth - 100),420))
    screen.blit(sSeven, ((screenWidth - 100),480))
    
    
    backbutton.draw(screen, BLACK)
    larrowbutton.draw(screen, BLACK)
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if backbutton.isOver(pos):
                nav  = 'home'
                lnav = 'out'
            if larrowbutton.isOver(pos):
                lnav = 'casual'
            
        if event.type == pygame.MOUSEMOTION:
            if backbutton.isOver(pos):
                backbutton.color = GREY
            else:
                backbutton.color = WHITE
            if larrowbutton.isOver(pos):
                larrowbutton.color = GREY
            else:
                larrowbutton.color = WHITE

def casual_game():
    global nav
    global P1col
    global P2col
    global p1p2entcol
    global p1entcol
    global p2entcol
    global p1p2entsamecol
    casnav = "home"
    if casnav == "home":
        screen.fill(BEIGE)

        cashead = GEfont.render("Casual Game", 1 , BLACK)
        cW = cashead.get_width()
        screen.blit(cashead, ((screenCenterH - cW/2),40))

        play1 = GEfont.render("Player 1", 1 , BLACK)
        p1W = play1.get_width()
        screen.blit(play1, ((screenCenterH/2 - p1W/2)-5,170))

        col1 = GEfont.render("Colour", 1 , BLACK)
        c1W = col1.get_width()
        screen.blit(col1, ((screenCenterH/2 - c1W/2)-6,230))

        play2 = GEfont.render("Player 2", 1 , BLACK)
        p2W = play1.get_width()
        screen.blit(play2, ((3*screenCenterH/2 - p2W/2)+5,170))

        col2 = GEfont.render("Colour", 1 , BLACK)
        c2W = col2.get_width()
        screen.blit(col2, ((3*screenCenterH/2 - c2W/2)+5,230))



        dividerh = 420
        pygame.draw.rect(screen, BLACK, (int(screenCenterH - 8), int(screenCenterH - dividerh/2 - 20), 8,dividerh))

        StartGamebutton.draw(screen, (0,0,0))
        backbutton.draw(screen, BLACK)
        redp1.draw(screen, GREY)
        greenp1.draw(screen, GREY)
        bluep1.draw(screen, GREY)
        blackp1.draw(screen, GREY)
        purplep1.draw(screen, GREY)
        whitep1.draw(screen, GREY)
        redp2.draw(screen, GREY)
        greenp2.draw(screen, GREY)
        bluep2.draw(screen, GREY)
        blackp2.draw(screen, GREY)
        purplep2.draw(screen, GREY)
        whitep2.draw(screen, GREY)

        

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                exit() 
            
            while p1p2entcol == True:
                p1p2entercol()
            while p1entcol == True:
                p1entercol()
            while p2entcol == True:
                p2entercol()
            while p1p2entsamecol == True:
                p1p2entersamecol()

            if P1col == RED:
                redp1.draw(screen,DRED)
            elif P1col == GREEN:
                greenp1.draw(screen,DRED)
            elif P1col == BLUE:
                bluep1.draw(screen,DRED)
            elif P1col == BLACK:
                blackp1.draw(screen,DRED)
            elif P1col == PURPLE:
                purplep1.draw(screen,DRED)
            elif P1col == WHITE:
                whitep1.draw(screen,DRED)
            
            if P2col == RED:
                redp2.draw(screen,DRED)
            elif P2col == GREEN:
                greenp2.draw(screen,DRED)
            elif P2col == BLUE:
                bluep2.draw(screen,DRED)
            elif P2col == BLACK:
                blackp2.draw(screen,DRED)
            elif P2col == PURPLE:
                purplep2.draw(screen,DRED)
            elif P2col == WHITE:
                whitep2.draw(screen,DRED)

            pygame.display.update()
            pos = pygame.mouse.get_pos()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Player 1 color options
                if redp1.isOver(pos):
                    P1col = RED
                if greenp1.isOver(pos):
                    P1col = GREEN
                if bluep1.isOver(pos):
                    P1col = BLUE
                if blackp1.isOver(pos):                    
                    P1col = BLACK
                if purplep1.isOver(pos):                   
                    P1col = PURPLE
                if whitep1.isOver(pos):                    
                    P1col = WHITE
                
                #player 2 colour options
                if redp2.isOver(pos):                 
                    P2col = RED
                if greenp2.isOver(pos):                   
                    P2col = GREEN
                if bluep2.isOver(pos):                   
                    P2col = BLUE
                if blackp2.isOver(pos):                    
                    P2col = BLACK
                if purplep2.isOver(pos):                   
                    P2col = PURPLE
                if whitep2.isOver(pos):                   
                    P2col = WHITE

                #start the game once players have chosen colours
                if  StartGamebutton.isOver(pos):
                    if P1col == '' and P2col == '':
                        p1p2entcol = True                        
                    elif P1col == '' and P2col != '':
                        p1entcol = True
                    elif P1col != '' and P2col == '':
                        p2entcol = True
                    elif P1col == P2col:
                        p1p2entsamecol = True
                    else:
                        casnav = 'casgame'        
                if backbutton.isOver(pos):
                    nav = 'home'           
                
            if event.type == pygame.MOUSEMOTION:
                #Player 1 color options
                if redp1.isOver(pos):
                    redp1.draw(screen, DRED)
                    pygame.display.update()
                if greenp1.isOver(pos):
                    greenp1.draw(screen, DRED)   
                    pygame.display.update()                 
                if bluep1.isOver(pos):
                    bluep1.draw(screen, DRED)
                    pygame.display.update()
                if blackp1.isOver(pos):
                    blackp1.draw(screen, DRED) 
                    pygame.display.update()                   
                if purplep1.isOver(pos):
                    purplep1.draw(screen, DRED) 
                    pygame.display.update()                   
                if whitep1.isOver(pos):
                    whitep1.draw(screen, DRED)
                    pygame.display.update()
                                    
                #player 2 colour options
                if redp2.isOver(pos):
                    redp2.draw(screen, DRED) 
                    pygame.display.update()                   
                if greenp2.isOver(pos):
                    greenp2.draw(screen, DRED)
                    pygame.display.update()                    
                if bluep2.isOver(pos):
                    bluep2.draw(screen, DRED) 
                    pygame.display.update()                   
                if blackp2.isOver(pos):
                    blackp2.draw(screen, DRED) 
                    pygame.display.update()                 
                if purplep2.isOver(pos):
                    purplep2.draw(screen, DRED) 
                    pygame.display.update()                   
                if whitep2.isOver(pos):
                    whitep2.draw(screen, DRED)
                    pygame.display.update()
                    
                if  StartGamebutton.isOver(pos):
                    StartGamebutton.color = GREY
                else:
                    StartGamebutton.color = WHITE

                if  backbutton.isOver(pos):
                    backbutton.color = GREY
                else:
                    backbutton.color = WHITE
                
            
    if casnav == "casgame":
        game_seq()
        if not nmm:
            casual_win_screen()

        nav = "home"

def casual_win_screen():
    global winner
    global score
    global winnername
    screen.fill(BEIGE)

    playerpwin = GEfont.render("Player "+ str(winner)+ " Wins!", 1 , BLACK)
    pwW = playerpwin.get_width()
    screen.blit(playerpwin, ((screenCenterH - pwW/2),200))

    Score = GEfont.render("Score: "+str(score), 1 , BLACK)
    sW = Score.get_width()
    screen.blit(Score, ((screenCenterH - sW/2),260))

    enterName = GEfont.render("Please enter name to", 1 , BLACK)
    enW = enterName.get_width()
    screen.blit(enterName, ((screenCenterH - enW/2),340))

    addlead = GEfont.render("be added to the Leaderboard", 1 , BLACK)
    alW = addlead.get_width()
    screen.blit(addlead, ((screenCenterH - alW/2),400))

    pygame.display.update()

    alpha = tk.Tk()
    alpha.attributes("-topmost", True)
    tk.Label(alpha, text="Please enter your name here:").grid(row=1, column=1)
    tk.Label(alpha, text='          ').grid(row=0,column=0)
    tk.Label(alpha, text='          ').grid(row=0,column=1)
    tk.Label(alpha, text='          ').grid(row=0,column=2)
    tk.Label(alpha, text='          ').grid(row=1,column=0)
    tk.Label(alpha, text='          ').grid(row=1,column=2)
    tk.Label(alpha, text='          ').grid(row=2,column=0)
    tk.Label(alpha, text='          ').grid(row=2,column=2)
    tk.Label(alpha, text='          ').grid(row=3,column=0)
    tk.Label(alpha, text='          ').grid(row=3,column=1)
    tk.Label(alpha, text='          ').grid(row=3,column=2)
    tk.Label(alpha, text='          ').grid(row=4,column=0)
    tk.Label(alpha, text='          ').grid(row=4,column=1)
    tk.Label(alpha, text='Name must be no longer').grid(row=4,column=1)
    tk.Label(alpha, text='          ').grid(row=5,column=0)
    tk.Label(alpha, text='          ').grid(row=5,column=2)
    tk.Label(alpha, text='than 13 characters').grid(row=5,column=1)
    tk.Label(alpha, text='          ').grid(row=6,column=0)
    tk.Label(alpha, text='          ').grid(row=6,column=1)
    tk.Label(alpha, text='          ').grid(row=6,column=2)

    e1 = tk.Entry(alpha)

    e1.grid(row=2, column=1)

    def keypressed(event):
        global winnername
        if event.keysym == "Return":
            
            if len(e1.get()) > 13:
                alpha.mainloop()
        
            else:
                winnername = e1.get()
                alpha.destroy()

    alpha.bind("<Key>", keypressed)

    alpha.mainloop()


    update_cas_leaderboard()    


def comp_game():
    global nav

    pass

def quit_screen():
    screen.fill(BEIGE)
    ThanksFor = GEfont.render("Thanks For", 1 , BLACK)
    Playing = GEfont.render("Playing", 1 , BLACK)
    pygame.draw.circle(screen, BLACK, (int(screenCenterH), int(screenCenterV)),300)
    pygame.draw.circle(screen, BEIGE, (int(screenCenterH), int(screenCenterV)),290)
    BarW = 540
    pygame.draw.rect(screen, BLACK, (int(screenCenterH - BarW/2), int(screenCenterH - 130), BarW,20))
    pygame.draw.rect(screen, BLACK, (int(screenCenterH - BarW/2), int(screenCenterH + 110), BarW,20))
    tfW = ThanksFor.get_width()
    pW = Playing.get_width()
    screen.blit(ThanksFor, (int(screenCenterH - tfW/2),120))
    screen.blit(Playing, (int(screenCenterH - pW/2),160))
    C4 = C4font.render("Connect Four", 1, BLACK)
    GE = GEfont.render("Global Offensive", 1, BLACK)
    c4W = C4.get_width()
    goW = GE.get_width()
    screen.blit(C4, (int(screenCenterH - c4W/2),290))
    screen.blit(GE, (int(screenCenterH -goW/2),380))
    pygame.display.update()
    pygame.time.wait(3000)

'''''''''''''''''''''''''''''''''''''''
        define aux sequences  
'''''''''''''''''''''''''''''''''''''''

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    check = 0
    #check horizontal
    for c in range(COLUMN_COUNT-(WIN_REQ-1)):
        for r in range(ROW_COUNT):
            for w in range(WIN_REQ):
                if board[r][c+w] == piece:
                    check += 1
                else:
                    check = 0
                if check == WIN_REQ:
                    return True
                elif check == 0:
                    break

    #check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-(WIN_REQ - 1)):
            for w in range(WIN_REQ):
                if board[r+w][c] == piece:
                    check = check + 1
                else:
                    check = 0
                if check == WIN_REQ:
                    return True
                elif check == 0:
                    break
    
    #check positive diagonals
    for c in range(COLUMN_COUNT-(WIN_REQ -1)):
        for r in range(ROW_COUNT-(WIN_REQ -1)):
            for w in range(WIN_REQ):
                if board[r+w][c+w] == piece:
                    check = check + 1
                else:
                    check = 0
                if check == WIN_REQ:
                    return True
                elif check == 0:
                    break

    #check negative diagonals
    for c in range(COLUMN_COUNT-(WIN_REQ -1)):
        for r in range((WIN_REQ -1), ROW_COUNT):
            for w in range(WIN_REQ):
                if board[r-w][c+w] == piece:
                    check = check + 1
                else:
                    check = 0
                if check == WIN_REQ:
                    return True
                elif check == 0:
                    break

def draw_board(board):
    screen.fill(BEIGE)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            RECT = c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE,SQUARESIZE
            InRECT = (c*SQUARESIZE+2), (r*SQUARESIZE+SQUARESIZE+2), (SQUARESIZE-4),(SQUARESIZE-4)
            pygame.draw.rect(screen, GREY, RECT)
            pygame.draw.rect(screen, CYAN, InRECT)
            
            if board[r][c] ==0:
                pygame.draw.circle(screen, GREY, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),(radius+2))
                pygame.draw.circle(screen, BEIGE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radius)
                
def update_board(board):
    global P1col
    global P2col
    for c in range(COLUMN_COUNT): 
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen, P1col, (int(c*SQUARESIZE+SQUARESIZE/2), boardHeight - int(r*SQUARESIZE+SQUARESIZE/2)),radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, P2col, (int(c*SQUARESIZE+SQUARESIZE/2), boardHeight - int(r*SQUARESIZE+SQUARESIZE/2)),radius)
        pygame.display.update()

def update_cas_leaderboard():
    global score
    global winnername
    r = 7
    stb = 0
    x = 0
    while x != 1:
        if sleaderboard[str(r)] == '__':
            stb = 0
        else:
            stb = int(sleaderboard[str(r)])
        if score > stb:
            r = r-1
        elif score <= stb:
            a = 7
            while a != r:
                sleaderboard[str(a)] = sleaderboard[str(a-1)]
                nleaderboard[str(a)] = nleaderboard[str(a-1)]
                a = a-1
            sleaderboard[str(r+1)] = str(score)
            nleaderboard[str(r+1)] = winnername
            with open('nleader.txt','w') as fp:
                json.dump(nleaderboard, fp)
            with open('sleader.txt','w') as fp:
                json.dump(sleaderboard, fp)
            x = 1
        if r == 0:
            a = 7
            while a>1:
                sleaderboard[str(a)] = sleaderboard[str(a-1)]
                nleaderboard[str(a)] = nleaderboard[str(a-1)]
                a = a - 1
            sleaderboard[str(1)] = str(score)
            nleaderboard[str(1)] = winnername
            with open('nleader.txt','w') as fp:
                json.dump(nleaderboard, fp)
            with open('sleader.txt','w') as fp:
                json.dump(sleaderboard, fp)
            x = 1

def game_seq():
    global winner
    global score
    global P1col
    global P2col
    global nmm
    score = 20
    game_over = False
    nmm = False
    turn = 1
    board = create_board()
    #print_board(board)
    draw_board(board)
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    nmm = True
                    game_over = True
                                    
            elif event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BEIGE, (0,0, boardWidth, SQUARESIZE))
                posx = event.pos[0]
                if turn == 1:
                    pygame.draw.circle(screen, P1col, (posx, int((SQUARESIZE/2))),radius)
                else:
                    pygame.draw.circle(screen, P2col, (posx, int((SQUARESIZE/2))),radius)
                pygame.display.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BEIGE, (0,0, boardWidth, SQUARESIZE))
                #ask for player 1 input
                if turn == 1:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        update_board(board)
                        if winning_move(board, 1):
                            label = winfont.render("Player 1 Wins!", 1, BLACK)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            game_over = True
                        turn = 0
                           
                    else:
                        turn = 1                    
            #ask for player 2 input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        update_board(board)
                        if winning_move(board, 2):
                            label = winfont.render("Player 2 Wins!", 1, BLACK)
                            screen.blit(label, (40,10))
                            pygame.display.update()
                            game_over = True
                        score = score - 1
                        turn = 1
                        if score == -1:
                            gOver = winfont.render("No More Moves!", 1, BLACK)
                            screen.blit(gOver, (40,10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            nmm = True
                            game_over = True
                            
                    else:
                        turn = 0
            #print_board(board)
            if game_over and not nmm:
                winner = turn+1
                pygame.time.wait(3000)
            elif game_over and nmm:
                pass
                

def p1p2entercol():
    global p1p2entcol
    popupoutlineW = 600
    popupoutlineH = 250
    popupW = 592
    popupH = 242
    pygame.draw.rect(screen, BLACK, (screenCenterH - popupoutlineW/2, screenCenterV - popupoutlineH/2, popupoutlineW, popupoutlineH))
    pygame.draw.rect(screen, BEIGE, (screenCenterH - popupW/2, screenCenterV - popupH/2, popupW, popupH))
    playerx = GEfont.render("Players 1 and 2:", 1 , BLACK)
    pxW = playerx.get_width()
    screen.blit(playerx, ((screenCenterH - pxW/2),250))

    choosecol = GEfont.render("Please choose a Colour", 1 , BLACK)
    ccW = choosecol.get_width()
    screen.blit(choosecol, ((screenCenterH - ccW/2)+5,310))
    continuebutton.draw(screen, BLACK)
    pygame.display.update()
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()                         
        pygame.display.update()

        if event.type == pygame.QUIT:
            exit() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if continuebutton.isOver(pos):
                p1p2entcol = False
                casual_game()
        if event.type == pygame.MOUSEMOTION:
            if  continuebutton.isOver(pos):
                continuebutton.color = GREY
            else:
                continuebutton.color = WHITE
                
def p1entercol():
    global p1entcol
    popupoutlineW = 600
    popupoutlineH = 250
    popupW = 592
    popupH = 242
    pygame.draw.rect(screen, BLACK, (screenCenterH - popupoutlineW/2, screenCenterV - popupoutlineH/2, popupoutlineW, popupoutlineH))
    pygame.draw.rect(screen, BEIGE, (screenCenterH - popupW/2, screenCenterV - popupH/2, popupW, popupH))
    playerx = GEfont.render("Player 1:", 1 , BLACK)
    pxW = playerx.get_width()
    screen.blit(playerx, ((screenCenterH - pxW/2),250))

    choosecol = GEfont.render("Please choose a Colour", 1 , BLACK)
    ccW = choosecol.get_width()
    screen.blit(choosecol, ((screenCenterH - ccW/2)+5,310))
    continuebutton.draw(screen, BLACK)
    pygame.display.update()
    for event in pygame.event.get():  
        pos = pygame.mouse.get_pos()                        
        pygame.display.update()

        if event.type == pygame.QUIT:
            exit() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if continuebutton.isOver(pos):
                p1entcol = False
                casual_game()
        if event.type == pygame.MOUSEMOTION:
            if  continuebutton.isOver(pos):
                continuebutton.color = GREY
            else:
                continuebutton.color = WHITE

def p2entercol():
    global p2entcol
    popupoutlineW = 600
    popupoutlineH = 250
    popupW = 592
    popupH = 242
    pygame.draw.rect(screen, BLACK, (screenCenterH - popupoutlineW/2, screenCenterV - popupoutlineH/2, popupoutlineW, popupoutlineH))
    pygame.draw.rect(screen, BEIGE, (screenCenterH - popupW/2, screenCenterV - popupH/2, popupW, popupH))
    playerx = GEfont.render("Player 2:", 1 , BLACK)
    pxW = playerx.get_width()
    screen.blit(playerx, ((screenCenterH - pxW/2),250))

    choosecol = GEfont.render("Please choose a Colour", 1 , BLACK)
    ccW = choosecol.get_width()
    screen.blit(choosecol, ((screenCenterH - ccW/2)+5,310))
    continuebutton.draw(screen, BLACK)
    pygame.display.update()
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()                         
        pygame.display.update()

        if event.type == pygame.QUIT:
            exit() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if continuebutton.isOver(pos):
                p2entcol = False
                casual_game()
        if event.type == pygame.MOUSEMOTION:
            if  continuebutton.isOver(pos):
                continuebutton.color = GREY
            else:
                continuebutton.color = WHITE

def p1p2entersamecol():
    global p1p2entsamecol
    popupoutlineW = 600
    popupoutlineH = 250
    popupW = 592
    popupH = 242
    pygame.draw.rect(screen, BLACK, (screenCenterH - popupoutlineW/2, screenCenterV - popupoutlineH/2, popupoutlineW, popupoutlineH))
    pygame.draw.rect(screen, BEIGE, (screenCenterH - popupW/2, screenCenterV - popupH/2, popupW, popupH))
    playerx = GEfont.render("Players must choose", 1 , BLACK)
    pxW = playerx.get_width()
    screen.blit(playerx, ((screenCenterH - pxW/2),250))

    choosecol = GEfont.render("different Colours", 1 , BLACK)
    ccW = choosecol.get_width()
    screen.blit(choosecol, ((screenCenterH - ccW/2)+5,310))
    continuebutton.draw(screen, BLACK)
    pygame.display.update()
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()                         
        pygame.display.update()

        if event.type == pygame.QUIT:
            exit() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            if continuebutton.isOver(pos):
                p1p2entsamecol = False
                casual_game()
        if event.type == pygame.MOUSEMOTION:
            if  continuebutton.isOver(pos):
                continuebutton.color = GREY
            else:
                continuebutton.color = WHITE
    
'''''''''''''''''''''''''''''''''''''''
             game loop  
'''''''''''''''''''''''''''''''''''''''

game_intro()

while not exit_game:
    while nav == "home":
        home_page()
    while nav == "casual":
        casual_game()
    while nav == "comp":
        comp_game()
    while nav == "leaderboard":
        leaderboard_screen()
    while nav == "quit":
        quit_screen()
        exit_game = True
        nav = 'x'
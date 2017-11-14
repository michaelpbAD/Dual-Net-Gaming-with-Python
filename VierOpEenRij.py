""" Vier op een rij """
import pygame

class VierOpEenRijGame():


    def __init__(self):
        pass

        pygame.init()
        pygame.font.init()

        #speel bord grote in voken
        self.boardBoxH=7
        self.boardBoxW=14

        #box dimensions and border
        self.boxD=50
        self.boxB=int(self.boxD/10)

        #speel bord grote in px
        self.boardH = self.boardBoxH*self.boxD-(self.boardBoxH-1)*self.boxB +self.boxB*4
        self.boardW = self.boardBoxW*self.boxD - (self.boardBoxW-1)*self.boxB +self.boxB*4

        #score bord hoogte
        self.panelH=200

        #venster grote
        self.width = self.boardW
        self.height = self.boardH + self.boxD + self.panelH

        #score bord brete
        self.panelW = self.width

        #initialize the screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VierOpEenRijGame")

        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()

        #defineer bord grote
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]

        #aantal spelers
        self.playerAantal=4

        #defineer wie start
        self.playerTurn=1

        #defineer spaeler naam
        self.playerNaam=["mich","andre","hans","griet"]

        #defineer speler kleur
        self.playerBox=[self.greenBox,self.bleuBox,self.redBox,self.yellowBox]

        #defineer pijl
        self.pijl=self.playerBox[self.playerTurn-1]
        self.pijlx=0
        self.pijly=0

        #defineer scoren
        self.scorePlayer=[0,0,0,0]
        self.wint=0

    def initGraphics(self):
        self.legeBox=pygame.transform.scale( pygame.image.load("legeBox.png"),(self.boxD,self.boxD))
        self.greenBox=pygame.transform.scale( pygame.image.load("greenBox.png"),(self.boxD,self.boxD))
        self.bleuBox=pygame.transform.scale( pygame.image.load("bleuBox.png"),(self.boxD,self.boxD))
        self.redBox=pygame.transform.scale( pygame.image.load("redBox.png"),(self.boxD,self.boxD))
        self.yellowBox=pygame.transform.scale( pygame.image.load("yellowBox.png"),(self.boxD,self.boxD))
        self.score_panel=pygame.transform.scale( pygame.image.load("score_panel.png"),(self.panelW,self.panelH))

    def update(self):
        #sleep to make the game 60 fps
        self.clock.tick(60)

        #clear the screen
        self.screen.fill((255,255,255))
        self.drawBoard()
        self.drawPanel()

        #envents/key pres
        self.eventAndKeys()

        #kontrole
        self.kontrole()

        #vult bord op met winaars kleur
        if self.wint!=0:
            for x in range (self.boardBoxW):
                self.board[0][x]=self.wint

        #update the screen
        pygame.display.flip()

    def eventAndKeys(self):
        #envents/key pres
        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

            #key pres
            if event.type == pygame.KEYDOWN :
                #pijl bewegen
                if event.key==pygame.K_LEFT:
                    if 0<self.pijlx:
                        self.pijlx -= 1
                if event.key==pygame.K_RIGHT:
                    if self.pijlx<(self.boardBoxW-1):
                        self.pijlx += 1

                if (event.key==pygame.K_KP_ENTER or event.key==pygame.K_DOWN) and self.board[0][self.pijlx]==0:
                    self.board[0][self.pijlx]=self.playerTurn
                    if self.playerAantal>self.playerTurn:
                        self.playerTurn+=1
                    else:
                        self.playerTurn=1
                    self.pijl=self.playerBox[self.playerTurn-1]

    def kontrole(self):
        #kontrole gebeurt allen (y,x) (0,+),(+,0),(+,+),(+,-)

        for y in range(self.boardBoxH):
            for x in range(self.boardBoxW):
                if self.board[y][x]!=0:
                    var=self.board[y][x]
                    #horisontale controle
                    if x<(self.boardBoxW-3):

                        if var==self.board[y][x+1] and var==self.board[y][x+2] and var==self.board[y][x+3]:
                            self.wint=var

                    #vertikaal controle
                    if y<(self.boardBoxH-3):

                        if var==self.board[y+1][x] and var==self.board[y+2][x] and var==self.board[y+3][x]:
                            self.wint=var

                    #recht naar beneden controle
                    if y<(self.boardBoxH-3) and x<(self.boardBoxW-3):

                        if var==self.board[y+1][x+1] and var==self.board[y+2][x+2] and var==self.board[y+3][x+3]:
                            self.wint=var

                    #lings naar beneden controle
                    if y<(self.boardBoxH-3) and x>2:

                        if var==self.board[y+1][x-1] and var==self.board[y+2][x-2] and var==self.board[y+3][x-3]:
                            self.wint=var

    def drawBoard(self):

        #box laten vallen
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH-1):
                if self.board[y][x]!=0:
                    if self.board[y+1][x]==0:
                        self.board[y+1][x]=self.board[y][x]
                        self.board[y][x]=0

        #bord tekenen
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH):
                if self.board[y][x]==0:
                    self.screen.blit(self.legeBox, [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])
                if self.board[y][x]!=0:
                    self.screen.blit(self.playerBox[self.board[y][x]-1], [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])

        #plaats pijl
        self.screen.blit(self.pijl,( (self.boxB*2)+((self.pijlx)*self.boxD)-self.boxB*self.pijlx, (self.boxB*2)+((self.pijly)*self.boxD)-self.boxB*self.pijly))

    def drawPanel(self):
        panelP=self.height-self.panelH

        #achtergrond paneel kleur of foto
        #self.screen.blit(self.score_panel, [0, panelP])
        pygame.draw.rect(self.screen,(0,0,0),[0,panelP,self.panelW,self.panelH])

        #print Player Score Labels
        x,y=0,panelP
        for i in range(self.playerAantal):
            if (self.width/2)>300:
                if i%2==0:
                    x=25
                    y+=35
                else :
                    x=(self.width/2)+25
            else:
                x=25
                y+=35
            self.printPlayerScoreLabel (x,y,self.playerBox[i],self.playerNaam[i],self.scorePlayer[i])

    def printPlayerScoreLabel(self, x, y, icon, naam, score):
        myfont = pygame.font.SysFont(None, 42)

        fScore = myfont.render(str(score), 1, (255,255,255))
        fNaam = myfont.render(str(naam), 1, (255,255,255))

        wNaam,hNaam=fNaam.get_size()
        self.screen.blit(pygame.transform.scale(icon,(25,25)), (x,y))
        self.screen.blit(fNaam, (x+50, y))
        self.screen.blit(fScore, (x+250, y))

bg=VierOpEenRijGame() #__init__ is called right here
while 1:
    bg.update()

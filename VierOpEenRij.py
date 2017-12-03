""" Vier op een rij """
import pygame
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class VierOpEenRijGame(ConnectionListener):
    def Network_startgame(self, data): #controleren
        self.running=True
        self.num=data["player"]
        self.gameid=data["gameid"]

    def Network_place(self, data):
        #get attributes
        self.pijlx = data["pijlx"]
        K_DOWN=data["K_DOWN"]

        if K_DOWN==True and self.board[0][self.pijlx]==0:
            self.board[0][self.pijlx]=self.playerTurn
            self.playerTurn=data["playerTurn"]
            self.pijl=self.playerBox[self.playerTurn-1]

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.stopped = False
        # dimensions tiles game board
        self.boardBoxH=7
        self.boardBoxW=14

        #box dimensions and border
        self.boxD=50                 # px length square side
        self.boxB=int(self.boxD/10)  # px border square

        # gameboard dimensions px
        self.boardH = self.boardBoxH*self.boxD-(self.boardBoxH-1)*self.boxB +self.boxB*4
        self.boardW = self.boardBoxW*self.boxD - (self.boardBoxW-1)*self.boxB +self.boxB*4

        #score board height
        self.panelH = 200
        # window dimensions
        self.width = self.boardW
        self.height = self.boardH + self.boxD + self.panelH
        # score board width
        self.panelW = self.width

        # initialize the screen with windows dimensions
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vier op een rij")

        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()

        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]

        # number of players
        self.playerAantal=4

        # define who starts
        self.playerTurn=1

        """ put this all in a dictionary? Andreas """
        #defineer spaeler naam
        self.playerNaam=["speler1","speler2","speler3","speler4"]
        #defineer player color
        self.playerBox=[self.greenBox,self.blueBox,self.redBox,self.yellowBox]
        # define scores
        self.scorePlayer=[0,0,0,0]
        self.wint=0
        """ end dictionary"""

        # define pijl (?)
        self.pijl=self.playerBox[self.playerTurn-1]
        self.pijlx=0
        self.pijly=0

        #drop tijd
        # self.dropTijdInit=1
        # self.dropTijd=self.dropTijdInit

        self.Connect(("LOCALHOST", 31425))#controleren

        self.gameid = None
        self.num = None

        self.running=False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        #determine attributes from player #
        # if self.num==0:
        #     self.turn=True
        #     self.marker = self.greenplayer
        #     self.othermarker = self.blueplayer
        # else:
        #     self.turn=False
        #     self.marker=self.blueplayer
        #     self.othermarker = self.greenplayer
        self.playerNR=self.num+1
        self.playerNaam[self.num]="ik"


    def initGraphics(self):
        self.legeBox=pygame.transform.scale( pygame.image.load("img/legeBox.png"),(self.boxD,self.boxD))
        self.greenBox=pygame.transform.scale( pygame.image.load("img/greenBox.png"),(self.boxD,self.boxD))
        self.blueBox=pygame.transform.scale( pygame.image.load("img/blueBox.png"),(self.boxD,self.boxD))
        self.redBox=pygame.transform.scale( pygame.image.load("img/redBox.png"),(self.boxD,self.boxD))
        self.yellowBox=pygame.transform.scale( pygame.image.load("img/yellowBox.png"),(self.boxD,self.boxD))
        self.scorePanel=pygame.transform.scale( pygame.image.load("img/scorePanel.png"),(self.panelW,self.panelH))

    def update(self):
        connection.Pump()
        self.Pump()

        #sleep to make the game 60 fps
        self.clock.tick(60)
        #clear the screen
        self.screen.fill((255,255,255))
        self.drawBoard()
        self.drawPanel()

        #kontrole
        self.controle()

        #vult bord op met winaars kleur
        if self.wint!=0:
            for x in range(self.boardBoxW):
                self.board[0][x]=self.wint

        #update the screen
        pygame.display.flip()

        # events/key pres
        self.eventAndKeys()

    def eventAndKeys(self):
        connection.Pump()
        self.Pump()
        #envents/key pres
        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.stopped = True
                pygame.display.quit()

            # key press
            if event.type == pygame.KEYDOWN and self.playerNR==self.playerTurn:
                # pijl move
                if event.key==pygame.K_LEFT:
                    if 0<self.pijlx:
                        self.pijlx -= 1
                        connection.Send({"action": "place","playerTurn":self.playerTurn, "pijlx":self.pijlx,"K_DOWN":False,"gameid": self.gameid, "playerNR": self.playerNR})

                if event.key==pygame.K_RIGHT:
                    if self.pijlx<(self.boardBoxW-1):
                        self.pijlx += 1
                        connection.Send({"action": "place","playerTurn":self.playerTurn, "pijlx":self.pijlx,"K_DOWN":False,"gameid": self.gameid, "playerNR": self.playerNR})

                if (event.key==pygame.K_KP_ENTER or event.key==pygame.K_DOWN) and self.board[0][self.pijlx]==0:
                    # self.board[0][self.pijlx]=self.playerTurn
                    # if self.playerAantal>self.playerTurn:
                    #     self.playerTurn+=1
                    # else:
                    #     self.playerTurn=1
                    # self.pijl=self.playerBox[self.playerTurn-1]
                    connection.Send({"action": "place","playerTurn":self.playerTurn, "pijlx":self.pijlx,"K_DOWN":True,"gameid": self.gameid, "playerNR": self.playerNR})

    def controle(self):
        # controle gebeurt alleen (y,x) (0,+),(+,0),(+,+),(+,-)
        for y in range(self.boardBoxH):
            for x in range(self.boardBoxW):
                if self.board[y][x]!=0:
                    var=self.board[y][x]
                    # horizontale controle
                    if x<(self.boardBoxW-3):

                        if var==self.board[y][x+1] and var==self.board[y][x+2] and var==self.board[y][x+3]:
                            self.wint=var

                    # verticale controle
                    if y<(self.boardBoxH-3):

                        if var==self.board[y+1][x] and var==self.board[y+2][x] and var==self.board[y+3][x]:
                            self.wint=var

                    # rechts naar beneden controle
                    if y<(self.boardBoxH-3) and x<(self.boardBoxW-3):

                        if var==self.board[y+1][x+1] and var==self.board[y+2][x+2] and var==self.board[y+3][x+3]:
                            self.wint=var

                    # links naar beneden controle
                    if y<(self.boardBoxH-3) and x>2:

                        if var==self.board[y+1][x-1] and var==self.board[y+2][x-2] and var==self.board[y+3][x-3]:
                            self.wint=var

    def drawBoard(self):

        # drop box
        # if self.dropTijd<=0:
        #     self.dropTijd=self.dropTijdInit
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH-1):
                if self.board[y][x]!=0:
                    if self.board[y+1][x]==0:
                        self.board[y+1][x]=self.board[y][x]
                        self.board[y][x]=0
        # else:
        #     self.dropTijd-=1

        # draw game board
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH):
                if self.board[y][x]==0:
                    self.screen.blit(self.legeBox, [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])
                if self.board[y][x]!=0:
                    self.screen.blit(self.playerBox[self.board[y][x]-1], [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])

        # place pijl
        self.screen.blit(self.pijl,( (self.boxB*2)+((self.pijlx)*self.boxD)-self.boxB*self.pijlx, (self.boxB*2)+((self.pijly)*self.boxD)-self.boxB*self.pijly))

    def drawPanel(self):
        panelP=self.height-self.panelH

        #achtergrond paneel kleur of foto
        #self.screen.blit(self.scorePanel, [0, panelP])
        pygame.draw.rect(self.screen,(0,0,0),[0,panelP,self.panelW,self.panelH])

        #print Player Score Labels
        x,y=0,panelP
        for i in range(self.playerAantal):
            if (self.width/2)>300:
                if i % 2==0:
                    x=25
                    y+=35
                else:
                    x=(self.width/2)+25
            else:
                x=25
                y+=35
            self.printPlayerScoreLabel(x,y,self.playerBox[i],self.playerNaam[i],self.scorePlayer[i])

    def printPlayerScoreLabel(self, x, y, icon, naam, score):
        myfont = pygame.font.SysFont(None, 42)

        fScore = myfont.render(str(score), 1, (255,255,255))
        fNaam = myfont.render(str(naam), 1, (255,255,255))

        wNaam,hNaam=fNaam.get_size()
        self.screen.blit(pygame.transform.scale(icon,(25,25)), (x,y))
        self.screen.blit(fNaam, (x+50, y))
        self.screen.blit(fScore, (x+250, y))



bg=VierOpEenRijGame()
while 1:
    bg.update()

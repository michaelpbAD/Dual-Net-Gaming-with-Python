"""inlade"""
import pygame

class VierOpEenRijGame():


    def __init__(self):
        pass
        #1
        pygame.init()

        self.boardBoxH=7
        self.boardBoxW=7

        self.boxD=100
        self.boxB=int(self.boxD/10)

        width, height = self.boardBoxW*self.boxD - (self.boardBoxW-1)*self.boxB +self.boxB*4, self.boxD+self.boardBoxH*self.boxD-(self.boardBoxH-1)*self.boxB +self.boxB*4
        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("VierOpEenRijGame")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()

        #defineer bord grote
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]

        self.playerTurn=1

        self.player1Box=self.greenBox
        self.player2Box=self.bleuBox

        if self.playerTurn==1:
            self.pijl=self.player1Box
        elif self.playerTurn==2:
            self.pijl=self.player2Box
        self.pijlx=0
        self.pijly=0

        self.wint=0


    def initGraphics(self):
        self.legeBox=pygame.transform.scale( pygame.image.load("legeBox.png"),(self.boxD,self.boxD))
        self.greenBox=pygame.transform.scale( pygame.image.load("greenBox.png"),(self.boxD,self.boxD))
        self.bleuBox=pygame.transform.scale( pygame.image.load("bleuBox.png"),(self.boxD,self.boxD))

    def update(self):
        #sleep to make the game 60 fps
        self.clock.tick(60)

        #clear the screen
        self.screen.fill((255,255,255))
        self.drawBoard()

        #envents/key pres
        self.eventAndKeys()

        #kontrole
        self.kontrole()

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

                if event.key==pygame.K_KP_ENTER and self.board[0][self.pijlx]==0:
                    self.board[0][self.pijlx]=self.playerTurn
                    if self.playerTurn==1:
                        self.playerTurn=2
                        self.pijl=self.player2Box
                    elif self.playerTurn==2:
                        self.playerTurn=1
                        self.pijl=self.player1Box

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
                if self.board[y][x]==1:
                    self.screen.blit(self.player1Box, [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])
                if self.board[y][x]==2:
                    self.screen.blit(self.player2Box, [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, self.boxD+(self.boxB*2)+((y)*self.boxD)-self.boxB*y])

        #plaats pijl
        self.screen.blit(self.pijl,( (self.boxB*2)+((self.pijlx)*self.boxD)-self.boxB*self.pijlx, (self.boxB*2)+((self.pijly)*self.boxD)-self.boxB*self.pijly))


bg=VierOpEenRijGame() #__init__ is called right here
while 1:
    bg.update()

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

        width, height = self.boardBoxW*self.boxD - (self.boardBoxW-1)*self.boxB +self.boxB*4, self.boardBoxH*self.boxD-(self.boardBoxH-1)*self.boxB +self.boxB*4
        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("VierOpEenRijGame")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()
    
    def initGraphics(self):
        self.legeBox=pygame.transform.scale( pygame.image.load("legeBox.png"),(self.boxD,self.boxD))
        self.greenBox=pygame.transform.scale( pygame.image.load("greenBox.png"),(self.boxD,self.boxD))
        self.orangeBox=pygame.transform.scale( pygame.image.load("orangeBox.png"),(self.boxD,self.boxD))

    def update(self):
        #sleep to make the game 60 fps
        self.clock.tick(60)

        #clear the screen
        self.screen.fill((255,255,255))
        self.drawBoard()

        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()

        #update the screen
        pygame.display.flip()

        #defineer bord grote
        
        self.board = [[False for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
    
    def drawBoard(self):
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH):
                #if not self.board[y][x]:
                self.screen.blit(self.legeBox, [(self.boxB*2)+((x)*self.boxD)-self.boxB*x, (self.boxB*2)+((y)*self.boxD)-self.boxB*y])
        
        
bg=VierOpEenRijGame() #__init__ is called right here
while 1:
    bg.update()
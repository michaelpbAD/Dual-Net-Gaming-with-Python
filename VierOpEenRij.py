""" Vier op een rij - Client"""
import pygame
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class VierOpEenRijGame(ConnectionListener):
    def Network_close(self, data):
        exit()

    def Network_connected(self, data):
        print("Connected to the server.")

    def Network_error(self, data):
        print("Error connecting to the server.")
        exit()

    def Network_disconnected(self, data):
        print("Disconnected from the server.")
        exit()

    def Network_nickname(self,data):
        self.playerNaam[data["playerNR"]-1] = data["nickname"]

    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]
        self.playerAantal = data["playerAantal"]
        self.boardBoxH = data["boardBoxH"]
        self.boardBoxW = data["boardBoxW"]

        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]

        #dimensies van scherm aanpassen naar spel grote
        # gameboard dimensions px
        self.boardH = self.boardBoxH * self.boxD - (self.boardBoxH - 1) * self.boxB + self.boxB * 4
        self.boardW = self.boardBoxW * self.boxD - (self.boardBoxW - 1) * self.boxB + self.boxB * 4
        # score board height
        self.panelH = 200
        # window dimensions
        self.width = self.boardW
        self.height = self.boardH + self.boxD + self.panelH
        # score board width
        self.panelW = self.width
        # initialize the screen with windows dimensions
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vier op een rij")

    def Network_place(self, data):
        # get attributes
        self.pijlx = data["pijlx"]
        K_DOWN = data["K_DOWN"]

        if K_DOWN == True and self.board[0][self.pijlx] == 0:
            self.board[0][self.pijlx] = self.playerTurn
            self.playerTurn = data["playerTurn"]
            self.pijl = self.playerBox[self.playerTurn - 1]

    def Network_win(self, data):
        self.wint = data["speler"]
        self.scorePlayer = data["score"]

    def Network_boardWipe(self, data):
        self.wint = data["wint"]
        self.board = data["board"]
        self.playerTurn = data["playerTurn"]
        self.pijl = self.playerBox[self.playerTurn - 1]

    # initialize VierOpEenRijGame
    def __init__(self, socket, nickname):
        pygame.init()
        pygame.font.init()
        # dimensions tiles game board
        self.boardBoxH = 7
        self.boardBoxW = 14

        # box dimensions and border
        self.boxD = 50  # px length square side
        self.boxB = int(self.boxD / 10)  # px border square

        # gameboard dimensions px
        self.boardH = self.boardBoxH * self.boxD - (self.boardBoxH - 1) * self.boxB + self.boxB * 4
        self.boardW = self.boardBoxW * self.boxD - (self.boardBoxW - 1) * self.boxB + self.boxB * 4

        # score board height
        self.panelH = 200
        # window dimensions
        self.width = self.boardW
        self.height = self.boardH + self.boxD + self.panelH
        # score board width
        self.panelW = self.width

        # initialize the screen with windows dimensions
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vier op een rij")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initGraphics()

        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]

        # define who starts
        self.playerTurn = 1

        # defineer spaeler naam
        self.playerNaam = ["speler1", "speler2", "speler3", "speler4"]
        # defineer player color
        self.playerBox = [self.greenBox, self.blueBox, self.redBox, self.yellowBox]
        # define scores
        self.scorePlayer = [0, 0, 0, 0]
        self.wint = 0

        # define pijl
        self.pijl = self.playerBox[self.playerTurn - 1]
        self.pijlx = 0
        self.pijly = 0

        # try to connect
        try:
            self.Connect((socket[0], int(socket[1])))
        except:
            pass

        self.gameid = None
        self.num = None
        self.running = False
        # wait until game starts
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.001)
        # determine attributes from player #
        self.playerNR = self.num + 1
        self.playerNaam[self.num] = "me > "+nickname
        connection.Send({"action": "nickname", "nickname": nickname, "gameid": self.gameid, "playerNR": self.playerNR})

    # initialize graphics images
    def initGraphics(self):
        self.legeBox = pygame.transform.scale(pygame.image.load("img/legeBox.png"), (self.boxD, self.boxD))
        self.greenBox = pygame.transform.scale(pygame.image.load("img/greenBox.png"), (self.boxD, self.boxD))
        self.blueBox = pygame.transform.scale(pygame.image.load("img/blueBox.png"), (self.boxD, self.boxD))
        self.redBox = pygame.transform.scale(pygame.image.load("img/redBox.png"), (self.boxD, self.boxD))
        self.yellowBox = pygame.transform.scale(pygame.image.load("img/yellowBox.png"), (self.boxD, self.boxD))
        #self.scorePanel = pygame.transform.scale(pygame.image.load("img/scorePanel.png"), (self.panelW, self.panelH))

    # update game
    def update(self):
        connection.Pump()
        self.Pump()
        # sleep to make the game 60 fps
        self.clock.tick(60)
        # clear the screen
        self.screen.fill((255, 255, 255))
        self.drawBoard()
        self.drawPanel()

        # vult bord op met winaars kleur
        if self.wint != 0:
            for x in range(self.boardBoxW):
                self.board[0][x] = self.wint

        # update the screen
        pygame.display.flip()

        # events/key press
        self.eventAndKeys()

    # handling events and key presses
    def eventAndKeys(self):
        for event in pygame.event.get():
            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit()
            # key press
            if event.type == pygame.KEYDOWN and self.playerTurn == self.playerNR:
                # pijl move links wanneer linker pijl
                if event.key == pygame.K_LEFT:
                    if 0 < self.pijlx:
                        self.pijlx -= 1
                        connection.Send(
                            {"action": "place", "playerTurn": self.playerTurn, "pijlx": self.pijlx, "K_DOWN": False,
                             "gameid": self.gameid, "playerNR": self.playerNR})
                # pijl move rechts wanneer rechterpijl
                if event.key == pygame.K_RIGHT:
                    if self.pijlx < (self.boardBoxW - 1):
                        self.pijlx += 1
                        connection.Send(
                            {"action": "place", "playerTurn": self.playerTurn, "pijlx": self.pijlx, "K_DOWN": False,
                             "gameid": self.gameid, "playerNR": self.playerNR})
                # place box wanneer enter of pijl naar beneden
                if (event.key == pygame.K_KP_ENTER or event.key == pygame.K_DOWN) and self.board[0][self.pijlx] == 0:
                    connection.Send(
                        {"action": "place", "playerTurn": self.playerTurn, "pijlx": self.pijlx, "K_DOWN": True,
                         "gameid": self.gameid, "playerNR": self.playerNR})

    # print dropped box, gameboard en pijl
    def drawBoard(self):
        # drop box
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH - 1):
                if self.board[y][x] != 0:
                    if self.board[y + 1][x] == 0:
                        self.board[y + 1][x] = self.board[y][x]
                        self.board[y][x] = 0
        # draw game board
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH):
                if self.board[y][x] == 0:
                    self.screen.blit(self.legeBox, [(self.boxB * 2) + ((x) * self.boxD) - self.boxB * x,
                                                    self.boxD + (self.boxB * 2) + ((y) * self.boxD) - self.boxB * y])
                if self.board[y][x] != 0:
                    self.screen.blit(self.playerBox[self.board[y][x] - 1],
                                     [(self.boxB * 2) + ((x) * self.boxD) - self.boxB * x,
                                      self.boxD + (self.boxB * 2) + ((y) * self.boxD) - self.boxB * y])
        # place pijl
        self.screen.blit(self.pijl, ((self.boxB * 2) + ((self.pijlx) * self.boxD) - self.boxB * self.pijlx,
                                     (self.boxB * 2) + ((self.pijly) * self.boxD) - self.boxB * self.pijly))
    # print score paneel
    def drawPanel(self):
        panelP = self.height - self.panelH
        # achtergrond paneel kleur of foto
        # self.screen.blit(self.scorePanel, [0, panelP])
        pygame.draw.rect(self.screen, (0, 0, 0), [0, panelP, self.panelW, self.panelH])
        # print Player Score Labels
        x, y = 0, panelP
        for i in range(self.playerAantal):
            if (self.width / 2) > 300:
                if i % 2 == 0:
                    x = 25
                    y += 35
                else:
                    x = (self.width / 2) + 25
            else:
                x = 25
                y += 35
            self.printPlayerScoreLabel(x, y, self.playerBox[i], self.playerNaam[i], self.scorePlayer[i])
    # print player scores
    def printPlayerScoreLabel(self, x, y, icon, naam, score):
        myfont = pygame.font.SysFont(None, 42)

        fScore = myfont.render(str(score), 1, (255, 255, 255))
        fNaam = myfont.render(str(naam), 1, (255, 255, 255))

        wNaam, hNaam = fNaam.get_size()
        self.screen.blit(pygame.transform.scale(icon, (25, 25)), (x, y))
        self.screen.blit(fNaam, (x + 50, y))
        self.screen.blit(fScore, (x + 250, y))

from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def Network(self, data):
        print(data)

    def Network_place(self, data):
        # deconsolidate all of the data from the dictionary
        playerTurn = data["playerTurn"]
        pijlx = data["pijlx"]
        K_DOWN = data["K_DOWN"]

        playerNR = data["playerNR"]

        # id of game given by server at start of game
        self.gameid = data["gameid"]

        # tells server to place line
        self._server.placeLine(playerTurn, pijlx, K_DOWN, data, self.gameid, playerNR)

    def Network_nickname(self, data):
        self._server.nickname(data)

    def Close(self):
        self._server.close(self.gameid)


class vieropeenrijServer(Server):
    def __init__(self, maxPlayers,*args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.maxPlayers = maxPlayers
        self.games = []
        self.queue = None
        self.currentIndex = 0
        self.numPlayers = 0

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        self.numPlayers += 1
        print('new connection:', channel)

        if self.queue == None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex, self.maxPlayers)
        elif self.numPlayers == 2:
            channel.gameid = self.currentIndex
            self.queue.player[1] = channel
        elif self.numPlayers == 3:
            channel.gameid = self.currentIndex
            self.queue.player[2] = channel
        elif self.numPlayers == 4:
            channel.gameid = self.currentIndex
            self.queue.player[3] = channel

        if self.numPlayers >= self.queue.playerAantal:
            for i in range(self.queue.playerAantal):
                self.queue.player[i].Send({"action": "startgame", "player": i, "gameid": self.queue.gameid, "playerAantal": self.queue.playerAantal, "boardBoxH": self.queue.boardBoxH, "boardBoxW": self.queue.boardBoxW})

            self.games.append(self.queue)
            self.queue = None
            self.numPlayers=0

    def placeLine(self, playerTurn, pijlx, K_DOWN, data, gameid, playerNR):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeLine(playerTurn, pijlx, K_DOWN, data, playerNR)

    def tick(self):
        for game in self.games:
            if game.wint != 0:
                game.wint = 0
                game.Turn = 1
                game.board = [[0 for x in range(game.boardBoxW)] for y in range(game.boardBoxH)]
                sleep(2)
                for i in range(game.playerAantal):
                    game.player[i].Send(
                        {"action": "boardWipe", "board": game.board, "playerTurn": game.Turn, "wint": game.wint})
        self.Pump()

    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid == gameid][0]
            for i in range(game.playerAantal):
                game.player[i].Send({"action": "close"})
        except:
            pass

    def nickname(self, data):
        game = [a for a in self.games if a.gameid == data["gameid"]][0]
        for i in range(game.playerAantal):
            if i != data["playerNR"]-1:
                game.player[i].Send({"action": "nickname", "playerNR": data["playerNR"], "nickname": data["nickname"]})


class Game(object):
    def __init__(self, player0, currentIndex, maxPlayers):
        # whose turn
        self.Turn = 1
        self.playerAantal = maxPlayers
        # dimensions tiles game board
        self.boardBoxH = 7
        self.boardBoxW = 20
        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        # initialize the players including the one who started the game
        self.player = [player0, None, None, None]
        self.scorePlayer = [0, 0, 0, 0]
        self.wint = 0

        # gameid of game
        self.gameid = currentIndex

    def placeLine(self, playerTurn, pijlx, K_DOWN, data, playerNR):
        # make sure it's their turn
        if playerNR == self.Turn:
            if K_DOWN == True and self.board[0][pijlx] == 0:
                # plaats box
                self.board[0][pijlx] = self.Turn
                # volgende speler
                if self.playerAantal > self.Turn:
                    self.Turn += 1
                else:
                    self.Turn = 1
                data["playerTurn"] = self.Turn
        # send data and turn data to each player
        for i in range(self.playerAantal):
            self.player[i].Send(data)

        self.dropBox()
        self.controle()
        if self.wint != 0:
            self.scorePlayer[self.wint - 1] += 1
            for i in range(self.playerAantal):
                self.player[i].Send({"action": "win", "speler": self.wint, "score": self.scorePlayer})

    def dropBox(self):
        for x in range(self.boardBoxW):
            for y in range(self.boardBoxH - 1):
                if self.board[y][x] != 0:
                    if self.board[y + 1][x] == 0:
                        self.board[y + 1][x] = self.board[y][x]
                        self.board[y][x] = 0

    def controle(self):
        # controle gebeurt alleen (y,x) (0,+),(+,0),(+,+),(+,-)
        for y in range(self.boardBoxH):
            for x in range(self.boardBoxW):
                if self.board[y][x] != 0:
                    var = self.board[y][x]
                    # horizontale controle
                    if x < (self.boardBoxW - 3):
                        if var == self.board[y][x + 1] and var == self.board[y][x + 2] and var == self.board[y][x + 3]:
                            self.wint = var

                    # verticale controle
                    if y < (self.boardBoxH - 3):
                        if var == self.board[y + 1][x] and var == self.board[y + 2][x] and var == self.board[y + 3][x]:
                            self.wint = var

                    # rechts naar beneden controle
                    if y < (self.boardBoxH - 3) and x < (self.boardBoxW - 3):
                        if var == self.board[y + 1][x + 1] and var == self.board[y + 2][x + 2] and var == \
                                self.board[y + 3][x + 3]:
                            self.wint = var

                    # links naar beneden controle
                    if y < (self.boardBoxH - 3) and x > 2:

                        if var == self.board[y + 1][x - 1] and var == self.board[y + 2][x - 2] and var == \
                                self.board[y + 3][x - 3]:
                            self.wint = var


##print("STARTING SERVER ON LOCALHOST")
#vieropenrijServer = vieropeenrijServer(localaddr=("LOCALHOST", 31425))


# def updateVierServer():
#     vieropenrijServer.Pump()
#     sleep(0.01)
#     vieropenrijServer.tick()


# def updateServer():
#     print("Clock is ticking")
#     vieropenrijServer.Pump()
#     sleep(0.0001)

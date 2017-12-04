from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ClientChannel(Channel):
    def Network(self, data):
        print(data)

    def Network_placeBox(self, data):
        # deconsolidate all of the data from the dictionary
        playerTurn = data["playerTurn"]
        pijlx = data["pijlx"]

        playerNR = data["playerNR"]

        # id of game given by server at start of game
        self.gameid = data["gameid"]

        # tells server to place line
        self._server.placeBox(playerTurn, pijlx, data, self.gameid, playerNR)

    def Network_movePijl(self,data):
        print(data)
        pijlx = data["pijlx"]
        gameid = data["gameid"]
        self._server.movePijl(pijlx, gameid, data)

    def Close(self):
        self._server.close(self.gameid)

class vieropeenrijServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):  # controleren
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        self.numPlayers = 0

    def Connected(self, channel, addr):  # controleren
        self.numPlayers += 1
        print('new connection:', channel)

        if self.queue == None:  # controleren
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameid = self.currentIndex
            ##self.queue.player1 = channel
            self.queue.player[(self.numPlayers-1)%self.queue.playerAantal] = channel
        # elif self.numPlayers == 3 :
        #     channel.gameid = self.currentIndex
        #     self.queue.player[2] = channel
        # elif self.numPlayers == 4:
        #     channel.gameid = self.currentIndex
        #     self.queue.player[3] = channel

        if self.numPlayers == self.queue.playerAantal:
            for i in range(self.queue.playerAantal):
                self.queue.player[i].Send({"action": "startgame", "player": i, "gameid": self.queue.gameid,"playerAantal": self.queue.playerAantal})
            self.games.append(self.queue)
            self.queue = None
            # self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            # self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            # self.queue.player2.Send({"action": "startgame", "player": 2, "gameid": self.queue.gameid})
            # self.queue.player3.Send({"action": "startgame", "player": 3, "gameid": self.queue.gameid})


    def movePijl(self,pijlx,gameid, data):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].movePijl(pijlx, data)

    def placeBox(self, playerTurn, pijlx, data, gameid, playerNR):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeBox(playerTurn, pijlx, data, playerNR)
    def close(self,gameid):
        try:
            game = [a for a in self.games if a.gameid == gameid]
            for i in range(self.queue.playerAantal):
                game.player[i].Send({"action": "close", "gameid": gameid})
        except:
            pass

class Game:  # controleren
    def __init__(self, player0, currentIndex):
        # whose turn
        self.Turn = 1
        self.playerAantal = 3
        # dimensions tiles game board
        self.boardBoxH = 7
        self.boardBoxW = 14
        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        # initialize the players including the one who started the game
        self.player=[player0,None,None,None]
        #self.player0 = player0
        # self.player1 = None
        # self.player2 = None
        # self.player3 = None
        # gameid of game
        self.gameid = currentIndex

    def movePijl(self, pijlx, data):
        for i in range(self.playerAantal):
            self.player[i].Send(data)
        # self.player[0].Send(data)
        # self.player[1].Send(data)
        # self.player2.Send(data)
        # self.player3.Send(data)

    def placeBox(self, playerTurn, pijlx, data, playerNR):
        # make sure it's their turn
        if playerNR == self.Turn:
            #  and self.board[0][pijlx]==0:
            # self.board[0][pijlx]=self.playerTurn
            if self.playerAantal > self.Turn:
                self.Turn += 1
            else:
                self.Turn = 1
            # self.Turn=playerTurn
            data["playerTurn"] = self.Turn
        # send data and turn data to each player
        for i in range(self.playerAantal):
            self.player[i].Send(data)
        # self.player2.Send(data)
        # self.player3.Send(data)


print("STARTING SERVER ON LOCALHOST")
vieropenrijServer = vieropeenrijServer(localaddr=("LOCALHOST", 31425))

while 1:
    vieropenrijServer.Pump()
    sleep(0.01)
#
# def updateServer():
#     print("Clock is ticking")
#     vieropenrijServer.Pump()
#     sleep(0.0001)

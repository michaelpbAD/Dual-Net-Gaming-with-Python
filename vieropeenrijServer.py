from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
    def Network(self, data):
        self.gameid = data["gameid"]
        print(data)

    def Network_placeBox(self, data):
        # deconsolidate all of the data from the dictionary
        playerTurn = data["playerTurn"]
        pijlx = data["pijlx"]
        playerNR = data["playerNR"]
        # id of game given by server at start of game
        self.gameid = data["gameid"]
        # tells server to place box
        self._server.placeBox(playerTurn, pijlx, data, self.gameid, playerNR)

    def Network_movePijl(self,data):
        pijlx = data["pijlx"]
        self.gameid = data["gameid"]
        self._server.movePijl(pijlx, self.gameid, data)

    def Close(self):
        self._server.close(self.gameid)

class vieropeenrijServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        self.numPlayers = 0

    def Connected(self, channel, addr):
        self.numPlayers += 1
        print('new connection:', channel)
        print(self.queue)
        if self.queue == None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameid = self.currentIndex
            self.queue.player[(self.numPlayers-1)%self.queue.playerAantal] = channel

        if self.numPlayers > 1 and self.numPlayers%self.queue.playerAantal == 0:
            for i in range(self.queue.playerAantal):
                self.queue.player[i].Send({"action": "startgame", "player": i, "gameid": self.queue.gameid,"playerAantal": self.queue.playerAantal})
            self.games.append(self.queue)
            for a in self.games:
                print(a)
            self.queue = None

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
            game = [a for a in self.games if a.gameid == gameid][0]
            for i in range(game.playerAantal):
                game.player[i].Send({"action": "close", "gameid": gameid})
        except:
            pass

class Game:  # controleren
    def __init__(self, player0, currentIndex):
        # whose turn
        self.Turn = 1
        self.playerAantal = 2
        # dimensions tiles game board
        self.boardBoxH = 7
        self.boardBoxW = 14
        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        # initialize the players including the one who started the game
        self.player=[player0,None,None,None]
        # gameid of game
        self.gameid = currentIndex

    def movePijl(self, pijlx, data):
        for i in range(self.playerAantal):
            self.player[i].Send(data)

    def placeBox(self, playerTurn, pijlx, data, playerNR):
        # make sure it's their turn
        if playerNR == self.Turn:
            #  and self.board[0][pijlx]==0:
            # self.board[0][pijlx]=self.playerTurn
            if self.playerAantal > self.Turn:
                self.Turn += 1
            else:
                self.Turn = 1
            data["playerTurn"] = self.Turn
        # send data and turn data to each player
        for i in range(self.playerAantal):
            self.player[i].Send(data)


print("STARTING SERVER ON LOCALHOST")
server = vieropeenrijServer(localaddr=("LOCALHOST", 31425))

while 1:
    server.Pump()
    sleep(0.01)


 # def updateServer():
 #    print("Clock is ticking")
 #    vieropenrijServer.Pump()
 #    sleep(0.0001)

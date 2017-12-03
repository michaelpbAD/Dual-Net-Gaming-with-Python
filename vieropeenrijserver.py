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

    def Close(self):
        self._server.close(self.gameid)


class vieropeenrijServer(Server):
    def __init__(self, *args, **kwargs):  # controleren
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        self.numPlayers = 0

    channelClass = ClientChannel

    def Connected(self, channel, addr):  # controleren
        self.numPlayers += 1
        print('new connection:', channel)

        if self.queue == None:  # controleren
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        elif self.numPlayers == 2:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
        elif self.numPlayers == 3:
            channel.gameid = self.currentIndex
            self.queue.player2 = channel
        else:
            channel.gameid = self.currentIndex
            self.queue.player3 = channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            self.queue.player2.Send({"action": "startgame", "player": 2, "gameid": self.queue.gameid})
            self.queue.player3.Send({"action": "startgame", "player": 3, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None

    def placeLine(self, playerTurn, pijlx, K_DOWN, data, gameid, playerNR):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeLine(playerTurn, pijlx, K_DOWN, data, playerNR)


class Game(object):  # controleren
    def __init__(self, player0, currentIndex):
        # whose turn
        self.Turn = 1
        self.playerAantal = 4
        # dimensions tiles game board
        self.boardBoxH = 7
        self.boardBoxW = 14
        # define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        # initialize the players including the one who started the game
        self.player0 = player0
        self.player1 = None
        self.player2 = None
        self.player3 = None

        # gameid of game
        self.gameid = currentIndex

    def placeLine(self, playerTurn, pijlx, K_DOWN, data, playerNR):
        # make sure it's their turn
        if playerNR == self.Turn:
            if K_DOWN == True:
                #  and self.board[0][pijlx]==0:
                # self.board[0][pijlx]=self.playerTurn
                if self.playerAantal > self.Turn:
                    self.Turn += 1
                else:
                    self.Turn = 1
                # self.Turn=playerTurn
                data["playerTurn"] = self.Turn
        # send data and turn data to each player
        self.player0.Send(data)
        self.player1.Send(data)
        self.player2.Send(data)
        self.player3.Send(data)


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

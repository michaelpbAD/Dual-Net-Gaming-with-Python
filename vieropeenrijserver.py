from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	def Network(self, data):
		print(data)

	def Network_place(self, data):
        #deconsolidate all of the data from the dictionary
		playerTurn = data["playerTurn"]
		pijlx = data["pijlx"]
		K_DOWN = data["K_DOWN"]

		num=data["num"]

        #id of game given by server at start of game
		self.gameid = data["gameid"]

        #tells server to place line
		self._server.placeLine(hv, x, y, data, self.gameid, num)
	def Close(self):
		self._server.close(self.gameid)

class vieropeenrijServer(Server):
	def __init__(self, *args, **kwargs): #controleren
	    Server.__init__(self, *args, **kwargs)
	    self.games = []
	    self.queue = None
	    self.currentIndex=0

	channelClass = ClientChannel

	def Connected(self, channel, addr): #controleren
		print('new connection:', channel)

		if self.queue==None:#controleren
		    self.currentIndex+=1
		    channel.gameid=self.currentIndex
		    self.queue=Game(channel, self.currentIndex)
		else:
		    channel.gameid=self.currentIndex
		    self.queue.player1=channel
		    self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
		    self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
		    self.games.append(self.queue)
		    self.queue=None

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

class Game(): #controleren
    def __init__(self, player0, currentIndex):
        # whose turn
        self.turn = 1
        # dimensions tiles game board
        self.boardBoxH=7
        self.boardBoxW=14
		# define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        #initialize the players including the one who started the game
        self.player0=player0
        self.player1=None
        #gameid of game
        self.gameid=currentIndex

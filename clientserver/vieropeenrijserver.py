from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	def Network(self, data):
		#print(data)
		print("")

	def Network_place(self, data):
		print(data)

class vieropeenrijServer(Server):
	def __init__(self, *args, **kwargs): #controleren
	    PodSixNet.Server.Server.__init__(self, *args, **kwargs)
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
vieropenrijServer = vieropeenrijServer(localaddr=("192.168.1.77", 31425))

while 1:
	vieropenrijServer.Pump()
	sleep(0.01)
#
# def updateServer():
#     print("Clock is ticking")
#     vieropenrijServer.Pump()
#     sleep(0.0001)

class Game: #controleren
    def __init__(self, player0, currentIndex):
        # whose turn
        self.turn = 1
        # dimensions tiles game board
        self.boardBoxH=7
        self.boardBoxW=14
		# define game board dimensions
        self.board = [[0 for x in range(self.boardBoxW)] for y in range(self.boardBoxH)]
        #initialize the players including the one who started the game
        self.playerNaam=[player0,None,None,None]
        #gameid of game
        self.gameid=currentIndex

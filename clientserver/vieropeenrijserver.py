from time import sleep
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	def Network(self, data):
		print(data)

	# def Network_myaction(self, data):
	# 	print("myaction:", data)

class vieropeenrijServer(Server):

	channelClass = ClientChannel

	def Connected(self, channel, addr):
		print('new connection:', channel)

print("STARTING SERVER ON LOCALHOST")
vieropenrijServer = vieropeenrijServer(localaddr=("localhost", 31425))

while 1:
	vieropenrijServer.Pump()
	sleep(0.01)
#
# def updateServer():
#     print("Clock is ticking")
#     vieropenrijServer.Pump()
#     sleep(0.0001)

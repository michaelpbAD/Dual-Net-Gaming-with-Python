

# connect to the server - optionally pass hostname and port like: ("mccormick.cx", 31425)


from PodSixNet.Connection import ConnectionListener

class MyNetworkListener(ConnectionListener):

	def Network(self, data):
		print('network data:', data)

	def Network_connected(self, data):
		print("connected to the server")

	def Network_error(self, data):
		print ("error:", data['error'][1])

	def Network_disconnected(self, data):
		print( "disconnected from the server")

	def Network_myaction(data):
		print ("myaction:", data)

	


class MyPlayerListener(ConnectionListener):

	def Network_numplayers(data):
		# update gui element displaying the number of currently connected players
		print(data['players'])

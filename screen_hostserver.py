from tkinter import *
from tkinter import ttk
from time import sleep


class screenServer():

    def __init__(self, socket, maxPlayers):
        self.root = Tk()
        self.root.title("Vier op een rij: Server")  # title of window
        self.serverframe = ttk.Frame(self.root, padding="80 80 80 80")  # padding of frame
        self.serverframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        self.serverframe.columnconfigure(0, weight=1)
        self.serverframe.rowconfigure(0, weight=1)
        ttk.Label(self.serverframe, text="Running the server...").grid(column=2, row=1, sticky=(W, E))

        ### server has to be started here
        import vieropeenrijserver
        self.hosting = vieropeenrijserver.vieropeenrijServer(maxPlayers, localaddr=(socket[0], int(socket[1])))

    def update(self):
        self.root.update()
        self.hosting.Pump()
        self.hosting.tick()
        sleep(0.001)

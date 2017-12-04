from tkinter import *
from tkinter import ttk
from time import sleep


class screenServer():

    def __init__(self, socket):
        self.root = Tk()
        self.root.title("Vier op een rij: Server")  # title of window
        self.serverframe = ttk.Frame(self.root, padding="80 80 80 80")  # padding of frame
        self.serverframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        self.serverframe.columnconfigure(0, weight=1)
        self.serverframe.rowconfigure(0, weight=1)
        ttk.Label(self.serverframe, text="Running the server...").grid(column=2, row=1, sticky=(W, E))
        ttk.Button(self.serverframe, text="Host server").grid(column=3, row=6, sticky=(W, E))
        ### server has to be started here
        import vieropeenrijserver
        self.hosting = vieropeenrijserver.vieropeenrijServer(localaddr=(socket[0], int(socket[1])))
        print("hosting the server")

    def update(self):
        self.root.update()
        sleep(0.01)
        self.hosting.Pump()
        self.hosting.tick()
        ### server has to be updated here
        # self.hosting.pump()
        # sleep(0.001)

# hostS = screenServer()
# while 1:
#     hostS.update()

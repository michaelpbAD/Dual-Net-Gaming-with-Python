from tkinter import *
from tkinter import ttk
from time import sleep


class screenServer():
    import vieropeenrijServer
    def __init__(self):
        root = Tk()
        root.title("Vier op een rij: Server")  # title of window
        serverframe = ttk.Frame(root, padding="80 80 80 80")  # padding of frame
        serverframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        serverframe.columnconfigure(0, weight=1)
        serverframe.rowconfigure(0, weight=1)
        ttk.Label(serverframe, text="Running the server...").grid(column=2, row=1, sticky=(W, E))
        ttk.Button(serverframe, text="Host server").grid(column=3, row=6, sticky=(W, E))
        ### server has to be started here

        # hosting = vieropeenrijServer.vieropeenrijServer(localaddr=("LOCALHOST", 31425))
        print("hosting the server")

    def update():
        self.root.update()
        print("helo")
        vieropeenrijServer.updateServer()
        ### server has to be updated here
        # self.hosting.pump()
        # sleep(0.001)

# hostS = screenServer()
# while 1:
#     hostS.update()

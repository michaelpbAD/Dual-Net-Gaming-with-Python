from tkinter import *
from tkinter import ttk

class screenServer():
    def __init__(self):
        root = Tk()
        print("host server")
        root.title("Vier op een rij: Server")  # title of window
        serverframe = ttk.Frame(root, padding="80 80 80 80")  # padding of frame
        serverframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        serverframe.columnconfigure(0, weight=1)
        serverframe.rowconfigure(0, weight=1)
        ttk.Label(serverframe, text="Running the server...").grid(column=2, row=1, sticky=(W, E))

    def update():
        self.root.update()

    ### server has to be called here

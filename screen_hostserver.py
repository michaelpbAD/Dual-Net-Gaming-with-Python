""" Form with tkinter: hosting the server """
# import modules
from tkinter import *
from tkinter import ttk
from time import sleep

class screenServer():
    def __init__(self, socket, maxPlayers):
        self.closedWindow = False
        # create window
        self.root = Tk()
        self.root.title("Vier op een rij: Server")
        self.root.resizable(False, False)
        # make frame to show widgets in
        self.serverframe = ttk.Frame(self.root, padding="80 80 80 80")
        self.serverframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.serverframe.columnconfigure(0, weight=1)
        self.serverframe.rowconfigure(0, weight=1)
        ttk.Label(self.serverframe, text="Running the server...").grid(column=2, row=1, sticky=(W, E))
        # import vieropeenrijserver
        import vieropeenrijserver
        # make object from server class with arguments maxPlayers and socket = localaddr
        self.hosting = vieropeenrijserver.vieropeenrijServer(maxPlayers, localaddr=(socket[0], int(socket[1])))
        # protocol handler for checking if window gets closed by clicking (WM_DELETE_WINDOW) and will do function on_closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # ask the user if he wants to quit?
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # start.py loops until closedWindow = True
            self.closedWindow = True
            # close the window
            self.root.destroy()

    def update(self):
        # update window
        self.root.update()
        # check for sockets / data / buffers
        self.hosting.Pump()
        sleep(0.01)
        self.hosting.tick()

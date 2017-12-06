""" Form with tkinter: join host or host server """
# import modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re


class joinorhost():
    def __init__(self):
        self.closedWindow = False
        self.hostS = None
        self.playVierOpEenRij = None
        # ============================ START FORM JOIN OR HOST SERVER =================================
        # make a window
        self.root = Tk()
        # title of window
        self.root.title("Vier op een rij: Client or Server")
        self.root.resizable(False, False)

        # making new derived styles
        s = ttk.Style()
        print(s.lookup('TFrame', 'background'))
        s.configure('vieropeenrij.TFrame', background='#1ABC9C')
        s.configure('vieropeenrij.TLabel', background='#1ABC9C')

        # frame is part of window (for showing form elements)
        mainframe = ttk.Frame(self.root, padding="80 80 80 80", style="vieropeenrij.TFrame")  # padding of frame
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        print(mainframe['style'])
        print(mainframe.winfo_class())
        print(s.layout('TButton'))
        print(s.element_options("Button.Border"))

        # tkinter variables for entries, spinbox
        self.socket = StringVar()
        self.nickname = StringVar()
        self.socketServer = StringVar()
        self.maxPlayers = StringVar()

        # label for text entry
        ttk.Label(mainframe, text="Server IP-adress: Server port", style="vieropeenrij.TLabel").grid(column=2, row=1,
                                                                                                     sticky=(W, E))
        # text entry for "socket" server to joing
        socketEntry = ttk.Entry(mainframe, width=20, textvariable=self.socket)
        socketEntry.grid(column=3, row=1, sticky=(N, W, E, S))
        # label for nickname
        ttk.Label(mainframe, text="Nickname:", style="vieropeenrij.TLabel").grid(column=2, row=2, sticky=(W, E))
        # text entry for nickname
        nicknameEntry = ttk.Entry(mainframe, width=20, textvariable=self.nickname)
        nicknameEntry.grid(column=3, row=2, sticky=(N, W, E, S))
        # button for function joinServer
        ttk.Button(mainframe, text="Join server", command=self.joinServer).grid(column=3, row=3, sticky=(W, E))

        # "or"-label
        ttk.Label(mainframe, text="OR", style="vieropeenrij.TLabel").grid(column=2, row=4, sticky=(W, E))

        # label for text entry server ip and port
        ttk.Label(mainframe, text="Your PC's IP-adress: Server port", style="vieropeenrij.TLabel").grid(column=2, row=5,
                                                                                                        sticky=(W, E))
        # entry for "socketServer"
        serverEntry = ttk.Entry(mainframe, width=15, textvariable=self.socketServer)
        serverEntry.grid(column=3, row=5, sticky=(N, W, E, S))
        # label for maximum number of players in a game
        ttk.Label(mainframe, text="Maximum number of players in a game:", style="vieropeenrij.TLabel").grid(column=2,
                                                                                                            row=6,
                                                                                                            sticky=(
                                                                                                            W, E))
        # spinbox for "maxplayers"
        Spinbox(mainframe, from_=2, to=4, textvariable=self.maxPlayers, width=3).grid(column=3, row=6, sticky=(W))
        # button for hosting the server, function hostServer
        ttk.Button(mainframe, text="Host server", command=self.hostServer).grid(column=3, row=7, sticky=(W, E))

        # loop through all child of the frame and add padding to x and y
        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # focus on text entry "socketEntry" when started
        socketEntry.focus()
        # ============================ END FORM JOIN OR HOST SERVER ===================================
        # protocol handler (interaction between application and window manager) for checking if window gets closed (WM_DELETE_WINDOW) and will do function on_closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def joinServer(self):
        # get socket out of text entry and check if it is valid
        checkedSocket = self.checkSocket(self.socket.get())
        # get nickname out of text entry
        nickname = self.nickname.get().strip()
        # check can't be false and nickname can't be empty
        if not (checkedSocket and nickname != ""):
            messagebox.showerror("Error", "No empty nickname allowed.")
            return False
        else:
            # close the window
            self.root.destroy()
            # import VierOpEenRij.py
            import VierOpEenRij
            print("Joining server at: " + checkedSocket[0] + " : " + checkedSocket[1] + " as " + nickname)
            # join server by making an object from VierOpEenRijGame with arguments: checkedSocket and nickname
            self.playVierOpEenRij = VierOpEenRij.VierOpEenRijGame(checkedSocket, nickname)

    def hostServer(self):
        # get socket out of text entry and check if it is valid
        checkedSocket = self.checkSocket(self.socketServer.get())
        # try saving maxPlayers as an int
        try:
            maxPlayers = int(self.maxPlayers.get())
        except:
            maxPlayers = 0
        # checkedSocket can't be false and maxPlayers must be 2,3 or 4
        if checkedSocket and (maxPlayers == 2 or maxPlayers == 3 or maxPlayers == 4):
            # close the window
            self.root.destroy()
            # import screen_server.py
            import screen_hostserver
            print("Hosting server at: " + checkedSocket[0] + " : " + checkedSocket[
                1] + " with maximum players in a game " + str(maxPlayers))
            # hosting the server with arguments: checkedSocket, maxPlayers
            self.hostS = screen_hostserver.screenServer(checkedSocket, maxPlayers)
        else:
            messagebox.showerror("Error", "Maximum players is 2, 3 or 4.")
            return False

    # check if socket entered is valid
    def checkSocket(self, socket):
        try:
            # split socket if possible
            isIp, isPort = socket.split(":")
        except:
            messagebox.showerror("Error", "Format is IP:Port")
            return False

        # lenth of IP adress may not be smaller than 7 or higher than 15
        if len(isIp) < 7 or len(isIp) > 15:
            messagebox.showerror("Error", "This can not be a valid IP address.")
            return False
        else:
            # check if pattern of IP is valid (3 dots with groups of 1 to 3 digits
            patIp = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            matchIp = patIp.search(isIp)
            if matchIp == None or matchIp.group() != isIp:
                messagebox.showerror("Error", "This can not be a valid IP address.")
                return False
        try:
            # check if port is negative
            if int(isPort) != abs(int(isPort)):
                messagebox.showerror("Error", "Not a valid port number.")
                return False
        except:
            messagebox.showerror("Error", "Not a valid port number.")
            return False
        # return the socket
        return [isIp, isPort]

    def on_closing(self):
        # ask the user if he wants to quit?
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # start.py loops until closedWindow = True
            self.closedWindow = True
            # close the window
            self.root.destroy()

    # update GUI 1 time
    def update(self):
        try:
            self.root.update()
        except:
            pass
        # only update when object exists
        if self.hostS != None:
            if self.hostS.closedWindow == False:
                self.hostS.update()
            else:
                self.closedWindow = True
        # only update when object exists
        if self.playVierOpEenRij != None:
            self.playVierOpEenRij.update()

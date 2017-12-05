""" Form with tkinter: join host and/or host server """
# import modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
import screen_hostserver

# checking IP adress
class joinorhost():
    def __init__(self):
        # =============================== START FORM JOIN OR HOST =========================================
        # root =
        self.root = Tk()
        # title of window
        self.root.title("Vier op een rij: Client or Server")
        self.hostS = None
        self.playVierOpEenRij = None

        mainframe = ttk.Frame(self.root, padding="80 80 80 80")  # padding of frame
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        # tkinter variables for entries (input field)
        self.socket = StringVar()
        self.nickname = StringVar()
        self.socketServer = StringVar()
        self.maxPlayers = StringVar()
        # label for input field
        ttk.Label(mainframe, text="Server IP-adress: Server port").grid(column=2, row=1, sticky=(W, E))
        # text input ipaddress
        socketEntry = ttk.Entry(mainframe, width=20, textvariable=self.socket)
        socketEntry.grid(column=3, row=1, sticky=(N, W, E, S))  # layout text input field ipaddress
        ttk.Label(mainframe, text="Nickname:").grid(column=2, row=2, sticky=(W, E))
        nicknameEntry = ttk.Entry(mainframe, width=20, textvariable=self.nickname)
        nicknameEntry.grid(column=3, row=2, sticky=(N, W, E, S))  # layout text input nickname ipaddress
        ttk.Button(mainframe, text="Join server", command=self.joinServer).grid(column=3, row=3, sticky=(W, E))

        # "or"-label
        ttk.Label(mainframe, text="OR").grid(column=2, row=4, sticky=(W, E))

        # label for input field host server
        ttk.Label(mainframe, text="Your PC's IP-adress: Server port").grid(column=2, row=5, sticky=(W, E))
        serverEntry = ttk.Entry(mainframe, width=15, textvariable=self.socketServer)
        serverEntry.grid(column=3, row=5, sticky=(N, W, E, S))
        # spinbox for choosing maximum number of players

        ttk.Label(mainframe, text="Maximum players in a game:").grid(column=2, row=6, sticky=(W, E))
        Spinbox(mainframe, from_=2, to=4, textvariable=self.maxPlayers).grid(column=3, row=6, sticky=(W, E))
        # button for hosting the server
        ttk.Button(mainframe, text="Host server", command=self.hostServer).grid(column=3, row=7, sticky=(W, E))
        # loop through all child of the frame and add padding to x and y
        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)
        # focus on ip text field when started
        socketEntry.focus()
        # =============================== END FORM JOIN OR HOST =========================================

    def joinServer(self):
        check = self.checkSocket(self.socket.get())
        nickname = self.nickname.get().strip()
        print('"'+nickname +'"')
        if not(check and nickname != ""):
            messagebox.showerror("Error","Spatienaam mag niet.")
            return False
        else:
            #join server vieropeenrij game
            self.root.destroy()
            print("Joining server at: "+check[0]+" , "+check[1] +" as "+nickname)
            import VierOpEenRij
            self.playVierOpEenRij = VierOpEenRij.VierOpEenRijGame(check, nickname)


    def hostServer(self):
        check = self.checkSocket(self.socketServer.get())
        try:
            maxPlayers = int(self.maxPlayers.get())
        except:
            maxPlayers = 0
        if check and (maxPlayers == 2 or maxPlayers == 3 or maxPlayers == 4):
            # hosting the server
            print("Hosting server at: ", check)
            self.hostS = screen_hostserver.screenServer(check, maxPlayers)
            self.root.destroy()
        else:
            messagebox.showerror("Error","Maximum players is 2, 3 or 4.")
            return False

    def checkSocket(self, socket):
        try:
            isIp, isPort = socket.split(":")
        except:
            messagebox.showerror("Error","Format is IP:Port")
            return False
        if len(isIp) < 8 or len(isIp) > 15:
            messagebox.showerror("Error","This is not an IP address.")
            return False
        else:
            patIp = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            matchIp = patIp.search(isIp)
            if matchIp == None or matchIp.group() != isIp:
                messagebox.showerror("Error","This is not a right IP-address.")
                return False
        try:
            # negatief getal wordt omgzet naar abs
            if int(isPort) != abs(int(isPort)):
                messagebox.showerror("Error","Not a valid port.")
                return False
        except:
            messagebox.showerror("Error","Not a valid port.")
            return False

        return [isIp, isPort]

    # update GUI 1 time
    def update(self):
        try:
            self.root.update()
        except:
            pass
        if self.hostS != None:
            self.hostS.update()
        if self.playVierOpEenRij != None:
            self.playVierOpEenRij.update()

# # TESTING PURPOSES
# joh = joinorhost()
# while 1:
#     joh.update()

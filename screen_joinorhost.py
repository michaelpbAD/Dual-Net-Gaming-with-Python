""" Form with tkinter: join host and/or host server """
# import modules
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
#import screen_hostserver

# checking IP adress
class joinorhost():
    def __init__(self):
        # =============================== START FORM JOIN OR HOST =========================================
        # root =
        self.root = Tk()
        self.root.title("Vier op een rij: Client or Server")  # title of window
        self.screenServe = None
        mainframe = ttk.Frame(self.root, padding="80 80 80 80")  # padding of frame
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        # tkinter variables for entries (input field)
        self.socket = StringVar()
        self.nickname = StringVar()
        self.socketServer = StringVar()
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
        # button for hosting the server
        ttk.Button(mainframe, text="Host server", command=self.hostServer).grid(column=3, row=6, sticky=(W, E))
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
            #join server
            print("Joining server at: "+check[0]+" , "+check[1] +" as "+nickname)


    def hostServer(self):
        check = self.checkSocket(self.socketServer.get())
        if check:
            print("Hosting server at: ", check)
            #self.screenServe = screen_hostserver.screenServer()
            # vieropeenrij game server
        else:
            return False

    def checkSocket(self, socket):
        try:
            isIp, isPort = socket.split(":")
        except:
            messagebox.showerror("Error","Format is IP:Port")
            return False
        #print(isIp + " : " + str(len(isIp)))
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

        #print(matchIp.group())
        #print(self.socket.get())
        return [isIp, isPort]

    # update GUI 1 time
    def update(self):
        self.root.update()


# TESTING PURPOSES
joh = joinorhost()
while 1:
    joh.update()
    if joh.screenServe != None:
        screenServe.update()
        print("Hello")

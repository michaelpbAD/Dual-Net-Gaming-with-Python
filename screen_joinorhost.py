""" Form with tkinter: nickname, server selection """
# import tkinter / ttk for GUI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re

# checking IP adress
class joinorhost():
    def __init__(self):
        # =============================== START FORM JOIN OR HOST =========================================
        # root =
        self.root = Tk()
        self.root.title("Vier op een rij: Client or Server")  # title of window
        mainframe = ttk.Frame(self.root, padding="80 80 80 80")  # padding of frame
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        # tkinter variables for entries (input field)
        self.socket = StringVar()
        self.nickname = StringVar()
        # label for input field
        ttk.Label(mainframe, text="Server IP-adress: Server port").grid(column=2, row=1, sticky=(W, E))
        # text input ipaddress
        socketEntry = ttk.Entry(mainframe, width=20, textvariable=self.socket)
        socketEntry.grid(column=2, row=2, sticky=(N, W, E, S))  # layout text input field ipaddress
        ttk.Label(mainframe, text="Nickname:").grid(column=1, row=3, sticky=(W, E))
        nicknameEntry = ttk.Entry(mainframe, width=20, textvariable=self.nickname)
        nicknameEntry.grid(column=2, row=3, sticky=(N, W, E, S))  # layout text input nickname ipaddress

        ttk.Button(mainframe, text="Join server", command=self.joinServer).grid(column=2, row=4, sticky=(W, E))
        # "or"-label
        ttk.Label(mainframe, text="or").grid(column=2, row=5, sticky=(W, E))
        # button for hosting the server
        ttk.Button(mainframe, text="Host server", command=self.hostServer).grid(column=2, row=6, sticky=(W, E))
        # loop through all child of the frame and add padding to x and y
        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)
        # focus on ip text field when started
        socketEntry.focus()

        # =============================== END FORM JOIN OR HOST =========================================
    def checkSocket(self):
        try:
            isIp, isPort = self.socket.get().split(":")
        except:
            messagebox.showerror("Error","Format is IP:Port")
            return False
        #print(isIp + " : " + str(len(isIp)))
        if len(isIp) < 8 or len(isIp) > 15:
            messagebox.showerror("This is not an IP address.")  # need to generate error
            return False
        else:
            patIp = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
            matchIp = patIp.search(isIp)
            if matchIp == None or matchIp.group() != isIp:
                messagebox.showerror("This is not a right address")
                return False

        try:
            # negatief getal wordt omgzet naar abs
            isPort = abs(int(isPort))
            print(isPort)
        except:
            messagebox.showerror("Not a valid port.")
            return False

        print(matchIp.group())
        print(self.socket.get())
        return [isIp, isPort]

    def joinServer(self):
        check = self.checkSocket()
        if check:
            print("Joining server: ", check)
        else:
            return False

    def hostServer(self):
        print("Hosting server")


    # update GUI 1 time
    def update(self):
        self.root.update()

##hello = joinorhost()
#hello.update()
joh = joinorhost()
while 1:
    joh.update()

""" Form with tkinter: nickname, server selection """
# import tkinter / ttk for GUI
from tkinter import *
from tkinter import ttk

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
        # tkinter variable for entry (input field)
        self.ip = StringVar()
        # label for input field
        ttk.Label(mainframe, text="Server IP-adress:").grid(column=2, row=1, sticky=(W, E))
        # text input ipaddress
        ip_entry = ttk.Entry(mainframe, width=20, textvariable=self.ip)
        ip_entry.grid(column=2, row=2, sticky=(N, W, E, S))  # layout text input field ipaddress
        ttk.Button(mainframe, text="Join server", command=self.getIp).grid(column=2, row=3, sticky=(W, E))
        # "or"-label
        ttk.Label(mainframe, text="or").grid(column=2, row=4, sticky=(W, E))
        # button for hosting the server
        ttk.Button(mainframe, text="Host server", command=self.hostServer).grid(column=2, row=5, sticky=(W, E))
        # loop through all child of the frame and add padding to x and y
        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)
        # focus on ip text field when started
        ip_entry.focus()

        # =============================== END FORM JOIN OR HOST =========================================

    def getIp(self):
        return self.ip.get()

    def hostServer(self):
        print("host")

    # update GUI 1 time
    def update(self):
        self.root.update()

##hello = joinorhost()
#hello.update()

""" Form with tkinter: nickname, server selection """
# import tkinter / ttk for GUI
from tkinter import *
from tkinter import ttk
# import regex to search for IP adress
import re
import pygame
from VierOpEenRij import *

gstart=False
# checking IP adress

def checkIp(*args):
    isIp = ip.get()
    print(isIp + " : " + str(len(isIp)))
    if len(isIp) < 8 or len(isIp) > 15:
        print("This is not an IP address.")  # need to generate error
    else:
        patIp = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        matchIp = patIp.search(isIp)
        if matchIp == None or matchIp.group() != isIp:
            print("This is not a right address")
        else:
            print(matchIp.group())
            print("join server")
            # exec(open("./VierOpEenRij.py").read())  # experimental, not the right way

            global bg
            bg=VierOpEenRijGame()  # init__ is called right here
            global gstart
            gstart=True

# checking if server can be hosted
def hostServer(*args):
    server = Tk()
    print("host server")
    server.title("Vier op een rij: Server")  # title of window
    serverframe = ttk.Frame(server, padding="80 80 80 80")  # padding of frame
    serverframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
    serverframe.columnconfigure(0, weight=1)
    serverframe.rowconfigure(0, weight=1)
    ttk.Label(serverframe, text="Running the server....").grid(column=2, row=1, sticky=(W, E))


# root =
root = Tk()
root.title("Vier op een rij: Client or Server")  # title of window
mainframe = ttk.Frame(root, padding="80 80 80 80")  # padding of frame
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # grid layout
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# tkinter variable for entry (input field)
ip = StringVar()

# label for input field
ttk.Label(mainframe, text="Server IP-adress:").grid(column=2, row=1, sticky=(W, E))
# text input ipaddress
ip_entry = ttk.Entry(mainframe, width=20, textvariable=ip)
ip_entry.grid(column=2, row=2, sticky=(N, W, E, S))  # layout text input field ipaddress
ttk.Button(mainframe, text="Join server", command=checkIp).grid(column=2, row=3, sticky=(W, E))

# "or"-label
ttk.Label(mainframe, text="or").grid(column=2, row=4, sticky=(W, E))

# button for hosting the server
ttk.Button(mainframe, text="Host server", command=hostServer).grid(column=2, row=5, sticky=(W, E))

# loop through all child of the frame and add padding to x and y
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# focus on ip text field when started
ip_entry.focus()

# loop for GUI
while 1:
    root.update()
    if gstart==True:
        bg.update()

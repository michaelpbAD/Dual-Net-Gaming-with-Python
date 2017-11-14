""" Form with tkinter: nickname, server selection """
from tkinter import *
from tkinter import ttk
def checkIP(*args):
    print("join server")
def hostServer(*args):
    print("host server")

root = Tk()
root.title("Vier op een rij: Client or Server")
mainframe = ttk.Frame(root, padding="80 80 80 80")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

IP = StringVar()

IP_entry = ttk.Entry(mainframe, width=20, textvariable=IP)
IP_entry.grid(column=2, row=2, sticky=(N, W, E, S))
ttk.Label(mainframe, text="Server IP-adress:").grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Join server", command=checkIP).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="or").grid(column=2, row=4, sticky=(W, E))
ttk.Button(mainframe, text="Host server", command=hostServer).grid(column=2, row=5, sticky=(W, E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)
IP_entry.focus()

root.mainloop()

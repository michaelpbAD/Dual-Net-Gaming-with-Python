""" This python script starts all other scripts. """
""" Form with tkinter: nickname, server selection """
# import tkinter / ttk for GUI
from tkinter import *
from tkinter import ttk
import screen_joinorhost

start = screen_joinorhost.joinorhost()
while 1:
    #checkIp(joinhost.getIp())
    start.update()

""" This python script starts all other scripts. """
""" Form with tkinter: nickname, server selection """
# import tkinter / ttk for GUI
from tkinter import *
from tkinter import ttk
# import regex to search for IP adress
from time import sleep
import screen_joinorhost

# def checkIp(checkIp):
#
#     print(checkIp + " : " + str(len(checkIp)))
#     if len(checkIp) < 8 or len(checkIp) > 15:
#         print("This is not an IP address.")  # need to generate error
#     else:
#         patIp = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
#         matchIp = patIp.search(checkIp)
#         if matchIp == None or matchIp.group() != checkIp:
#             print("This is not a right address")
#         else:
#             print(matchIp.group())
#             print("join server")



start = screen_joinorhost.joinorhost()
while 1:
    #checkIp(joinhost.getIp())
    start.update()
# """
# gstart=False
# sstart = False
# # checking IP adress
#
# def checkIp(*args):
#     isIp = ip.get()
#     print(isIp + " : " + str(len(isIp)))
#     if len(isIp) < 8 or len(isIp) > 15:
#         print("This is not an IP address.")  # need to generate error
#     else:
#         patIp = re.compile(r'\d{2,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
#         matchIp = patIp.search(isIp)
#         if matchIp == None or matchIp.group() != isIp:
#             print("This is not a right address")
#         else:
#             print(matchIp.group())
#             print("join server")
#
#             # exec(open("./VierOpEenRij.py").read())  # experimental, not the right way
#             #global bg
#             #bg=VierOpEenRijGame()  # init__ is called right here
#             global gstart
#             gstart=True
#
# # checking if server can be hosted
# def hostServer(*args):
#     global sstart
#     sstart = True
#     print("host server")
#     # print IP lol
#     """"""print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])"""
#     """ print IP adress
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     print(s.getsockname()[0])
#     s.close()"""

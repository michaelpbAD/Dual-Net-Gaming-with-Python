""" This python script starts screen_joinorhost.py (object) """
# import screen_joinorhost.py
import screen_joinorhost

# make object to initialize the window for joining or hosting a server
start = screen_joinorhost.joinorhost()
# keep updating object
while not start.closedWindow:
    start.update()

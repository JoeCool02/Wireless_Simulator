"""
File Name: cursesuser.py
Author: Joe Peterson

Purpose:  Convenient way to display information on the command line.

Usage:

from cursesuser import *
cinstance = CursesUser()
cinstance.write('Hello, World!')
cinstance.shutdown()

"""
import curses as C

class CursesUser:
    def __init__(self):
        self.stdscr = C.initscr()  #Initialize the screen (clear it)
        C.noecho()  #Do not echo user keystrokes
        C.cbreak()  #React to keys immediately, without waiting for an enter or return
        self.stdscr.keypad(1)  #Allow curses to handle special keys (up, down, esc, etc.)
    def shutdown(self):
        #Reverses everything done in __init__
        C.nocbreak()
        self.stdscr.keypad(0)
        C.echo()
        print "Curses Shutdown"
    def write(self, string, x = 0, y = 0):        
        #Writes a string to a standard place on the screen, refreshes
        self.stdscr.addstr(y, x, string)      
        self.stdscr.refresh()
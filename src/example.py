"""
A simple example of hooking the keyboard on Linux using pyxhook

Any key pressed prints out the keys values, program terminates when spacebar
is pressed.
"""
from __future__ import print_function

# Libraries we need
import pyxhook
import time

serial_no = []

# This function is called every time a key is presssed
def kbevent(event):
    global running
    global serial_no
    # print key info
    serial_no.append(event.Key)

    # If the ascii value matches spacebar, terminate the while loop
    if event.Ascii == 13:
        running = False

def mainhook():
    global running
    global serial_no
    ctr = 0 
    
    # Create hookmanager
    hookman = pyxhook.HookManager()
    # Define our callback to fire when a key is pressed down
    hookman.KeyDown = kbevent
    # Hook the keyboard
    hookman.HookKeyboard()
    # Start our listener
    hookman.start()

    # Create a loop to keep the application running
    running = True
    while running:
        time.sleep(0.1)
        ctr += 1
        if ctr >= 20:
            running = False

    # Close the listener when we are done
    hookman.cancel()
    print(serial_no)

mainhook()

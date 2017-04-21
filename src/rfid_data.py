
import pyxhook
import time
import datetime
from vars import *

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
    return serial_no

#TODO print to file and send to DB functions (DB dummy)

def rfid_check(rfid_raw):
    if len(rfid_raw)==11 and rfid_raw[-1]=="Return":
        return True
    else:
        return False

def parse(rfid_raw):

    global running

    if rfid_check(rfid_raw):

        data_list = []

        rfid_raw.pop()
        rfid_raw = ''.join(rfid_raw)
        data_list.append(rfid_raw)
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        data_list.append(timestamp)
        return data_list
    else:
        running = False
        #exit()

def write_to_file(rfid_parsed):
    f = open('data.log', 'a+')

    f.write("%s; %s; %s;\n" % (rfid_parsed[RFID_TSTAMP],RFID_READER,rfid_parsed[RFID_SERIALNO]))

    f.close()

def commit_data(rfid_parsed):
    write_to_file(rfid_parsed)
    #send_to_db(rfid_parsed)

def test_commit():
    try:
        result = parse(mainhook())
        commit_data(result)
        return result
    except:
        exit()

if __name__=="__main__":

    test_serial = ["1","2","3","4","5","6","7","8","9","0","0","Return"]

    test_commit()


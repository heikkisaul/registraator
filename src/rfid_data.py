
import pyxhook
import pymysql
import time
import datetime
from vars import *

serial_no = []
prev_result = None

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
    serial_no = []

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

    return serial_no

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
        timestamp = datetime.datetime.now()
        str_timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(timestamp)
        data_list.append(str_timestamp)
        return (data_list, timestamp)
    else:
        running = False
        return (None,None)

def write_to_file(rfid_parsed):
    f = open('data.log', 'a+')

    try:
        f.write("%s; %s; %s;\n" % (rfid_parsed[RFID_TSTAMP],RFID_READER,rfid_parsed[RFID_SERIALNO]))
        f.close()
    except:
        f.close()

def send_to_db(rfid_parsed, ts, lect_id):

    conn = pymysql.connect(host='127.0.0.1', port=9990, user=DB_USR, passwd=DB_PWD,
                           db=DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute("CALL `lect_reg_base`.`INSERT_LECTURE_VISIT_RFID`(" + str(rfid_parsed[RFID_SERIALNO]) + ", " + str(lect_id) + ", \'" + str(ts) + "\')")

        conn.commit()
        print(cur.description)

        cur.close()
        conn.close()
    except:
        print("error")
        cur.close()
        conn.close()


def commit_data(rfid_parsed, ts, lect_id):
    write_to_file(rfid_parsed)
    send_to_db(rfid_parsed, ts, lect_id)


def test_commit(lect_id):

    result,ts = parse(mainhook())
    commit_data(result, ts, lect_id)
    return result

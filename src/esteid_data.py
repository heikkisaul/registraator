# -*- coding: utf-8 -*-

#import sys
import subprocess
import datetime
#import pymysql
from vars import *
import os
import signal
g_data_list=[]

#reload(sys)
#sys.setdefaultencoding('utf-8')


# After being called, waits for card insertion. When a proper card is inserted, reads the data on the card chip
def get_data(reader = '0'):
    call_eidenv = subprocess.Popen(['eidenv', reader, '-w'],stdout=subprocess.PIPE)#,stderr=subprocess.STDOUT)
    call_eidenv.wait()
    eidenv_raw = call_eidenv.communicate()[0]
    #call_eidenv.kill()
    return eidenv_raw.decode('latin-1')

# Parses raw data from get_eid_data() into a list [surname,first name,ID code]
def parse(eidenv_raw):

    global g_data_list

    data_list = []

    for i in [0,1,2,6]:
        raw_line = eidenv_raw.splitlines()[i].split(': ')[1].strip()
        data_list.append(raw_line)
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data_list.append(timestamp)
    return data_list

def commit_data(eidenv_parsed):
    write_to_file(eidenv_parsed)
    #send_to_db(eidenv_parsed)

def send_to_db(eidenv_parsed):
    db = pymysql.connect(DB_ADDR, DB_USR, DB_PWD, DB_NAME)

    cursor = db.cursor()

    cursor.execute("INSERT INTO STUDENTS(FIRST_NAME, LAST_NAME, ID_CODE) VALUES ("+eidenv_parsed[0]+", "+eidenv_parsed[1]+", "+eidenv_parsed[2]+")")
    db.commit()

    db.close()

def write_to_file(eidenv_parsed):
    f = open('data.log', 'a+')

    f.write("%s; %s; %s; %s; %s; %s\n" % (eidenv_parsed[EID_TSTAMP],SC_READER,eidenv_parsed[EID_IDCODE],eidenv_parsed[EID_SNAME],eidenv_parsed[EID_FNAME],eidenv_parsed[EID_MNAME]))

    f.close()

def test_commit():
    result = parse(get_data())
    commit_data(result)
    print(result)

if __name__ == "__main__":

    #print(parse(get_data()))
    commit_data(parse(get_data()))





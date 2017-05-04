# -*- coding: utf-8 -*-

#import sys
import subprocess
import datetime
import pymysql
from vars import *
import os
import signal
g_data_list=[]


#reload(sys)
#sys.setdefaultencoding('utf-8')


# After being called, waits for card insertion. When a proper card is inserted, reads the data on the card chip
def get_data(reader = '0'):
    call_eidenv = subprocess.Popen(['eidenv', reader, '-w'],stdout=subprocess.PIPE)#,stderr=subprocess.STDOUT)
    #call_eidenv.wait()
    try:
        eidenv_raw = call_eidenv.communicate(timeout=5)[0]
        return eidenv_raw.decode('latin-1')
    except:
        call_eidenv.kill()


# Parses raw data from get_eid_data() into a list [surname,first name,ID code]
def sc_parse(eidenv_raw):

    global g_data_list

    data_list = []

    for i in [0,1,2,6]:
        raw_line = eidenv_raw.splitlines()[i].split(': ')[1].strip()
        data_list.append(raw_line)
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data_list.append(timestamp)
    return (data_list, timestamp)

def sc_commit_data(eidenv_parsed, ts, lect_id):
    sc_write_to_file(eidenv_parsed)
    sc_send_to_db(eidenv_parsed, ts, lect_id)
    # print(eidenv_parsed, ts, lect_id)

def sc_send_to_db(eidenv_parsed, ts, lect_id):

    conn = pymysql.connect(host='127.0.0.1', port=9990, user=DB_USR, passwd=DB_PWD,
                           db=DB_NAME)
    cur = conn.cursor()



    cur.execute("INSERT INTO LECTURE_VISIT (ID_CODE, LECTURE_ID, REG_TIMESTAMP) VALUES ("+str(eidenv_parsed[3])+", "+str(lect_id)+", \'"+str(ts)+"\')")
    conn.commit()
    print(cur.description)

    cur.close()
    conn.close()


def sc_write_to_file(eidenv_parsed):
    f = open('data.log', 'a+')

    f.write("%s; %s; %s; %s; %s\n" % (eidenv_parsed[EID_TSTAMP],SC_READER,eidenv_parsed[EID_IDCODE],eidenv_parsed[EID_FNAME],eidenv_parsed[EID_SNAME]))

    f.close()

def sc_test_commit(lect_id):
    try:
        result, ts = sc_parse(get_data())
        sc_commit_data(result, ts, lect_id)
        return result
    except:
        return None

if __name__ == "__main__":

    #print(parse(get_data()))
    sc_commit_data(sc_parse(get_data()))





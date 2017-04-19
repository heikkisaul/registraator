from multiprocessing import Process
import esteid_data as ed
import rfid_data as rd
import os
import sys

p2 = Process(target=ed.test_commit)
p3 = Process(target=rd.test_commit)

try:
    p2.start()
    p3.start()
    os.execv(sys.executable,['python3'] + sys.argv)

except:
    os.execv(sys.executable, ['python3'] + sys.argv)


    
##try:
##    ed.test_commit()
##    rd.test_commit()
##
##    os.execv(sys.executable, ['python3'] + sys.argv)
##    exit()
##except:
##    os.execv(sys.executable,['python3'] + sys.argv)
##    exit()





from multiprocessing import Process
import esteid_data as ed
import example as rd
import os
import sys

p2 = Process(target=ed.test_commit)
p3 = Process(target=rd.mainhook)

try:
    p2.start()
    p3.start()
    os.execv(sys.executable,['python3'] + sys.argv)
except:
    os.execv(sys.executable, ['python3'] + sys.argv)0858860661
    
#try:
    #ed.test_commit()
    #rd.mainhook()

    #os.execv(sys.executable, ['python3'] + sys.argv)
    #exit()
#except:
    #os.execv(sys.executable,['python3'] + sys.argv)
    #exit()





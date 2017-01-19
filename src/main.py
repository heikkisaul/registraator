from multiprocessing import Process
import eid_data_reader as ed

def rfid_placeholder(code):

    print(code)

p1 = Process(target=rfid_placeholder,args=("11111151515",))
#pool.apply(ed.commit_data(ed.parse(ed.get_data())))
p2 = Process(target=ed.test_commit)
p3 = Process(target=rfid_placeholder,args=("22551515",))

p1.start()
p2.start()
p3.start()


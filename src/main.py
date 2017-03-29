from multiprocessing import Process
import esteid_data as ed
import rfid_data as rd

def rfid_placeholder(code):

    print(code)


p1 = Process(target=rfid_placeholder,args=("11111151515",))
#pool.apply(ed.commit_data(ed.parse(ed.get_data())))
#p2 = Process(target=ed.test_commit)
p3 = Process(target=rd.get_data())
p4 = Process(target=rfid_placeholder,args=("2584484415",))

p1.start()
#p2.start()
p3.start()
p4.start()



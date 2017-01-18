from multiprocessing import Pool
import esteid_data as ed

def rfid_placeholder(code):

    print(code)

pool = Pool(processes=30)

pool.apply(rfid_placeholder,args=("11111151515",))
#pool.apply(ed.commit_data(ed.parse(ed.get_data())))
pool.apply(ed.test_commit)
pool.apply(rfid_placeholder,args=("22551515",))



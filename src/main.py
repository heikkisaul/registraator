import threading

import esteid_data

def rfid_placeholder(code):
    print(code)

eid_t = threading.Thread(name='esteid_thread', target=esteid_data.get_eid_data)
rfid_t = threading.Thread(name='rfid_thread', target=rfid_placeholder,args=("112344456",))

eid_t.start()
rfid_t.start()

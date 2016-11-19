import subprocess
import datetime

# After being called, waits for card insertion. When a proper card is inserted, reads the data on the card chip
def get_eid_data(reader = '0'):
    call_eidenv = subprocess.Popen(['eidenv', reader,'-w'],stdout=subprocess.PIPE)
    call_eidenv.wait()
    eidenv_raw = call_eidenv.communicate()[0]
    return eidenv_raw

# Parses raw data from get_eid_data() into a list [surname,first name,ID code]
def esteid_data_parse(eidenv_raw_out):

    data_list = []

    for i in [0,1,2,6]:
        raw_line = eidenv_raw_out.splitlines()[i].split(': ')[1].strip()
        data_list.append(raw_line)
    timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    data_list.append(timestamp)
    return data_list

print(esteid_data_parse(get_eid_data()))


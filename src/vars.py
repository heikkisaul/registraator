"""
List of variables required by different parts of the program
"""
# Variables for MySQL database
DB_ADDR = "localhost"
DB_USR = "root"
DB_PWD = "Yamato"
DB_NAME = "Mydb"

# Variables for parsed EID data
EID_FNAME = 1
EID_MNAME = 2
EID_SNAME = 0
EID_IDCODE = 3
EID_TSTAMP = 4

# Variables to identify I/O devices for log
SC_READER = 'SC'
RFID_READER = 'RF'
FPRINT_READER = 'FP'

# Variables to select I/O devices
SC_READER_ID = '0'
RFID_READER_ID = '0'
FPRINT_READER_ID = '0'
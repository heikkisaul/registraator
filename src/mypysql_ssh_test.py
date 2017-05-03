import pymysql

conn = pymysql.connect(host='127.0.0.1', port=9990, user='lrb_admin', passwd='oiurfmneroejf5v9', db='lect_reg_base')

cur=conn.cursor()

cur.execute("SELECT * FROM USER")

print(cur.description)

print()

for row in cur:
    print(row)

cur.close()
conn.close()

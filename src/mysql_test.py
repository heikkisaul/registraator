import pymysql

db = pymysql.connect("localhost", "root", "Yamato", "Mydb")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")
data = cursor.fetchone()

#cursor.execute("INSERT INTO STUDENTS(FIRST_NAME, LAST_NAME, ID_CODE) VALUES ('Henri', 'Saul', 36805300835)")
#db.commit()

print(data)

db.close()
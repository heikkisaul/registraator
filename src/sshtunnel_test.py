from sshtunnel import SSHTunnelForwarder
from time import sleep

server = SSHTunnelForwarder('ims.ut.ee', ssh_username="lectbot", ssh_password="ZUEAxLBr2L", remote_bind_address=('127.0.0.1', 3306), local_bind_address=('127.0.0.1', 9990))

server.start()

print(server.local_bind_port)

while True:
    sleep(1)

server.stop()
print("CLOSED")

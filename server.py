import socket
from threading import Thread

HOST = 'localhost'
PORT = 50000

client = []
messages = []

def protocol(msg):
  print(msg)

def listenner(conn, addr):
  while True:
    data = conn.recv(1024).decode('utf-8')
    if not data: continue
    protocol(data)
    conn.send(b'Recebi!')
  client_socket.close()

s = socket.socket()

s.bind((HOST, PORT))
s.listen(5)

print('Server inicializado na porta: ' + str(PORT))

while True:
  c, addr = s.accept()
  print(f"{addr} Connected!")
  thread = Thread(target=listenner, args=(c, addr))
  thread.start()

c.close()
thread.join()
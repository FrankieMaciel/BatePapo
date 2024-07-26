import socket

HOST = 'localhost'
PORT = 50000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
      text = input()
      s.sendall(bytes(text, 'utf-8'))
      data = s.recv(1024)
      if not data: continue
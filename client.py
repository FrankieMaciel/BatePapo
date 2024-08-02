from threading import Thread
import socket
from texts import drawnSquare

HOST = 'localhost'
PORT = 50000
name = 'user'

def listenner(s):
  while True:
    try:
        message = s.recv(1024)
    except:
        break
    message = message.decode('utf-8')
    parts = message.split(" ")
    if parts[0] == '!msg':
      parts.pop(0)
      userName = parts.pop(0)
      nmsg = " ".join(parts)
      drawnSquare(nmsg, userName)
    elif parts[0] == '!disconected':
      parts.pop(0)
      userName = parts.pop(0)
      nmsg = " ".join(parts)
      drawnSquare(f'{userName} disconectou!')
    else: continue

def sender(s):
  while True:
    text = input()
    print('\033[1A' + '\033[K', end='')
    formatedText = f"!sendmsg {text}"
    s.send(bytes(formatedText, 'utf-8'))
    drawnSquare(text, name)

name = input("Por favor insira seu nome: ")
print('\033[1A' + '\033[K', end='')
nameCommand = f"!nick {name}"

s = socket.create_connection((HOST,PORT))
s.send(bytes(nameCommand, 'utf-8'))

lt = Thread(target=listenner, args=(s,))
st = Thread(target=sender, args=(s,))
lt.start()
st.start()
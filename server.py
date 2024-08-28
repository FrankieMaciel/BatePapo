import socket
import select
from threading import Thread

HOST = 'localhost'
PORT = 5000

clients = []
messages = []

allClients = {}

class Client:
  def __init__(self, name, conn, addr):
    self.name = name
    self.conn = conn
    self.addr = addr
  
  def __eq__(self, other):
        assert isinstance(other, Client)
        return self.addr == other.addr

def createClient(c, addr):
  clientData = c.recv(1024).decode('utf-8')
  parts = clientData.split(' ')

  if parts[0] == '!nick':
    cName = parts[1]
  else:
    c.close()
    return False

  nameList = [c.name for c in clients]
  nListLen = len(nameList)
  strNameList = ' '.join(nameList)
  userListResponse = f"!users {nListLen} {strNameList}"
  c.send(bytes(userListResponse, 'utf-8'))

  nc = Client(cName, c, addr)
  allClients[nc.addr] = nc
  clients.append(nc)
  formatedMsg = f"!join {cName}"
  for c in clients:
    if c.addr == addr: continue
    sendMsg(c, formatedMsg)
  print(f"{nc.name} Connected!")
  return nc

def sendMsg(client, msg):
  try:
    client.conn.send(bytes(msg, 'utf-8'))
  except Exception as e:
    print(e)
    desconectClient(client)

def protocol(msg, client):
  if not msg: return

  parts = msg.split(" ")
  command, userName = parts[0], parts[1]
  message = " ".join(parts[1:])

  if command == '!sendmsg':
    formatedMsg = f"!msg {client.name} {message}"
    if len(clients) <= 1: return
    for c in clients:
      if c.addr == client.addr: continue
      sendMsg(c, formatedMsg)
  if command == '!poke':
    if not allClients.get(userName): return
    formatedMsg = f"!poke {client.name} {userName}"
    if len(clients) <= 1: return
    for c in clients:
      if c.addr == client.addr: continue
      sendMsg(c, formatedMsg)
  if command == '!changenickname':
    newUserName = message.split(" ")[1]
    c = allClients.get(client.addr)
    c.name = newUserName
    formatedMsg = f"!changenickname {userName} {newUserName}"
    if len(clients) <= 1: return
    for c in clients:
      # if c.addr == client.addr: continue
      sendMsg(c, formatedMsg)

def desconectClient(client):
  formatedMsg = f"!left {client.name}"
  for c in clients:
    if c.addr == client.addr: continue
    sendMsg(c, formatedMsg)
  client.conn.close()
  clients.remove(client)
  allClients.pop(client.addr)
  print(f"{client.name} desconectou!")

def listenner(client):
  while True:
    try:
      data = client.conn.recv(1024)
      if data == b"":
        desconectClient(client)
        break
    except:
        desconectClient(client)
        break
    data = data.decode('utf-8')
    protocol(data, client)

if __name__ == "__main__":
  s = socket.socket()

  s.bind((HOST, PORT))
  s.listen(5)

  print('Server inicializado na porta: ' + str(PORT))

  while True:
    c, addr = s.accept()
    client = createClient(c, addr)
    if not client: continue
    thread = Thread(target=listenner, args=(client,))
    thread.start()

  c.close()
  thread.join()
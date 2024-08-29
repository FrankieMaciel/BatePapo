from texts import drawnSquare
from threading import Thread
import random
import socket
import sys
import os

HOST = 'localhost'
PORT = 5000
name = 'user'

usersInChat = {}

class Client:
  def __init__(self, name):
    self.name = name
    self.color = generate_random_color()
  
  def __eq__(self, other):
        assert isinstance(other, Client)
        return self.name == other.name

def generate_random_color():
    r = random.randint(100, 255)
    g = random.randint(100, 255)
    b = random.randint(100, 255)
    return [r, g, b]

def getUsers(numOfUseresAsStr, usersString):
  usersInChat.clear()
  usersList = usersString.split(" ")
  for userName in usersList:
    if userName == '': continue
    nc = Client(userName)
    usersInChat[userName] = nc

def addUser(name):
  nc = Client(name)
  usersInChat[name] = nc

def removeUser(name):
  usersInChat.pop(name)

def changeUserName(oldName, newName):
  if oldName in usersInChat:
    nc = usersInChat.pop(oldName)
    nc.name = newName
    usersInChat[newName] = nc

def getchar():
	ch = ''
	if os.name == 'nt': # how it works on windows
		import msvcrt
		ch = msvcrt.getch()
	else:
		import tty, termios, sys
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	if ord(ch) == 3: quit() # handle ctrl+C
	return ch

def getInput(prefix, suffix):
    input_text = ""
    while True:
        message = f"\r\033[K{prefix} [{len(usersInChat)} users online] | {input_text}{suffix}"
        print(message, end='', flush= True)
        char = getchar()
        if char.strip() == '' and char != ' ': break
        elif char == '\x7f': input_text = input_text[:-1]
        else: input_text += char
    sys.stdout.write("\n")
    return input_text

def commands(s, text):
  global name
  commandParts = text.split(" ")
  if len(commandParts) < 2: return
  if commandParts[0] == '/poke':
    formatedText = f"!poke {commandParts[1]}"
    s.send(bytes(formatedText, 'utf-8'))
  if commandParts[0] == '/changenickname':
    nName = commandParts[1]
    if nName == name: return
    formatedText = f"!changenickname {name} {nName}"
    s.send(bytes(formatedText, 'utf-8'))
    name = nName

def listenner(s):
  while True:
    # try to recive the message
    try: message = s.recv(1024)
    except: break
    # process the message and get params
    message = message.decode('utf-8')
    parts = message.split(" ")
    if len(parts) < 2: continue
    command, userName = parts[0], parts[1]
    nmsg = " ".join(parts[2:])
    
    # all commands
    print('\r\033[K\r', end='')
    if command == '!msg': 
      userClient = usersInChat.get(userName)
      if not userClient: ncolor = [100,100,100]
      else: ncolor = userClient.color
      drawnSquare(nmsg, userName, color = ncolor, pos = 2)
    if command == '!users': getUsers(userName, nmsg)

    if command == '!join':
      addUser(userName)
      drawnSquare(f'{userName} conectou!', color=[100,100,100], pos = 1)
    if command == '!left': 
      removeUser(userName)
      drawnSquare(f'{userName} disconectou!', color=[100,100,100], pos = 1)
    if command == '!poke':
      drawnSquare(f'{userName} deu uma cutucada em {nmsg}', color=[100,100,100], pos = 1)
      pass
    if command == '!changenickname':
      changeUserName(userName, nmsg)
      drawnSquare(f'{userName} trocou seu nick para "{nmsg}"', color=[100,100,100], pos = 1)
      pass

def sender(s):
  while True:
    text = getInput(f"┃ ", " ┃")
    print('\033[1A' + '\033[K', end='')
    if not text: continue
    if text[0] == '/':
      commands(s, text)
      continue
    formatedText = f"!sendmsg {text}"
    s.send(bytes(formatedText, 'utf-8'))
    drawnSquare(text, name)

name = getInput("┃ Enter your name: ", " ┃")
print('\033[1A' + '\033[K', end='')
nameCommand = f"!nick {name}"

s = socket.create_connection((HOST,PORT))
s.send(bytes(nameCommand, 'utf-8'))

lt = Thread(target=listenner, args=(s,))
st = Thread(target=sender, args=(s,))
lt.start()
st.start()
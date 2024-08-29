import os
import math

OFFSETX = 1
OFFSETY = 0
TITLEOFFSET = 1

TOPLEFT = '┏'
TOPRIGHT = '┓'
BOTTOMLEFT = '┗'
BOTTOMRIGTH = '┛'
HORIZONTALLINE = '━'
VERTICALLINE = '┃'

def colored(text, color):
    r = color[0]
    g = color[1]
    b = color[2]
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def getAvaliableSize():
  return os.get_terminal_size().columns

def appendAndCheck(array, item):
  array.append(item)
  return 

def splitWords(text, size):
  parts = []
  lines = text.split('\n')
  maxLength = 0
  for line in lines:
    letters = list(line)
    part = ''
    for letter in letters:
      if (len(part) + 1 > size):
        parts.append(part)
        part = ''
      else:
        part += str(letter)
    if (len(part) > maxLength): 
        maxLength = len(part)
    if len(letters) < 1: continue
    if (len(part) > 0): parts.append(part)
  return parts, maxLength

def squareLogic(x,y, sizeX, sizeY, color):
  if (x == 0):
    if (y == 0): print(colored(TOPLEFT, color), end='')
    elif (y == sizeY): print(colored(BOTTOMLEFT, color), end='')
    else: print(colored(VERTICALLINE, color), end='')
  elif (x == sizeX):
    if (y == 0): print(colored(TOPRIGHT, color), end='')
    elif (y == sizeY): print(colored(BOTTOMRIGTH, color), end='')
    else: print(colored(VERTICALLINE, color), end='')
  elif (y == 0 or y == sizeY):
    print(colored(HORIZONTALLINE, color), end='')
  else:
    print(' ', end='')

def drawnSquare(text, title = None, color = [255,255,255], pos = 0):
  squareOffsetX = (OFFSETX + 1)
  squareOffsetY = (OFFSETY + 1)

  textSpaceLengthX = squareOffsetX * 2
  textSpaceLengthY = squareOffsetY * 2

  maxSize = getAvaliableSize() - textSpaceLengthX
  allText, maxLength = splitWords(text, maxSize)

  if title:
    title = ' ' + str(title) + ' '
    titleSize = len(title)
    if (titleSize > maxLength):
      maxLength = titleSize
    titleMax = len(title)

  sizeY = (textSpaceLengthY + len(allText)) - 1
  sizeX = (textSpaceLengthX + maxLength) - 1

  messageOffset = 0
  if (pos == 1):
    messageOffset = (math.floor(getAvaliableSize() / 2) - math.floor(sizeX / 2)) - 1
  if (pos == 2):
    messageOffset = getAvaliableSize() - sizeX - 1

  for y in range(sizeY + 1):
    print(' ' * messageOffset, end='')
    for x in range(sizeX + 1):
      textIndexX = x - squareOffsetX
      textIndexY = y - squareOffsetY
      
      if title:
        titleIndex = x - TITLEOFFSET - 1
        hasTiteIndex = titleIndex >= 0 and titleIndex < titleMax
        if (hasTiteIndex and y == 0 and title != None):
          print(colored(title[titleIndex], color), end='')
          continue

      if (textIndexX < 0 or  textIndexY < 0): 
        squareLogic(x,y, sizeX, sizeY, color)
        continue

      lineSizeY = len(allText) - 1
      if (textIndexY > lineSizeY):
        squareLogic(x,y, sizeX, sizeY, color)
        continue

      lineSizeX = len(allText[textIndexY]) - 1

      if (textIndexX > lineSizeX): 
        squareLogic(x,y, sizeX, sizeY, color)
        continue
      
      if not title:
        print(colored(allText[textIndexY][textIndexX], color), end='')
      else:
        print(allText[textIndexY][textIndexX], end='')
    print('\r')

if __name__ == "__main__":
  drawnSquare('Mensagem de exemplo.')
  drawnSquare('Bom dia meus amigos', 'Frankie', [250, 200, 100], pos = 2)
  drawnSquare('Fulano de tal, entrou no chat!', color = [100,100,100], pos = 1)
  drawnSquare('Bora de mines :p\nOlá', 'Álvaro Renam', color = [0,150,200], pos = 2)
  drawnSquare(r'''
            _   _
           (.)_(.)
        _ (   _   ) _
       / \/`-----'\/ \
     __\ ( (     ) ) /__
     )   /\ \._./ /\   (
jgs   )_/ /|\   /|\ \_(''', 'Alana', [150, 0, 200])
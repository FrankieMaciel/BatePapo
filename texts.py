import os

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
  words = text.split()
  maxLength = 0
  parts = []
  part = ''
  for word in words:
    partSize = len(part.strip())
    if (partSize + len(word) + 1 > size):
      parts.append(part.strip())
      part = ''
    else:
      part += str(word) + ' '
    partSize = len(part)
    if (partSize > maxLength): 
        maxLength = partSize - 1

  if (partSize > 0): parts.append(part.strip())

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

def drawnSquare(text, title = None, color = [255,255,255]):
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

  for y in range(sizeY + 1):
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
    print()

if __name__ == "__main__":
  drawnSquare('Mensagem de exemplo.')
  drawnSquare('Bom dia meus amigos', 'Frankie', [250, 200, 100])
  drawnSquare('Fulano de tal, entrou no chat!', color = [100,100,100])
  drawnSquare('Bora de mines :p', 'Álvaro Renam', color = [0,150,200])
  drawnSquare('Oxi', 'Alana', [150, 0, 200])
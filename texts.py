import subprocess

OFFSET = 2

TOPLEFT = '┏'
TOPRIGHT = '┓'
BOTTOMLEFT = '┗'
BOTTOMRIGTH = '┛'
HORIZONTALLINE = '━'
VERTICALLINE = '┃'

def getAvaliableSize():
  tput = subprocess.Popen(['tput', 'cols'], stdout=subprocess.PIPE)
  return int(tput.communicate()[0].strip())

def appendAndCheck(array, item):
  array.append(item)
  return 

def splitWords(text, size):
  words = text.split()
  maxLength = 0
  parts = []
  part = ''
  for word in words:
    partSize = len(part)
    if (partSize + len(word) > size):
      parts.append(part)
      part = ''
    else:
      part += str(word) + ' '
    partSize = len(part)
    if (partSize > maxLength): 
        maxLength = partSize

  if (partSize > 0): parts.append(part)

  return parts, maxLength

def squareLogic(x,y, sizeX, sizeY):
  if (x == 0):
    if (y == 0): print(TOPLEFT, end='')
    elif (y == sizeY): print(BOTTOMLEFT, end='')
    else: print(VERTICALLINE, end='')
  elif (x == sizeX):
    if (y == 0): print(TOPRIGHT, end='')
    elif (y == sizeY): print(BOTTOMRIGTH, end='')
    else: print(VERTICALLINE, end='')
  elif (y == 0 or y == sizeY):
    print(HORIZONTALLINE, end='')
  else:
    print(' ', end='')

def drawnSquare(text):
  squareOffset = (OFFSET + 1)
  textSpaceLength = squareOffset * 2
  maxSize = getAvaliableSize() - textSpaceLength
  allText, maxLength = splitWords(text, maxSize)

  sizeY = (textSpaceLength + len(allText)) - 1
  sizeX = (textSpaceLength + maxLength) - 1

  for y in range(sizeY + 1):
    for x in range(sizeX + 1):
      textIndexX = x - squareOffset
      textIndexY = y - squareOffset

      if (textIndexX < 0 or  textIndexY < 0): 
        squareLogic(x,y, sizeX, sizeY)
        continue

      lineSizeY = len(allText) - 1
      if (textIndexY > lineSizeY):
        squareLogic(x,y, sizeX, sizeY)
        continue

      lineSizeX = len(allText[textIndexY]) - 1

      if (textIndexX > lineSizeX): 
        squareLogic(x,y, sizeX, sizeY)
        continue

      print(allText[textIndexY][textIndexX], end='')
    print()


drawnSquare('Bom dia')
      


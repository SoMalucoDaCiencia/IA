from enum import Enum
            
class Circle:
    def __init__(self, x, y, player):
        self.X = x # int
        self.Y = y # int
        self.player = player # bool

class Schema:
    def __init__(self):
        self.contentSize = 0  # int
        self.content = []  # []Square

        for x in range(0, 7):
            for y in range(0, 6):
               self.content.append(Circle(x, y, None))

    def getAt(self, x, y):
        if y < 0 or y == 6 or x < 0 or x == 7:
            raise Exception("Invalid Index (getAt)")

        index = (6 - (y + 1)) * 7 + x
        if len(self.content) > index:
            return self.content[index]
        else:
            raise Exception("Invalid Index (getAt)")
    
    def setAt(self, x, y, player):
        if y < 0 or y == 6 or x < 0 or x == 7:
            raise Exception("Invalid Index (setAt)")

        index = (6 - (y + 1)) * 7 + x
        if len(self.content) > index:
            self.content[index].player = player 
        else:
            raise Exception("Invalid Index (setAt)")
        
    def print(self):
        for y in range(5, -1, -1):
            board = ""
            for x in range(0, 7):
               circle = self.getAt(x, y)
               if circle.player == True:
                   board += '\033[96m' + " ● " + '\033[0m'
               elif circle.player == False:
                   board += '\033[93m' + " ● " + '\033[0m'
               else:
                   board += " • "
            print(board)
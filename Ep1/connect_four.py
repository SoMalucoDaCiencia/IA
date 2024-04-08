import re

# Classe para cada círculo/posição do tabuleiro
class Circle:
    def __init__(self, x, y, player):
        self.X = x # int
        self.Y = y # int
        self.player = player # bool -> None = vazio, True = agente e False = humano

# Classe do jogo inteiro
class Schema:
    COLLUMNS = 7
    ROWS = 6

    def __init__(self):
        self.contentSize = 0  # int
        self.content = []  # []Circle

        # Cria um tabuleiro com 42 espaços vazios
        for x in range(0, self.COLLUMNS):
            for y in range(0, self.ROWS):
               self.content.append(Circle(x, y, None))

    # Retorna as posições do tabuleiro
    def getAt(self, x, y):
        if y < 0 or y == self.ROWS or x < 0 or x == self.COLLUMNS:
            raise Exception("Invalid Index (getAt)")

        index = (self.ROWS - (y + 1)) * self.COLLUMNS + x
        if len(self.content) > index:
            return self.content[index]
        else:
            raise Exception("Invalid Index (getAt)")

    # Cria as posições do tabuleiro   
    def setAt(self, x, y, player):
        if y < 0 or y == self.ROWS or x < 0 or x == self.COLLUMNS:
            raise Exception("Invalid Index (setAt)")

        index = (self.ROWS - (y + 1)) * self.COLLUMNS + x
        if len(self.content) > index:
            self.content[index].player = player 
        else:
            raise Exception("Invalid Index (setAt)")
    
    # Printa o tabuleiro    
    def printBoard(self):
        for y in range(self.ROWS-1, -1, -1):
            board = ""
            for x in range(0, self.COLLUMNS):
               circle = self.getAt(x, y)
               if circle.player == True:
                   board += '\033[96m' + " ● " + '\033[0m' # Player azul 
               elif circle.player == False:
                   board += '\033[93m' + " ● " + '\033[0m' # Player amarelo
               else:
                   board += " • "
            print(board)

    # Valida uma vitória                
    def won(self, player):
        return self.wonHorizontal(player) or self.wonVertical(player) or self.wonDiagonal(player) 
    
    # Verifica se algum player venceu, ou se deu empate      
    def terminalNode(self):
        return self.won(True) or self.won(False) # or self.won(None)

    # Define as posições de vitória
    def wonHorizontal(self, player):
        # Verifica as posições horizontais
        for x in range(0, self.COLLUMNS-3):   
             for y in range(0, self.ROWS): 
                if self.getAt(x, y).player == player and self.getAt(x+1, y).player == player and self.getAt(x+2, y).player == player and self.getAt(x+3, y).player == player:
                    return True
                
    def wonVertical(self, player):
        # Verifica as posições verticais
        for x in range(0, self.COLLUMNS): 
            for y in range(0, self.ROWS-3):
                if self.getAt(x, y).player == player and self.getAt(x, y+1).player == player and self.getAt(x, y+2).player == player and self.getAt(x, y+3).player == player:
                    return True

    def wonDiagonal(self, player):       
        # Verifica as posições diagonais
        for x in range(0, self.COLLUMNS-3): 
            for y in range(0, self.ROWS-3):
                if self.getAt(x, y).player == player and self.getAt(x + 1, y + 1).player == player and self.getAt(x + 2, y + 2).player == player and self.getAt(x + 3, y + 3).player == player:
                    return True
    
    # Verifica a próxima linha jogável 
    def nextValidRow(self, x):
        for y in range(self.ROWS):
            if self.getAt(x, y).player == None:
                return y
    
    # Verifica se a posição está vazia
    def validMoves(self, colIndex):
        y = 0 
        while y < self.ROWS:
            if self.getAt(colIndex, y).player == None:
                return True
            y += 1
        return False

    # Calcula os pontos se baseando na quantidade de peças
    def score(self, player):
       score = 0
       utilMoves = []

       for x in range(self.COLLUMNS):
           for y in range(self.ROWS -3):
               pass
       pass



    def turns(self):
        turn = False
        while True:
            if not turn:
                # jogada = int(re.sub(r'\D', '', input("Escolha um círculo (0-6): "))) % 7
                move = int(input("Escolha um círculo (0-6): "))
                if move <= self.ROWS and self.validMoves(move):
                    row = self.nextValidRow(move) 
                    self.setAt(move, row, False)
                    self.printBoard()
            else:
                print("---------- IA JOGANDO ----------")
                # jogar com IA
                move = int(input("Escolha um círculo (0-6): "))
                if move <= self.ROWS and self.validMoves(move):
                    row = self.nextValidRow(move) 
                    self.setAt(move, row, True)
                    self.printBoard()
            
            turn = not turn

            if self.terminalNode():
                break
            else:
                continue

            # if move <= self.ROWS and move >= 0:
            #     break
            

# def remover_nao_numeros(texto):
#     texto_apenas_numeros = re.sub(r'\D', '', texto)
#     if not texto_apenas_numeros:
#         return 4
#     return texto_apenas_numeros
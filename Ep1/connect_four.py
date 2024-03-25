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

    # Verifica se a posição está vazia
    def validMoves(self):
        valid_moves = []
        for y in range(self.ROWS):
            for x in range(0, self.COLLUMNS):
                if self.getAt(x, y).player == None:
                    valid_moves.append((x, y))
        return valid_moves
                
    # Valida uma vitória                
    def won(self):
        return self.wonDiagonal(self.player) or self.wonHorizontal(self.player) or self.wonVertical(self.player)

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

    # def utility(self, player):
                
    def humanTurn(self):
        jogada = -1
        while jogada not in self.validMoves():
            jogada = int(input("Escolha um círculo (1-7)"))
        return jogada
    
# Para adiconar #
    # Turno
    # Jogar
    # Utilidade
    # Minimax
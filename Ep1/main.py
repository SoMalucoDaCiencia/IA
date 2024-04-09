import re
import copy

JOGADOR_PURO = False
JOGADOR_IA = True
SEM_PLAYER = None

# Classe para cada círculo/posição do tabuleiro
class Circle:
    def __init__(self, x, y, player):
        self.X = x # int
        self.Y = y # int
        self.player = player # bool -> None = vazio

    def copy(self):
        # circle = Circle(self.X, self.Y, self.player)
        # circle.X = self.X
        # circle.Y = self.Y
        # circle.player = self.player
        return Circle(self.X, self.Y, self.player)

# Classe do jogo inteiro
class Schema:
    COLUMNS = 7
    ROWS = 6

    def __init__(self):
        self.content = []  # []Circle

        # Cria um tabuleiro com 42 espaços vazios
        for x in range(0, self.COLUMNS):
            for y in range(0, self.ROWS):
               self.content.append(Circle(x, y, SEM_PLAYER))

    def copySchema(self):
        schema = Schema()
        # schema.content = self.content.copy()
        schema.content = [self.content[i].copy() for i in range(42)]
        return schema

    # Retorna as posições do tabuleiro
    def getAt(self, x, y):
        if y*x < 0 or y >= self.ROWS or x >= self.COLUMNS:
            raise Exception("Invalid Index (getAt)")

        index = (self.ROWS - (y + 1)) * self.COLUMNS + x
        if len(self.content) > index:
            return self.content[index]
        else:
            raise Exception("Invalid Index (getAt)")

    # Configura uma posição do tabuleiro por X e Y
    def setAt(self, x, y, player):
        if y < 0 or y == self.ROWS or x < 0 or x == self.COLUMNS:
            raise Exception("Invalid Index (setAt)")

        index = (self.ROWS - (y + 1)) * self.COLUMNS + x
        if len(self.content) > index:
            self.content[index].player = player
        else:
            raise Exception("Invalid Index (setAt)")

    # Configura uma posição do tabuleiro por coluna
    def setAtCol(self, col, player):
        if col < 0 or col == self.COLUMNS:
            raise Exception("Invalid Index (setAtCol)")
        for y in range(self.ROWS):
            if self.getAt(col, y).player == SEM_PLAYER:
                self.setAt(col, y, player)
                break
            elif y == self.COLUMNS-1:
                return "error"

    # Printa o tabuleiro
    def printBoard(self):
        for y in range(self.ROWS-1, -1, -1):
            board = ""
            for x in range(0, self.COLUMNS):
               circle = self.getAt(x, y)
               if circle.player == JOGADOR_IA:
                   board += '\033[91m' + " ● " + '\033[0m' # VERMELHO
               elif circle.player == JOGADOR_PURO:
                   board += '\033[93m' + " ● " + '\033[0m' # AMARELO
               else:
                   board += " • "
            print(board)

    # Pontua tabuleiro e retorna qual jogada fazer TODO: diagonal
    def scorePlayer(self, player):
        score = 0
        # Verifica as posições horizontais
        for y in range(self.ROWS):
            wonRow, loseScore, noScore = 0, 0, 0
            for x in range(self.COLUMNS):
                circle = self.getAt(x, y).player
                if circle == player:
                    wonRow += 1
                elif circle == SEM_PLAYER:
                    noScore += 1
                else:
                    loseScore += 1
        
            if wonRow == 4:
                score += 100
            elif wonRow == 3 and noScore >= 1:
                score += 5
            elif wonRow == 2 and noScore >= 2:
                score += 2
            if loseScore == 3 and noScore >= 1:
                score -= 4

        # Verifica as posições verticais
        for x in range(self.COLUMNS):
            wonRow, loseScore, noScore = 0, 0, 0
            for y in range(self.ROWS):
                circle = self.getAt(x, y).player
                if circle == player:
                    wonRow += 1
                elif circle == SEM_PLAYER:
                    noScore += 1
                else:
                    loseScore += 1
        
            if wonRow == 4:
                score += 100
            elif wonRow == 3 and noScore >= 1:
                score += 5
            elif wonRow == 2 and noScore >= 2:
                score += 2
            if loseScore == 3 and noScore >= 1:
                score -= 4

        return score

    # Valida uma vitória TODO: diagonal
    def won(self, player):
        # Verifica as posições horizontais
        for y in range(0, self.ROWS):
            wonRow = 0
            for x in range(0, self.COLUMNS):
                if self.getAt(x, y).player == player:
                    wonRow += 1
                    if wonRow >= 4:
                        return True
                else:
                    wonRow = 0 
            wonRow = 0

        # Verifica as posições verticais
        for x in range(0, self.COLUMNS):
            wonCol = 0
            for y in range(0, self.ROWS):
                if self.getAt(x, y).player == player:
                    wonCol += 1
                    if wonCol >= 4:
                        return True
                else:
                    wonCol = 0
            wonCol = 0

        # Verifica as posições diagonais
        for x in range(0, self.COLUMNS-3):
            for y in range(0, self.ROWS-3):
                if self.getAt(x, y).player == player and self.getAt(x + 1, y + 1).player == player and self.getAt(x + 2, y + 2).player == player and self.getAt(x + 3, y + 3).player == player:
                    print("aqui 2")
                    return True

        return False

    # actual: profundidade atual, max: profundidade maxima, pos: posicao a ser jogada, min: booleano de min ou de max
    def minmax(self, actual, maxDepth, min, player):
        if actual == maxDepth:
            return self.scorePlayer( not player)
        list = []
        for x in range(0, self.COLUMNS):
            n = self.copySchema()
            if n.setAtCol(x, player) != "error":
                list.append((x, n.minmax(actual+1, maxDepth, not min, player)))
        list = sorted(list, key=lambda tup: tup[1])
        return list[0 if min else 6][0]

    # Verifica a próxima linha jogável
    def nextValidRow(self, x):
        for y in range(self.ROWS):
            if self.getAt(x, y).player == SEM_PLAYER:
                return True

    # Pega o input do usuario e tranforma em coluna
    def colunInput(self):
        move = re.sub(r'[^\d-]', '', input("Escolha uma coluna (0-6): "))
        while len(move) <= 0 or int(move) >= self.COLUMNS or int(move) < 0 or not self.nextValidRow(int(move)):
            move = input("Esse input não é válido ou acoluna já está ocupada. Escolha novamente (0-6): ")
            move = re.sub(r'[^\d-]', '', move)
        return int(move)

    # Começa o jogo
    def startGame(self, startWith):
        while True:
            if not startWith:
                print("\n---------- Vez do usuário ----------\n")
                move = self.colunInput()
                self.setAtCol(move, JOGADOR_PURO)
                print(self.scorePlayer(JOGADOR_PURO))
                if self.won(JOGADOR_PURO):
                    self.printBoard()
                    print("\n---------- Vitória do usuário ----------\n")
                    exit(0)

            else:
                print("\n------------- Vez da IA ------------\n")
                # move = self.colunInput()
                self.setAtCol(self.minmax(0, 5, False, JOGADOR_IA), JOGADOR_IA)
                print(self.scorePlayer(JOGADOR_IA))
                if self.won(JOGADOR_IA):
                    self.printBoard()
                    print("\n------------- Vitória da IA -------------\n")
                    exit(0)

            self.printBoard()
            startWith = not startWith


jogo = Schema()
jogo.printBoard()
jogo.startGame(JOGADOR_PURO)
# jogo.setAtCol(5, JOGADOR_PURO)
# jogo.setAtCol(5, JOGADOR_PURO)
# jogo.setAtCol(5, JOGADOR_PURO)
# jogo.setAtCol(6, JOGADOR_IA)
# jogo.setAtCol(6, JOGADOR_IA)
# jogo.printBoard()
# print(jogo.scorePlayer(JOGADOR_IA))
# print(jogo.scorePlayer(JOGADOR_PURO))

 
#  •  •  •  •  •  •  • 
#  •  •  •  •  •  •  • 
#  •  •  •  •  •  •  • 
#  •  •  •  •  •  •  • 
#  •  •  •  •  ●  •  •
#  •  •  •  ●  •  •  • 

from connect_four import Schema

jogo = Schema()
jogo.printBoard()
jogo.boardScore(False)
jogo.turns()
print(jogo.score(False))
print(jogo.score(True))



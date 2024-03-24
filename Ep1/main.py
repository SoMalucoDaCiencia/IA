from connect_four import Schema

jogo = Schema()
jogo.setAt(3, 1, False)
jogo.setAt(4, 2, False)
jogo.setAt(5, 3, False)
jogo.setAt(6, 4, False)
print(jogo.wonDiagonal(False))
jogo.printBoard()
import unittest
from tic_tac_toe import criar_tabuleiro, fazer_jogada, verificar_vitoria, verificar_empate

class TestTicTacToe(unittest.TestCase):

    def test_criar_tabuleiro(self):
        tabuleiro = criar_tabuleiro()
        self.assertEqual(tabuleiro, [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    def test_fazer_jogada(self):
        tabuleiro = criar_tabuleiro()
        fazer_jogada(tabuleiro, 0, 'X')
        self.assertEqual(tabuleiro[0], 'X')

    def test_verificar_vitoria_linhas(self):
        # Vitória na primeira linha
        tabuleiro = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(verificar_vitoria(tabuleiro, 'X'))
        # Vitória na segunda linha
        tabuleiro = [' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ']
        self.assertTrue(verificar_vitoria(tabuleiro, 'O'))

    def test_verificar_vitoria_colunas(self):
        # Vitória na primeira coluna
        tabuleiro = ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']
        self.assertTrue(verificar_vitoria(tabuleiro, 'X'))
        # Vitória na segunda coluna
        tabuleiro = [' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' ']
        self.assertTrue(verificar_vitoria(tabuleiro, 'O'))

    def test_verificar_vitoria_diagonais(self):
        # Vitória na diagonal principal
        tabuleiro = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
        self.assertTrue(verificar_vitoria(tabuleiro, 'X'))
        # Vitória na diagonal secundária
        tabuleiro = [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
        self.assertTrue(verificar_vitoria(tabuleiro, 'O'))

    def test_verificar_empate(self):
        tabuleiro = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        self.assertTrue(verificar_empate(tabuleiro))

    def test_nao_vitoria_nem_empate(self):
        tabuleiro = ['X', 'O', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertFalse(verificar_vitoria(tabuleiro, 'X'))
        self.assertFalse(verificar_vitoria(tabuleiro, 'O'))
        self.assertFalse(verificar_empate(tabuleiro))

if __name__ == '__main__':
    unittest.main()


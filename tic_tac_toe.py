# tic_tac_toe.py

import random

def criar_tabuleiro():
    return [str(i+1) for i in range(9)] # Inicializa com números de 1 a 9

def exibir_tabuleiro(tabuleiro):
    print("\n")
    print(f" {tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]} ")
    print("-----------")
    print(f" {tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]} ")
    print("-----------")
    print(f" {tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]} ")
    print("\n")

def jogada_valida(tabuleiro, posicao):
    # A posição agora é de 1 a 9, então o índice do array é posicao - 1
    return 1 <= posicao <= 9 and tabuleiro[posicao - 1] not in ["X", "O"]

def fazer_jogada(tabuleiro, posicao, jogador):
    tabuleiro[posicao - 1] = jogador # Ajusta para índice do array

def verificar_vitoria(tabuleiro, jogador):
    # Linhas
    for i in range(0, 9, 3):
        if all(tabuleiro[i + j] == jogador for j in range(3)):
            return True
    # Colunas
    for i in range(3):
        if all(tabuleiro[i + j * 3] == jogador for j in range(3)):
            return True
    # Diagonais
    if (tabuleiro[0] == jogador and tabuleiro[4] == jogador and tabuleiro[8] == jogador) or \
       (tabuleiro[2] == jogador and tabuleiro[4] == jogador and tabuleiro[6] == jogador):
        return True
    return False

def verificar_empate(tabuleiro):
    # Verifica se todos os espaços foram preenchidos por X ou O
    return all(celula in ["X", "O"] for celula in tabuleiro)

def jogada_ia(tabuleiro, jogador_ia, jogador_humano):
    # 1. Verificar se a IA pode vencer na próxima jogada
    for i in range(9):
        if jogada_valida(tabuleiro, i + 1): # jogada_valida espera 1-9
            tabuleiro_copia = list(tabuleiro)
            fazer_jogada(tabuleiro_copia, i + 1, jogador_ia) # fazer_jogada espera 1-9
            if verificar_vitoria(tabuleiro_copia, jogador_ia):
                return i + 1

    # 2. Verificar se o jogador humano pode vencer na próxima jogada e bloquear
    for i in range(9):
        if jogada_valida(tabuleiro, i + 1):
            tabuleiro_copia = list(tabuleiro)
            fazer_jogada(tabuleiro_copia, i + 1, jogador_humano)
            if verificar_vitoria(tabuleiro_copia, jogador_humano):
                return i + 1

    # 3. Tentar o centro
    if jogada_valida(tabuleiro, 5): # Posição 5 é o centro
        return 5

    # 4. Tentar os cantos
    cantos = [1, 3, 7, 9]
    random.shuffle(cantos)
    for i in cantos:
        if jogada_valida(tabuleiro, i):
            return i

    # 5. Tentar os lados
    lados = [2, 4, 6, 8]
    random.shuffle(lados)
    for i in lados:
        if jogada_valida(tabuleiro, i):
            return i
    
    return -1 # Não deveria chegar aqui em um tabuleiro não cheio

def jogar_jogo_da_velha():
    print("Bem-vindo ao Jogo da Velha!")
    while True:
        modo = input("Escolha o modo de jogo (1 para Jogador vs Jogador, 2 para Jogador vs IA): ")
        if modo in ["1", "2"]:
            break
        else:
            print("Opção inválida. Por favor, escolha 1 ou 2.")

    tabuleiro = criar_tabuleiro()
    jogador_atual = "X"
    jogo_ativo = True

    while jogo_ativo:
        exibir_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador_atual}")
        
        posicao = -1
        if modo == "1": # Jogador vs Jogador
            while True:
                try:
                    posicao_str = input("Escolha uma posição (1-9): ")
                    posicao = int(posicao_str)
                    if jogada_valida(tabuleiro, posicao):
                        break
                    else:
                        print("Posição inválida ou já ocupada. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número entre 1 e 9.")
        else: # Jogador vs IA
            if jogador_atual == "X": # Jogador humano
                while True:
                    try:
                        posicao_str = input("Escolha uma posição (1-9): ")
                        posicao = int(posicao_str)
                        if jogada_valida(tabuleiro, posicao):
                            break
                        else:
                            print("Posição inválida ou já ocupada. Tente novamente.")
                    except ValueError:
                        print("Entrada inválida. Por favor, digite um número entre 1 e 9.")
            else: # IA
                print("IA está fazendo sua jogada...")
                posicao = jogada_ia(tabuleiro, "O", "X")
                print(f"IA jogou na posição {posicao}")

        fazer_jogada(tabuleiro, posicao, jogador_atual)
        if verificar_vitoria(tabuleiro, jogador_atual):
            exibir_tabuleiro(tabuleiro)
            print(f"Parabéns! O jogador {jogador_atual} venceu!")
            jogo_ativo = False
        elif verificar_empate(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("O jogo empatou!")
            jogo_ativo = False
        else:
            jogador_atual = "O" if jogador_atual == "X" else "X"

if __name__ == "__main__":
    jogar_jogo_da_velha()



from flask import Blueprint, request, jsonify
import random

game_bp = Blueprint('game', __name__)

def calculate_winner(board):
    """Verifica se há um vencedor no tabuleiro"""
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # colunas
        [0, 4, 8], [2, 4, 6]              # diagonais
    ]
    
    for line in lines:
        a, b, c = line
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return board[a]
    return None

def is_draw(board):
    """Verifica se o jogo empatou"""
    return all(cell is not None for cell in board) and not calculate_winner(board)

def is_valid_move(board, position):
    """Verifica se a jogada é válida (posição de 1 a 9)"""
    return 1 <= position <= 9 and board[position - 1] is None

def make_ai_move(board):
    """Faz a jogada da IA usando a mesma lógica do jogo CLI"""
    # Converter board para formato compatível com a lógica original
    # None -> número da posição, 'X'/'O' -> mantém
    converted_board = []
    for i, cell in enumerate(board):
        if cell is None:
            converted_board.append(str(i + 1))
        else:
            converted_board.append(cell)
    
    # 1. Verificar se a IA pode vencer na próxima jogada
    for i in range(9):
        if converted_board[i] not in ["X", "O"]:
            test_board = converted_board.copy()
            test_board[i] = "O"
            if calculate_winner(test_board) == "O":
                return i + 1
    
    # 2. Verificar se o jogador humano pode vencer na próxima jogada e bloquear
    for i in range(9):
        if converted_board[i] not in ["X", "O"]:
            test_board = converted_board.copy()
            test_board[i] = "X"
            if calculate_winner(test_board) == "X":
                return i + 1
    
    # 3. Tentar o centro
    if converted_board[4] not in ["X", "O"]:
        return 5
    
    # 4. Tentar os cantos
    corners = [1, 3, 7, 9]
    random.shuffle(corners)
    for corner in corners:
        if converted_board[corner - 1] not in ["X", "O"]:
            return corner
    
    # 5. Tentar os lados
    sides = [2, 4, 6, 8]
    random.shuffle(sides)
    for side in sides:
        if converted_board[side - 1] not in ["X", "O"]:
            return side
    
    return -1  # Não deveria chegar aqui

@game_bp.route('/ai-move', methods=['POST'])
def ai_move():
    """Endpoint para a IA fazer uma jogada"""
    try:
        data = request.get_json()
        board = data.get('board', [])
        
        if len(board) != 9:
            return jsonify({'error': 'Tabuleiro inválido'}), 400
        
        # Verificar se o jogo já terminou
        if calculate_winner(board) or is_draw(board):
            return jsonify({'error': 'Jogo já terminou'}), 400
        
        # Fazer a jogada da IA
        ai_position = make_ai_move(board)
        
        if ai_position == -1:
            return jsonify({'error': 'Não foi possível fazer uma jogada'}), 500
        
        return jsonify({
            'position': ai_position,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@game_bp.route('/validate-move', methods=['POST'])
def validate_move():
    """Endpoint para validar uma jogada"""
    try:
        data = request.get_json()
        board = data.get('board', [])
        position = data.get('position')
        
        if len(board) != 9:
            return jsonify({'error': 'Tabuleiro inválido'}), 400
        
        is_valid = is_valid_move(board, position)
        
        return jsonify({
            'valid': is_valid,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@game_bp.route('/game-status', methods=['POST'])
def game_status():
    """Endpoint para verificar o status do jogo"""
    try:
        data = request.get_json()
        board = data.get('board', [])
        
        if len(board) != 9:
            return jsonify({'error': 'Tabuleiro inválido'}), 400
        
        winner = calculate_winner(board)
        draw = is_draw(board)
        
        return jsonify({
            'winner': winner,
            'draw': draw,
            'finished': winner is not None or draw,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


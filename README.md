# Jogo-da-Velha
Descrição para o jogo da Velha 


# Instruções de Deploy do Jogo da Velha Web

Este documento fornece as instruções para fazer o deploy da aplicação web do Jogo da Velha, que consiste em um frontend React e um backend Flask.

## Estrutura do Projeto

O projeto é composto por duas partes principais:

- `tic-tac-toe-frontend`: Contém o código-fonte do frontend React.
- `tic-tac-toe-backend`: Contém o código-fonte do backend Flask, que também serve os arquivos estáticos do frontend.

## Pré-requisitos

Certifique-se de ter o seguinte instalado em seu ambiente de deploy:

- Python 3.x
- pip (gerenciador de pacotes Python)
- Node.js e npm/pnpm (para construir o frontend, se necessário, mas os arquivos já estão incluídos no backend para deploy)

## Passos para o Deploy

### 1. Backend (Flask)

O backend Flask já inclui os arquivos estáticos do frontend React pré-construídos no diretório `src/static`.

1.  **Navegue até o diretório do backend:**

    ```bash
    cd tic-tac-toe-backend
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências do Python:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação Flask:**

    ```bash
    python src/main.py
    ```

    Por padrão, a aplicação será executada em `http://0.0.0.0:5000`. Se a porta 5000 estiver em uso, você pode especificar outra porta:

    ```bash
    python src/main.py --port 8000
    ```

    Ou, se estiver usando o comando direto:

    ```bash
    python -c "
import sys
sys.path.insert(0, ".")
from src.main import app
app.run(host=\'0.0.0.0\', port=5000, debug=False)
" # Altere a porta se necessário
    ```

    A aplicação Flask servirá o frontend React a partir do diretório `src/static` e também exporá os endpoints da API (ex: `/api/ai-move`).

### 2. Acessando a Aplicação

Após iniciar o servidor Flask, você pode acessar a aplicação web abrindo seu navegador e navegando para o endereço onde o servidor está rodando (por exemplo, `http://localhost:5000` ou `http://seu_ip_do_servidor:5000`).

## Conteúdo do Backend (tic-tac-toe-backend)

### `src/main.py`

```python
import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.routes.game import game_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

CORS(app)

app.register_blueprint(game_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on.')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=False)
```

### `src/routes/game.py`

```python
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
```

### `requirements.txt`

```
click==8.1.3
Flask==3.1.1
Flask-Cors==4.0.1
itsdangerous==2.2.0
Jinja2==3.1.3
MarkupSafe==2.1.5
Werkzeug==3.0.3
```

Com essas instruções e arquivos, você pode fazer o deploy da aplicação em qualquer servidor web que suporte Python e Flask.


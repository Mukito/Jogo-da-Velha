import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import './App.css'

function App() {
  const [board, setBoard] = useState(Array(9).fill(null))
  const [isXNext, setIsXNext] = useState(true)
  const [gameMode, setGameMode] = useState(null) // null, 'pvp', 'ai'
  const [gameStatus, setGameStatus] = useState('waiting') // 'waiting', 'playing', 'finished'
  const [winner, setWinner] = useState(null)

  const calculateWinner = (squares) => {
    const lines = [
      [0, 1, 2],
      [3, 4, 5],
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6],
    ]
    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i]
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a]
      }
    }
    return null
  }

  const isDraw = (squares) => {
    return squares.every(square => square !== null) && !calculateWinner(squares)
  }

  const handleClick = async (i) => {
    if (board[i] || winner || gameStatus !== 'playing') {
      return
    }

    const newBoard = [...board]
    newBoard[i] = isXNext ? 'X' : 'O'
    setBoard(newBoard)

    const gameWinner = calculateWinner(newBoard)
    if (gameWinner) {
      setWinner(gameWinner)
      setGameStatus('finished')
      return
    }

    if (isDraw(newBoard)) {
      setGameStatus('finished')
      return
    }

    if (gameMode === 'ai' && isXNext) {
      // Player made a move, now it's AI's turn
      setIsXNext(false)
      
      // Make AI move after a short delay
      setTimeout(async () => {
        try {
          const response = await fetch('/api/ai-move', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ board: newBoard }),
          })
          
          if (response.ok) {
            const data = await response.json()
            const aiBoard = [...newBoard]
            aiBoard[data.position - 1] = 'O' // API returns 1-9, convert to 0-8
            setBoard(aiBoard)
            
            const aiWinner = calculateWinner(aiBoard)
            if (aiWinner) {
              setWinner(aiWinner)
              setGameStatus('finished')
            } else if (isDraw(aiBoard)) {
              setGameStatus('finished')
            } else {
              setIsXNext(true)
            }
          }
        } catch (error) {
          console.error('Error making AI move:', error)
          setIsXNext(true) // Reset turn on error
        }
      }, 500)
    } else {
      setIsXNext(!isXNext)
    }
  }

  const startGame = (mode) => {
    setGameMode(mode)
    setGameStatus('playing')
    setBoard(Array(9).fill(null))
    setIsXNext(true)
    setWinner(null)
  }

  const resetGame = () => {
    setGameMode(null)
    setGameStatus('waiting')
    setBoard(Array(9).fill(null))
    setIsXNext(true)
    setWinner(null)
  }

  const renderSquare = (i) => {
    return (
      <Button
        key={i}
        className="w-20 h-20 text-2xl font-bold border-2 border-gray-300 hover:bg-gray-100 disabled:opacity-100"
        onClick={() => handleClick(i)}
        disabled={board[i] || winner || gameStatus !== 'playing'}
        variant="outline"
      >
        {board[i]}
      </Button>
    )
  }

  const getStatusMessage = () => {
    if (gameStatus === 'waiting') {
      return 'Escolha um modo de jogo'
    }
    if (winner) {
      return `Jogador ${winner} venceu!`
    }
    if (isDraw(board)) {
      return 'Empate!'
    }
    if (gameMode === 'ai') {
      return isXNext ? 'Sua vez (X)' : 'Vez da IA (O)...'
    }
    return `Vez do jogador ${isXNext ? 'X' : 'O'}`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Jogo da Velha
        </h1>
        
        {gameStatus === 'waiting' && (
          <div className="space-y-4 mb-8">
            <Button 
              onClick={() => startGame('pvp')} 
              className="w-full py-3 text-lg"
            >
              Jogador vs Jogador
            </Button>
            <Button 
              onClick={() => startGame('ai')} 
              className="w-full py-3 text-lg"
              variant="outline"
            >
              Jogador vs IA
            </Button>
          </div>
        )}

        {gameStatus !== 'waiting' && (
          <>
            <div className="text-center mb-6">
              <p className="text-lg font-semibold text-gray-700">
                {getStatusMessage()}
              </p>
            </div>

            <div className="grid grid-cols-3 gap-2 mb-6 justify-center">
              {Array(9).fill(null).map((_, i) => renderSquare(i))}
            </div>

            <div className="space-y-2">
              <Button 
                onClick={resetGame} 
                className="w-full"
                variant="outline"
              >
                Novo Jogo
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default App


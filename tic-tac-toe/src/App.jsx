import Player from "./components/Player"
import GameBoard from "./components/GameBoard"
import Log from "./components/Log";
import { useState } from "react";
import { WINNING_COMBINATIONS } from "./winning_combination";
import GameOver from "./components/GameOver";

const initialGameBoard =[
  [null,null,null],
  [null,null,null],
  [null,null,null]
  
];
const PLAYERS={
  X:'player 1',
  O:'player 2'
};

function deriveActivePlayer(gameTurns){
  let currentPlayer ='X';
  if(gameTurns.length > 0 && gameTurns[0].player==='X'){
    currentPlayer='O';
  }

  return currentPlayer;
}

function deriveGameBoard(gameTurns){
  let gameBoard =[...initialGameBoard.map(array =>[...array])];
    
    for(const turn of gameTurns){
       const{square,player} =turn;
       const{row,col} =square;

       gameBoard[row][col] =player;
    }
 return gameBoard;
}

function deriveWinner(gameBoard,playerName){
  let winner;
  for(const combination of WINNING_COMBINATIONS){
    const firstSquareSymbol = gameBoard[combination[0].row][combination[0].column]
    const secondSquareSymbol = gameBoard[combination[1].row][combination[1].column]
    const thirdSquareSymbol = gameBoard[combination[2].row][combination[2].column]

    if(firstSquareSymbol &&
      firstSquareSymbol === secondSquareSymbol &&
      firstSquareSymbol === thirdSquareSymbol
    )
    {
      winner =playerName[firstSquareSymbol];
    }
  }
  return winner;
}
function App() {
  const [playerName,setPlayer] =useState(PLAYERS);
  const [gameTurns,setGameTurns] =useState([]);
  //const [activePlayer,setActivePlayer] = useState('X');
  const activePlayer=deriveActivePlayer(gameTurns);
  const gameBoard =deriveGameBoard(gameTurns);
  const winner =deriveWinner(gameBoard,playerName);
  const hasDraw =gameTurns.length === 9 && !winner;
   
  function handleSelectSquare(rowIndex,colIndex){
   //setActivePlayer((currentActivePlayer)=>(currentActivePlayer==='X'?'O':'X'));
   setGameTurns((prevTurns) =>{
    const currentPlayer = deriveActivePlayer(prevTurns);
    const updatedTurns =[
      {square:{row : rowIndex,col : colIndex},player:currentPlayer},
      ...prevTurns];

      return updatedTurns;
   });
  }

  function handleRestart(){
    setGameTurns([]);
  }
  function handlePlayerNameChnage(symbol,newName){
    setPlayer(prevplayerName =>{
      return{
        ...prevplayerName,
      [symbol]:newName
      };
      
    }
  );
  }

  return (
    <main>
    <div id='game-container'>
      <ol id='players' className="highlight-player">
        <Player name={PLAYERS.X} symbol='X' isActive={activePlayer ==='X'} isNameChange={handlePlayerNameChnage}/>
        <Player name={PLAYERS.O} symbol='O'isActive={activePlayer ==='O'} isNameChange={handlePlayerNameChnage}/>
      </ol>
      {(winner || hasDraw) && <GameOver winner={winner} onRestart={handleRestart}></GameOver>}
      <GameBoard onSelectSquare={handleSelectSquare}  board={gameBoard}></GameBoard>
    </div>
    
    <Log turns={gameTurns}/>
    </main>
  );
  
}

export default App

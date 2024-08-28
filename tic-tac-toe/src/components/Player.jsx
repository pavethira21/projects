import { useState } from "react";
export default function Player({name,symbol,isActive,isNameChange}){
    const [isEditing,setEditing]=useState(false);
    const[playerName,setEditedName] =useState(name);
    function handleClick(){
        setEditing(editing =>!editing);
        
        console.log(isEditing);
    }

    let player=<span className="player-name">{playerName}</span>;
    function handleChange(event){
        setEditedName(event.target.value);
        if(isEditing){
        isNameChange(symbol,playerName);
        }
    }
    if(isEditing){
        player=<input type="text" required value={playerName} onChange={handleChange}/>
    }
    return(
    <li className={isActive?'active':undefined}>
          <span className="player">
          {player}
          <span className="player-symbol">{symbol}</span>
          </span>
          <button onClick={handleClick}>{isEditing? 'save':'Edit'}</button>
          
        </li>
    );
}
import React, { Component } from 'react'
import useWebSocket from 'react-use-websocket'
import './App.css';
import { useState } from 'react';




const lobbyid = window.location.pathname.split('/')[3]

function GameBoard() {
  const [board, setBoard] = useState([0, 9, 0])


  const ws = new WebSocket(
    "ws://"
    + window.location.host
    + "/ws/asgi/"
    + lobbyid + "/"
  );



  function inputHandler(event) {

    switch (event.key) {
      case "w":
        ws.send(JSON.stringify({ "direction": "up" }));
        break;
      case "a":
        ws.send(JSON.stringify({ "direction": "left" }));
        break;
      case "d":
        ws.send(JSON.stringify({ "direction": "right" }));
        break;
      case "s":
        ws.send(JSON.stringify({ "direction": "down" }));
        break;
    }

  };


  ws.onmessage = (text_data) => {
    console.log(text_data)
    setBoard(text_data.data);
    console.log(text_data.data);
  }

  ws.onopen = (event) => {

    document.addEventListener("keydown", inputHandler);

  };

  ws.onclose = (event) => {
    console.log('oh no connetion is lost');
    document.removeEventListener("keydown", inputHandler);
  };




}



function StartGameButton() {
  return (<button onClick={startGame}>START GAME BUTTOOONN !!!!</button>)
}

function startGame() {
  fetch('http://' + window.location.host + "/snakeo/api/", {
    method: 'POST',
    body: JSON.stringify({
      lobby_id: lobbyid
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  })
    .then(() => console.log('startedgame, get response'))
    .catch((err) => {

      console.log(err.message);

    })
};

// есть листенер на нажатия и есть функция отображения поля,
// не думаю что нужно делать какую-то сложную локигу построения компонентов,
// так как вся логика будет на стороне сервера
// Я совсем  не знаю js Это нужно изучить заранее

export default function App() {
  return (
    <html>
      <body>
        <div>
          <GameBoard />
          <StartGameButton />
        </div>
      </body>
    </html>
  )
}



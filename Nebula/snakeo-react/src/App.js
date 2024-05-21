import React, { Component } from 'react'
import useWebSocket from 'react-use-websocket'
import './App.css';
import { useState } from 'react';

import { useEffect, useRef } from 'react'


// OK done for today, useState reaolds websocket connect, need to separate canvas from ws connection. Problem is how to update Canvas state from another function

const lobbyid = window.location.pathname.split('/')[3]


function GameBoard() {
  const map = []; /// temporary kostil :p
  const map_size = 10; // temporary

  for (var i = 0; i < map_size; i++) { ///assume that we have olny square maps 
    map[i] = [];
    for (var j = 0; j < map_size; j++) {
      map[i][j] = 0;
    }
  }

  const [board, setBoard] = useState(map); // how to get geN?
  const socketRef = useRef();

  console.table(board);

  const Canvas = props => {
    const ref = useRef();

    useEffect(() =>  // running after element is mount
    {
      const canvas = ref.current;
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, 500, 500) // TODO koslis
      context.fillStyle = 'red';
      for (var i = 0; i < map_size; i++) {
        for (var j = 0; j < map_size; j++) {
          if (board[i][j] == 1) {
            context.fillRect(i * 50, j * 50, 50, 50);
          }
        }
      }

    }, [])  // idk wht is that for

    return <canvas ref={ref} {...props} />
  }

  const ws = new WebSocket(
    "ws://"
    + window.location.host
    + "/ws/asgi/"
    + lobbyid + "/"
  );


  useEffect(() => {
    // Проверяем, было ли уже установлено соединение
    if (!socketRef.current) {
      // Если соединение еще не установлено, создаем новое
      socketRef.current = new WebSocket(url);
    }

    // Закрытие соединения при размонтировании компонента
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [url]);

  function inputHandler(event) {

    switch (event.key) {
      case "w":
        socketRef.current.send(JSON.stringify({ "direction": "up" }));
        break;
      case "a":
        socketRef.current.send(JSON.stringify({ "direction": "left" }));
        break;
      case "d":
        socketRef.current.send(JSON.stringify({ "direction": "right" }));
        break;
      case "s":
        socketRef.current.send(JSON.stringify({ "direction": "down" }));
        break;
    }

  };


  ws.onmessage = (text_data) => {
    console.log(text_data)
    var new_board = map.slice();
    const food = JSON.parse(text_data.data)["food"];
    const snakes = JSON.parse(text_data.data)["snakes"];


    for (var i = 0; i < food.length; i++) {
      new_board[food[i][0]][food[i][1]] = 1;  // LOOL
    } //// IT WORKS !!! :>

    for (var i = 0; i < snakes.length; i++) {
      const snake_body = snakes[i]["body"];
      for (var j = 0; j < snake_body.length; j++) {
        new_board[snake_body[j][0]][snake_body[j][1]] = 1; // TODO rewrite this unreadable
      }
    }
    //for(var key in text_data.data){
    //}
    //{"food": [[6, 6]], "snakes": [{"body": [[2, 0], [3, 0], [4, 0]], "score": 0, "living": true, "name": "AnonymousUser"}]}  --DATA
    setBoard(new_board);
    console.log(map.slice());
    console.log(text_data.data);
  }

  ws.onopen = (event) => {

    document.addEventListener("keydown", inputHandler);

  };

  ws.onclose = (event) => {
    console.log('oh no connetion is lost');
    document.removeEventListener("keydown", inputHandler);
  };



  return <Canvas height="500" weight="500" />; ///works
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



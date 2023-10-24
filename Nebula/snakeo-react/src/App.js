import React, { Component } from 'react'
import useWebSocket from 'react-use-websocket'
import './App.css';



function App() {

  const ws = new WebSocket(
    "ws://"
    + window.location.host
    + "/ws/asgi/"
  );

  ws.onopen = (event) => {
    console.log('heyyya');
  };

  ws.onclose = (event) => {
    console.log('oh no connetion is lost');
  };

  console.log(window.location.host)


  return (
    <html>
      <body>
        <div>
          appjs
        </div>
      </body>
    </html>
  )
}

export default App;


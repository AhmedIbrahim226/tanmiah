const newWebsocket = () => {
    // if protocol https:// wss ,,,,, if protocol http:// ws
    
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/post/consumer/`)
    socket.onopen = (e) => {
        console.log('Websocket opened');
    }
    return socket;
}

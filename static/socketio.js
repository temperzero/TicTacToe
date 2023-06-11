document.addEventListener('DomContentLoaded', () => {
	var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        socket.send('I am connected!');
    });

    socket.on('message', data => {
    	console.log(`message received ${data}`)
    });
})
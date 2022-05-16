const express = require('express')
var send = require('./send')
const fs = require('fs')
const util = require('util')
var cors = require('cors')
const multer = require('multer')
const upload = multer({ dest: 'uploads/' })
const app = express()
var amqp = require('amqplib/callback_api');
var server = require('http').Server(app) 
var socketIO = require('socket.io')(server)

var calcSocket = socketIO.of('/calc')


app.use(cors())

amqp.connect('amqp://localhost', function(error0, connection) {
  if (error0) {
    throw error0;
  }
  connection.createChannel(function(error1, channel) {
    if (error1) {
      throw error1;
    }
    var queue = 'result';

    channel.assertQueue(queue, {
      durable: true
    });

    console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);
    channel.consume(queue, function(msg) {
      console.log("msg recieved",msg.content.toString())
      var result = JSON.stringify(msg.content.toString());
      //calcSocket.emit('calc', result)
    }, {
      noAck: true
    });
  });
});

app.put('/predict', upload.single('image'), async (req, res) => {

  const response = await send.send(req.file.path)
}) 

app.listen(8080, () => console.log("listening on port 8080"))

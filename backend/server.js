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

let results = [];

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
      console.log("msg recieved", msg.content.toString())
      results.push(msg.content.toString());
    }, {
      noAck: true
    });
  });
});

app.post('/upload', upload.single('image'), async (req, res) => {
  const response = await send.send(req.file.path)
  return res.status(200).json({ result: true, msg: 'file uploaded' });
}) 

app.get("/process", (req, res) => {
  if(results.length === 0) return res.status(400).json({results: false, msg: "Files didn't get processed"});
  return res.status(200).json({results, msg: "Files processed"});
})

app.delete("/upload", (req, res) => {
    results.splice(req.query.index, 1);
    return res.status(200).json({ result: true, msg: 'file deleted' });
});

app.delete("/refresh", (req, res) => {
    results = [];
    return res.status(200).json({ result: true, msg: 'files deleted' });
})

app.listen(8080, () => console.log("listening on port 8080"))

const express = require('express')
var send = require('./send')
const fs = require('fs')
const util = require('util')
const unlinkFile = util.promisify(fs.unlink)
var cors = require('cors')
const multer = require('multer')
const upload = multer({ dest: 'uploads/' })
const axios = require('axios')
//const { uploadFile, getFileStream } = require('./s3')

const app = express()
app.use(cors())
app.get('/images/:key', (req, res) => {
  console.log(req.params)
  const key = req.params.key
  const readStream = getFileStream(key)

  readStream.pipe(res)
})

app.put('/predict', upload.single('image'), async (req, res) => {

  const response = await send.send(req.file.path)
})

app.listen(8080, () => console.log("listening on port 8080"))

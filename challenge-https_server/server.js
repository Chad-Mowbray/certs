//starting point

const express = require('express')
const http = require('http')

const app = express()

app.use(express.static('public'))

app.get('/', function (req, res) {
  res.render("index.html")
})

http.createServer(app)
.listen(3333, function () {
  console.log('Listening on localhost:3333...')
})
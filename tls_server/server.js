//starting point

// const express = require('express')
// const http = require('http')

// const app = express()

// app.use(express.static('public'))

// app.get('/', function (req, res) {
//   res.render("index.html")
// })

// http.createServer(app)
// .listen(3333, function () {
//   console.log('Listening on localhost:3333...')
// })






// http server with password submit

// const express = require('express')
// const http = require('http')

// const app = express()

// app.use(express.static('public'))


// app.get('/', function (req, res) {
//   res.render("index.html")
// })

// app.post("/login", function(req, res) {
//   res.send("Thank you for submitting your password")
// })


// http.createServer(app)
// .listen(3000, function () {
//   console.log('Example app listening on port 3000! Go to https://localhost:3000/')
// })















// the https version:

// const express = require('express')
// const fs = require('fs')
// const https = require('https')
// const app = express()

// app.get('/', function (req, res) {
//   res.send('hello world')
// })

// const options = {
//   key: fs.readFileSync('key.pem'),
//   cert: fs.readFileSync('cert.pem')
// };

// https.createServer(options, app)
// .listen(3000, function () {
//   console.log('Example app listening on port 3000! Go to https://localhost:3000/')
// })



// show that its actually encrypted using wireshark
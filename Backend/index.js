let express = require('express');
let mongoose = require('mongoose');
let bodyParser = require('body-parser');
let path = require('path');
let imageRoutes = require('./routes/image');
let mainRoutes = require('./routes/main')



// setup express app
let app = express();

// connect to mongodb
mongoose.connect(<your_mongo_connection>);
mongoose.Promise = global.Promise;

// use the body parser
app.use(bodyParser.json());

app.use('/public', express.static('public'))
app.set('view engine', 'ejs');

// redirect to the api routes
app.use('', mainRoutes);
app.use('/image', imageRoutes);
 
app.use(function(err, req, res, next){
    res.status(422);
    res.send({error: err.message});
});

// listen to requests
app.listen(process.env.port || 8000, function(){
    console.log('Server runningon port 8000 > http://127.0.0.1:8000');
});


























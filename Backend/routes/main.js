let express = require('express');
let router = express.Router();
let fetch = require('node-fetch');

router.get('/', (req, res) => {
    res.render('index');
});

router.get('/upload', (req, res) => {
    res.render('upload');
});


router.get('/getpredict', (req, res) => {
    async function getPredictData () {
        try{
            let response = await fetch('http://127.0.0.1:5000/'); // change this to the python 5000 port
            let data = await response.json();
            // res.json(data);
            res.render('../views/final', data);
        }
        catch(error){
            console.log("######### ERROR ##########")
            // console.log(error);
        }
    };
    getPredictData()
});



module.exports = router;






















let express = require('express');
let router = express.Router();
let fetch = require('node-fetch');

router.get('/', (req, res) => {
    res.render('index');
});

router.get('/upload', (req, res) => {
    res.render('upload');
});


// report page data is sent from here.

router.get('/getpredict', (req, res) => {
    async function getPredictData () {
        try{
            let response = await fetch('http://127.0.0.1:5000/'); 
            let api_data = await response.json();
            // res.json(data);
            // console.log(data["image_data"]["rawdata"]["name"])
            data = {
                "prediction": api_data["prediction"],
                "name": api_data["image_data"]["rawdata"]["name"],
                "age":api_data["image_data"]["rawdata"]["age"],
                // "email": api_data["image_data"]["rawdata"]["email"],
                "gender": api_data["image_data"]["rawdata"]["gender"],
                "number": api_data["image_data"]["rawdata"]["number"],
                "ses": api_data["image_data"]["rawdata"]["ses"],
                "mmse": api_data["image_data"]["rawdata"]["mmse"],
                "asf": api_data["image_data"]["rawdata"]["asf"],
                "etiv": api_data["image_data"]["rawdata"]["etiv"],
                "educ": api_data["image_data"]["rawdata"]["educ"],
                "nebv": api_data["image_data"]["rawdata"]["nebv"]
            };
            res.render('../views/final', data);
        }
        catch(error){
            console.log("## ERROR: Couldnot fetch from port 50000 ##")
            console.log("1. Connect to the internet\n2. run server at port 5000")
            // console.log(error);
        }
    };
    getPredictData()
});



module.exports = router;






















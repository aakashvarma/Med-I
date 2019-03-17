let express = require('express');
let router = express.Router();
let multer = require('multer');
let fs = require('fs')
let bodyParser = require('body-parser')
let extend = require('extend');

let imageUpload = require('../models/photo');

// global variable declaration
let image_data
let raw_data


let storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + '.png')
    }
});

let upload = multer({ storage: storage }).single('profileImage');

let urlencodedParser = bodyParser.urlencoded({ extended: false })

router.post('/upload', urlencodedParser, function (req, res, next) {
    upload(req, res, function (err) {
        if (err) {
            // An error occurred when uploading
            console.log('An error has occurred while uploading.');
        }
        imageUpload.create({ success: true,  filename: req.file.filename,  path: req.file.path })
        .then(function(imageData){
            image_data = imageData;
            raw_data = req.body;
            res.redirect("../getpredict")
        }).catch(next);
    });
});

// @route GET - to get api info
router.get('/api', function(req, res){
    res.json({
        imagedata: image_data,
        rawdata: raw_data
    });  // always has to be json
});


// @route GET - to view image
router.get('/view', (req, res) => {
    let readstream = fs.createReadStream(image_data.path);
    readstream.pipe(res);
});

module.exports = router;






































let express = require('express');
let router = express.Router();
let multer = require('multer');

let imageUpload = require('../models/photo');

// global variable declaration
let data


let storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + '.png')
    }
});

let upload = multer({ storage: storage }).single('profileImage');


router.post('/upload', function (req, res, next) {
    upload(req, res, function (err) {
        if (err) {
            // An error occurred when uploading
            console.log('An error has occurred while uploading.');
        }
        imageUpload.create({ success: true,  filename: req.file.filename,  path: req.file.path })
        .then(function(imageData){
            data = imageData;
            // res.send(imageData);
            res.redirect("api")
            console.log("Image uploaded sussessfully and data is sent to the database.")
        }).catch(next);
    });
});

router.get('/api', function(req, res){
    res.send(data);
});


module.exports = router;






































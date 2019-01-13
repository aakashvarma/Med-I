let express = require('express');
let router = express.Router();


router.get('/', (req, res) => {
    res.render('index');
});

router.get('/upload', (req, res) => {
    res.send("this is the uploads page.");
});

module.exports = router;






















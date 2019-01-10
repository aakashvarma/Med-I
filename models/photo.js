let mongoose = require('mongoose');
let Schema = mongoose.Schema;

let ItemSchema = new Schema(
    {
        success: {
            type: Boolean,
            default: false
        },
        filename: {   
            type: String,
            required: [true, 'Name field is required']
        },
        path: {
            type: String,
            required: true
        }
    }
)

let Item = mongoose.model('scannedImage', ItemSchema);

// Export module
module.exports = Item;



















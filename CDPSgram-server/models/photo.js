/* 

Modelo de datos de imágenes (photo)

photoSchema: {
	name: nombre de la imagen,
	url: url de la imagen
} 

*/

var mongoose = require('mongoose'),  
    Schema   = mongoose.Schema;

var photoSchema = new Schema({  
	name: 	{ type: String },
	url: 	{ type: String }
});

module.exports = mongoose.model('Photo', photoSchema);  
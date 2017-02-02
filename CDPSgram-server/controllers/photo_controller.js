var fs = require('fs');
var photo_model = require('mongoose').model('Photo');

// Devuelve una lista de las imagenes disponibles y sus metadatos
exports.list = function (req, res) {
	photo_model.find(function (err, photos) {
		res.render('photos/index', {photos: photos});
	});
};

// Devuelve la vista del formulario para subir una nueva foto
exports.new = function (req, res) {
	res.render('photos/new');
};

// Devuelve la vista de visualización de una foto.
// El campo photo.url contiene la url donde se encuentra el fichero de audio
exports.show = function (req, res) {
	photo_model.find(function (err, photos) {
		var photo_encontrada = photos[req.params.photoId];
		if (err) return res.send(500, err.message);
		res.render('photos/show', { photo: photo_encontrada });
	});
};

// Escribe una nueva foto en el registro de imagenes.
exports.create = function (req, res) {
	var photo = req.files.photo;
	console.log('Nuevo fichero: ', req.body);
	var name = req.body.name;
	var url = req.body.url;
	
	// Escribe los metadatos de la nueva foto en el registro.
	var new_photo = new photo_model({
		name: name,
		url: url
	});
	new_photo.save(function(err, new_photo) {
		if (err) console.log('ERROR: ' + err);
	});
	res.redirect('/photos');
};

// Borra una foto (photoId) del registro de imagenes 
exports.destroy = function (req, res, next) {
	// Aquí debe implementarse el borrado del fichero de audio indetificado por photoId en photos.cdpsfy.es
	photo_model.findById(req.params.photoId).then(function(photo) {
		photo.remove().then(function() {
			res.redirect('/photos');
		});
	}).catch(function(error) {
		next(error);
	});
};
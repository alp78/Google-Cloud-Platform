'use strict';

const gcs = require('@google-cloud/storage')();
const path = require('path');
const sharp = require('sharp');
const async = require('async');
const config = require('./config.json');

exports.createThumb = (event, callback) => {
  const storeObject = event.data;
  
  const filePath = storeObject.name;  // origin/example.jpg
  const fileName = path.basename(filePath);  // example.jpg
  const fileDir = path.dirname(filePath);
  
  if (fileName.startsWith('thumb_')) {
	console.log('Already a thumbnail!');
	callback();
	return;
  }
  
  const contentType = storeObject.contentType;  // image/JPEG
  
  if (!contentType.startsWith('image/')) {
	console.log('This is not an image.');
	callback();
	return;
  }
  
  const originBucketName = storeObject.bucket; // images-ap
  const imgBucket = gcs.bucket(originBucketName);  // {}
  const thumbBucket = gcs.bucket("thumb-img-ap");
  
  const metadata = { contentType: contentType };
  
  var itemsResized = 0;
  var config_size = Object.keys(config).length;
  console.log(`config_size = Object.keys(config).length: {config_size}`);
  
  async.forEachOf(config, function (size, key, cb) {
	const MIN = size["min"];
	const MAX = size["max"];
	const sizeName = size["name"];
	console.log("Size name : " + sizeName + " " + MIN + " " + size["max"]);
  
  	const thumbFileName = `thumb_${sizeName}_${fileName}`; // thumb__small_example.jpg
  	const thumbDir = `${sizeName}/`;
  	const thumbFilePath = path.join(thumbDir, thumbFileName);   // thumb/small/thumb_small_example.jpg
  
  	const originFile = imgBucket.file(filePath);  // {}
  	const thumbFile = thumbBucket.file(thumbFilePath);  //  {}
  
  	const transformer = sharp();
  	transformer
  		.resize(MIN, MAX)
    	.max();  // doesn't crop, keeps original shape
  
  	originFile.createReadStream()
    	.on('error', function(err) { console.log(`Error in ReadStream: ${err}`); return cb("Resize failed"); })
    	.on('end', function() { console.log("Origin file read successfully.") })
    	.pipe(transformer)
    	.pipe(thumbFile.createWriteStream({metadata}))
    	.on('error', function(err) { console.log(`Error in WriteStream: ${err} `) })
    	.on('finish', function() {console.log("Thumbnail created successfully."); cb(); });
  
  },
  function (err) {
	// After iterating through all the elements of the config object
	if (err) console.error(err.message);
	console.log("Done");
	callback();
	return;           
  });
};
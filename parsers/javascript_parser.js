let escodegen = require('escodegen');

let fs = require('fs');
let path = require('path');
const { PassThrough } = require('stream');
let filePath = path.join(__dirname, 'jsast.json');


fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
    if (!err) {
        console.log(escodegen.generate(JSON.parse(data)));
    
    
    } else {
        console.log(err);
    }
});

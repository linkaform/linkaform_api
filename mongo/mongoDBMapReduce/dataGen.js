var mongojs = require('mongojs');
var db = mongojs('mapReduceDB', ['sourceData']);
var fs = require('fs');
var dummyjson = require('dummy-json');

var helpers = {
  numb: function(){
	var number = Math.random() *100;
	return Math.floor(number,1);
},
  salary: function(){
        var number = Math.random() *10000;
        return Math.round(number)
},
  gender: function() {
    return ""+ Math.random() > 0.5 ? 'male' : 'female';
  },
  dob : function() {
	var start = new Date(1900, 0, 1),
		end = new Date();
		return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
	},
  hobbies : function () {
  	var hobbysList = [];
  	hobbysList[0] = [];
  	hobbysList[0][0] = ["Acrobatics", "Meditation", "Music"];
  	hobbysList[0][1] = ["Acrobatics", "Photography", "Papier-Mache"];
  	hobbysList[0][2] = [ "Papier-Mache"];
  	return hobbysList[0][Math.floor(Math.random() * hobbysList[0].length)];
  }
};

console.log("Begin Parsing >>");

var template = fs.readFileSync('template.hbs', {encoding: 'utf8'});
var result = dummyjson.parse(template, {helpers: helpers});

console.log("Begin Database Insert >>");

db.sourceData.remove(function (argument) {
	console.log("DB Cleanup Completd");
});
console.log('pass')
db.sourceData.insert(JSON.parse(result), function (err, docs) {
	console.log("DB Insert Completed");
});

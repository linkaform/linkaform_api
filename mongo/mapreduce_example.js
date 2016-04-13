var mongojs = require('mongojs')
var db = mongojs('mydb')
var mycollection = db.collection('mycollection')




var mongojs = require('mongojs');
var db = mongojs('mapReduceDB', ['sourceData']);
var fs = require('fs');
var dummyjson = require('dummy-json');

var helpers = {
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

db.sourceData.insert(JSON.parse(result), function (err, docs) {
	console.log("DB Insert Completed");
});


var mapper = function () {
	emit(this.answers ;, 1);

 db.runCommand({
    mapReduce: "form_answer",
    map: function(){
        var granja = this.answers ;
        var fecha  = granja['000000000000000000000001'];
        var name  = granja['000000000000000000000002'];
        var group = granja['56d0dd1023d3fd54b8eaafcf'];
        var cerdos = granja['276000000000000000000006'];
        var x = {granja:name, group:group, cerdos: cerdos}
        emit(fecha , 5);
    },
    reduce : function(granja, counters) {
        count += 0;
        for (var index = 0; index < counters.lenght; ++index) {
            count += counters[index];
        }
        return count;
    },
    out : {inline:1},
    query : {'answers.000000000000000000000002' : {$ne : null},'form_id'  : {$in:[4706,2760,2754,4886]}},
})



var mapper = function () {
	emit(this.gender, 1);
};

var mapper = function () {
	emit(this.work, 1);
};

var reducer = function(gender, count){
 	return Array.sum(count);
};
rs.slaveOk()
use infosync_answers_client_414

var emit = function(key, value) {
    print("emit");
    print("key: " + key + "  value: " + tojson(value));
}

var mapper =  function(){
    var granja = this.answers ;
    var fecha  = granja['000000000000000000000001'];
    var name  = granja['000000000000000000000002'];
    var group = granja['56d0dd1023d3fd54b8eaafcf'];
    var lote = granja['276000000000000000000005']
    var cerdos = granja['276000000000000000000006'];
    var x = {granja:name, group:group, cerdos: cerdos ,lote: lote}
    emit(fecha , x);
}



db.sourceData.mapReduce(
	mapper,
	reducer,
	{
		out : "example2_results"
	}
 );


 {
'fecha':'2016-01-01',
'semana':53,
'granja':'18_de_marzo_a',
'inventario':670
}

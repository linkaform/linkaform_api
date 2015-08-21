var conn = new Mongo();
var db = conn.getDB("infosync_answers_client_9");
var records = db.form_answer.find({"form_id": 6});

var mapFunction = function(records){
for(var i = 0; i < records.count(); i++){
var record = records[i];
var form = record.voucher;
var dictionary = {};
for(var j in form.fields){
var field = form.fields[j];
dictionary[field.field_id.id] = field.label;
}

var new_answers = {};
for(var key in record.answers){
new_answers[dictionary[key]] = record.answers[key];
}
record.answers = new_answers;
}
return records;
}	

var new_records = mapFunction(records);

db.createCollection('new_form_answer');
for(var i = 0; i < new_records.count(); i++){
var new_record = new_records[i];
db.new_form_answer.insert(new_record);
}

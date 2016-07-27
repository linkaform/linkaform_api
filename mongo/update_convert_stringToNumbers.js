//db.form_answer.find({ 'voucher.fields.field_type':{$in:['integer', 'decimal']}},
use admin
db = db.getSiblingDB("admin");
dbs = runCommand( { listDatabases: 1 } ).databases
dbs.forEach(function (database) {
  print ("db=" + database.name);
  db = db.getSiblingDB(database.name)
  db.form_answer.find({created_at: {$gt:ISODate("2015-06-15")}, 'voucher.fields.field_type':{$in:['integer', 'decimal']}},
  {created_at:1, 'voucher.fields':1, 'answers':1}).forEach(function(form_data) {
    //busco que id tiene cada cambpo que es integer o decimal
    var fields = form_data.voucher['fields']
    var num_fields_list = []
    for (i=0; i < fields.length; i++){
      ttype = fields[i].field_type
      //print(ttype)
      if (ttype == 'integer' || ttype == 'decimal'){
            field_id = fields[i].field_id['id']
            num_fields_list.push(field_id)
      }
    }
    //print('num_fields_list=' + num_fields_list)
    var new_answer = {}
    var has_strings = false
    for (x=0; x < num_fields_list.length; x++){
      res_number = form_data.answers[num_fields_list[x]]
      //print('res_number=' + res_number)
      if (typeof res_number == "string"){
      //if (typeof res_number == "number"){
        has_strings = true
        //print('answer' + res_number)
        new_answer['answers.' + num_fields_list[x]] = parseFloat(res_number)
        //new_answer['answers.' + num_fields_list[x]] = '' + res_number
      }
    }
    if (has_strings == true){
      print('Updating Record: ' + form_data._id)
      db.form_answer.update({_id:form_data._id},{$set:new_answer})
  }
  })
})

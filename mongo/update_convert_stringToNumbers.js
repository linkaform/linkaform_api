//db.form_answer.find({ 'voucher.fields.field_type':{$in:['integer', 'decimal']}},
//use admin
db = db.getSiblingDB("admin");
dbs = db.runCommand( { listDatabases: 1 } ).databases;
dbs.forEach(function (database) {
    print ("db=" + database.name);
    db = db.getSiblingDB(database.name)
    db.form_answer.find({deleted_at:{$exists:0}, 'voucher.fields.field_type':{$in:['integer', 'decimal']}},
      {created_at:1, 'voucher.fields':1, 'answers':1,'folio':1}).forEach(function(form_data) {
      var fields = form_data.voucher['fields']
      var num_fields_list = []
      var group_fields_dict = {}
      var group_fields_list = []
      var group_id_list = []
      for (i=0; i < fields.length; i++){
          ttype = fields[i].field_type
          if (ttype == 'integer' || ttype == 'decimal'){
            field_id = fields[i].field_id['id']
            if(fields[i].group != undefined){
              var group_id = fields[i].group.group_id.id
              if (group_id){
                  if(group_fields_list.indexOf(group_id) == -1){
                      group_fields_list.push(group_id)
                      group_fields_dict[group_id] = []
                    }
                  if(group_fields_dict[group_id] == undefined){
                    group_fields_dict[group_id] = [field_id]
                  }
                  else { group_fields_dict[group_id].push(field_id)}
                  } 
              else{
                 }
            }  
            num_fields_list.push(field_id)
          }
      }
      var new_answer = {}
      var has_strings = false
      var group_string = false
      var has_answer = false
      var has_group_answer = false
      for (i =0; i<num_fields_list.length; i++ ) {
         if(num_fields_list[i] in form_data.answers){
            has_answer = true
         }
      }
      for (a =0; a<group_fields_list.length; a++ ) {
         if(group_fields_list[a] in form_data.answers){
            if(form_data.answers[group_fields_list[a]].length > 0){
              has_group_answer = true
            }
         }
      }
      if(has_answer){
          for (x=0; x < num_fields_list.length; x++){
              res_number = form_data.answers[num_fields_list[x]]
              if (typeof res_number == "string"){
                has_strings = true
                new_answer['answers.' + num_fields_list[x]] = parseFloat(res_number)
              }
          }
      }
      if(has_group_answer){
          for (y=0; y < group_fields_list.length; y++){
              ans_group_list = form_data.answers[group_fields_list[y]]
              var g_new_answer_list = []
              group_string = false
              if(ans_group_list != undefined){
                for(z=0; z < ans_group_list.length; z++){
                    var agl = ans_group_list[z]
                    var g_new_answer = agl
                    for(w=0; w < group_fields_dict[group_fields_list[y]].length; w++){
                        group_field_id = group_fields_dict[group_fields_list[y]][w]
                        res_number = agl[group_field_id]
                        if (typeof res_number == "string"){
                            group_string = true
                            has_strings = true
                            g_new_answer[group_field_id] = parseFloat(res_number)
                        }
                    }
                    g_new_answer_list.push(g_new_answer)
                }
              }
              if(group_string == true){
                  new_answer['answers.' + group_fields_list[y]] = g_new_answer_list
                }
            }
    }
      if (has_strings == true){
          print('folio: ' + form_data.folio)
          print('Updating Record: ' + form_data._id)
          //db.form_answer.update({_id:form_data._id},{$set:new_answer})
      }
    })
})

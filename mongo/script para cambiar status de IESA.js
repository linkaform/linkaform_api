



db.form_answer.find({'answers.f1054000a010000000000002':'Tacubaya','deleted_at':{'$exists':0}}).forEach(function(data) {
    print(data.answers['f1054000a010000000000002'])
    db.form_answer.update({_id:data._id},{$set:{'answers.f1054000a010000000000002':'tacubaya'}})
    db.form_answer.update({_id:data._id},{$set:{'voucher':vv}})
})

db.form_answer.find({'answers.f1054000a010000000000002':'azorez','deleted_at':{'$exists':0}}).forEach(function(data) {
    print(data.answers['f1054000a010000000000002'])
    db.form_answer.update({_id:data._id},{$set:{'answers.f1054000a010000000000002':'azores'}})
    db.form_answer.update({_id:data._id},{$set:{'voucher':vv}})
})



db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'cotizando'}).forEach(function(data) {
    print(data.answers['555f6a9f01a4de47e4a9364d'])
    db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'evaluacion_/_compra'}});
})
db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'cotización_enviada'}).forEach(function(data) {
    print(data.answers['555f6a9f01a4de47e4a9364d'])
    db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'enlace_con_distribuidor'}});
})
db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'vendido'}).forEach(function(data) {
  print(data.answers['555f6a9f01a4de47e4a9364d'])
  db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'compra'}});
})
db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'compro_otra_marca'}).forEach(function(data) {
    print(data.answers['555f6a9f01a4de47e4a9364d'])
    db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'perdido'}});
})
db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'nunca_contesto'}).forEach(function(data) {
    print(data.answers['555f6a9f01a4de47e4a9364d'])
    db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'perdido'}});
})
db.form_answer.find({'answers.555f6a9f01a4de47e4a9364d':'cambio_de_rep'}).forEach(function(data) {
    print(data.answers['555f6a9f01a4de47e4a9364d'])
    db.form_answer.update({_id:data._id},{$set:{'answers.555f6a9f01a4de47e4a9364d':'cerrado'}});
})


###esto es para cambiar el folio mal capturador
db.form_answer.find({'answers.00000000000000000000a099':{$exists:1}},{answers:1,folio:1}).forEach(function(data) {
    var ref_folio = data.answers['00000000000000000000a099']
    if (ref_folio.length == 8){
      ref_folio = ref_folio.slice(0,6)
    }
    if (ref_folio.length == 6){
      ref_folio = ref_folio + '-96'
    }
    print('ref: ' + data.answers['00000000000000000000a099'])
    print ('new folio: ' + ref_folio )
    db.form_answer.update({_id:data._id},{$set:{'answers.00000000000000000000a099':ref_folio}});
  })

#para cambiar la referencia del folio y el folio mismo
db.form_answer.find({'answers.00000000000000000000a099':{$exists:1}},{answers:1,folio:1}).forEach(function(data) {
    var ref_folio = data.answers['00000000000000000000a099']
    if (ref_folio.length == 8){
      ref_folio = ref_folio.slice(0,6)
    }
    if (ref_folio.length == 6){
      ref_folio = ref_folio + '-96'
    }
    doc2 = db.form_answer.findOne({'folio':ref_folio, 'form_id': 5477},{'folio':1});
    if (doc2 == null){
      print('ref: ' + data.answers['00000000000000000000a099'])
      print('folio: ' + data.folio)
      print('---- update folio -----')
      db.form_answer.update({_id:data._id},{$set:{'answers.00000000000000000000a099':ref_folio, 'folio':ref_folio}});
    }
    else{
      db.form_answer.update({_id:data._id},{$set:{'answers.00000000000000000000a099':ref_folio}});
    }
  })
  print('new folio' + folio)

  print('folio' + folio)

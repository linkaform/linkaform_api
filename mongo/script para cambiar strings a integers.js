



db.form_answer.find({form_id:3406, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['5589a03701a4de7bba84fb32'])
    db.form_answer.update({_id:data._id},{$set:{'answers. ':parseInt(data.answers['5589a03701a4de7bba84fb32'])}});
})

db.form_answer.find({form_id:3407, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['5589a09c01a4de7bba84fb50'])
    db.form_answer.update({_id:data._id},{$set:{'answers.5589a09c01a4de7bba84fb50':parseInt(data.answers['5589a09c01a4de7bba84fb50'])}});
})

db.form_answer.find({form_id:3408, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['5589a0bc01a4de7bba84fb58'])
    db.form_answer.update({_id:data._id},{$set:{'answers.5589a0bc01a4de7bba84fb58':parseInt(data.answers['5589a0bc01a4de7bba84fb58'])}});
})

db.form_answer.find({form_id:2667, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552fdbf501a4de288f4275ee'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552fdbf501a4de288f4275ee':parseInt(data.answers['552fdbf501a4de288f4275ee'])}});
})

db.form_answer.find({form_id:2654, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552fc75201a4de2890055381'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552fc75201a4de2890055381':parseInt(data.answers['552fc75201a4de2890055381'])}});
})

db.form_answer.find({form_id:2650, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552fc35b01a4de288f4275d5'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552fc35b01a4de288f4275d5':parseInt(data.answers['552fc35b01a4de288f4275d5'])}});
})

db.form_answer.find({form_id:2638, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552e89ae01a4de288eebef38'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552e89ae01a4de288eebef38':parseInt(data.answers['552e89ae01a4de288eebef38'])}});
})

db.form_answer.find({form_id:2639, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552e89da01a4de28900552f3'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552e89da01a4de28900552f3':parseInt(data.answers['552e89da01a4de28900552f3'])}});
})

db.form_answer.find({form_id:3398, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['55899c9401a4de2ea94629ea'])
    db.form_answer.update({_id:data._id},{$set:{'answers.55899c9401a4de2ea94629ea':parseInt(data.answers['55899c9401a4de2ea94629ea'])}});
})

db.form_answer.find({form_id:3399, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['55899ce801a4de2ea94629f7'])
    db.form_answer.update({_id:data._id},{$set:{'answers.55899ce801a4de2ea94629f7':parseInt(data.answers['55899ce801a4de2ea94629f7'])}});
})

db.form_answer.find({form_id:2652, deleted_at: {$exists:0}, connection_id:126}).forEach(function(data) {
    print(data.answers['552fc36801a4de2890055369'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552fc36801a4de2890055369':parseInt(data.answers['552fc36801a4de2890055369'])}});
})

///// Cambiar granja
use infosync_answers_client_414
db.form_answer.find({form_id:2667, 'answers.552fdbf501a4de288f4275e9':'ermita'}).count()
db.form_answer.find({form_id:2667, deleted_at: {$exists:0}}).forEach(function(data) {
    print(data.answers['552fdbf501a4de288f4275e9'])
    db.form_answer.update({_id:data._id},{$set:{'answers.552fdbf501a4de288f4275e9':'ermita'}});
})
db.form_answer.find({form_id:2667, 'answers.552fdbf501a4de288f4275e9':'ermita'}).count()
db.form_answer.find({form_id:5857 ,deleted_at: {$exists:0}, 'answers.5696e5af23d3fd3face97f0b':'viboras'},{answers:1}).count()
db.form_answer.find({form_id:5857, deleted_at: {$exists:0}}).forEach(function(data) {
    print(data.answers['5696e5af23d3fd3face97f0b'])
    db.form_answer.update({_id:data._id},{$set:{'answers.5696e5af23d3fd3face97f0b' : 'viboras_184'}});
})
db.form_answer.find({form_id:5857 ,deleted_at: {$exists:0}, 'answers.5696e5af23d3fd3face97f0b':'viboras'},{answers:1}).count()


//mandar a 0 todo los registros con id raro
db.form_answer.find(
  {form_id:2714,
  deleted_at:{$exists:0}},
  {'answers.553904c201a4de236a68ac97':1,'answers.553904c201a4de236a68ac97.5538265701a4de236b938e96':1})

db.form_answer.find(    {form_id:2714,
  //  'answers.553904c201a4de236a68ac95':"2016-01-25",
    'answers.553904c201a4de236a68ac96':'liebres' ,
    deleted_at:{$exists:0}},
     {'answers.553904c201a4de236a68ac97.553904c201a4de236a68ac99':1,
     'answers.553904c201a4de236a68ac97.5538265701a4de236b938e96':1})

//Quita el id 99 de las salidas de empaque
 use infosync_answers_client_414
 db.form_answer.find({form_id:2714, deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.553904c201a4de236a68ac99':{$exists:1}}).count()
 db.form_answer.find({form_id:2714, deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.5538265701a4de236b938e96':{$exists:1}}).forEach(function(data) {
     var group =  data.answers['553904c201a4de236a68ac97'];
     for (i=0; i < group.length; i++){
       delete group[i]['5538265701a4de236b938e96'] ;
     }
     print('NEXT')
     data.answers['553904c201a4de236a68ac97'] = group
     db.form_answer.update({_id:data._id},{$set:{'answers.553904c201a4de236a68ac97':group}});
 })



 ObjectId("554a1b3001a4de043933205c")
5538265701a4de236b938e94


//Quita el id 96 de las salidas de empaque
use infosync_answers_client_414
db.form_answer.find({form_id:2714, folio:'205645-414' , deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.553904c201a4de236a68ac99':{$exists:1}}).count()
db.form_answer.find({form_id:2714,  deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.553904c201a4de236a68ac99':{$exists:1}}).forEach(function(data) {
    var group =  data.answers['553904c201a4de236a68ac97'];
    for (i=0; i < group.length; i++){
      delete group[i]['553904c201a4de236a68ac99'] ;
    }
    print('NEXT')
    data.answers['553904c201a4de236a68ac97'] = group
    db.form_answer.update({_id:data._id},{$set:{'answers.553904c201a4de236a68ac97':group}});
})

db.form_answer.find({form_id:2714, deleted_at:{$exists:0}}).count()
826
db.form_answer.find({form_id:2714, deleted_at:{$exists:0},
    'answers.553904c201a4de236a68ac95': {$exists:1},
    'answers.553904c201a4de236a68ac96': {$exists:1},
    'answers.553904c201a4de236a68ac97': {$exists:1}}).count()

435
db.form_answer.find({form_id:2714, deleted_at:{$exists:0},
    'answers.5538265701a4de236b938e87': {$exists:1},}).count()
    'answers.553904c201a4de236a68ac95': {$exists:1}}).count(),
    'answers.553904c201a4de236a68ac97': {$exists:1}}).count()

390
    //granja/5538265701a4de236b938e88
    //granja nueva 553904c201a4de236a68ac96

    { "_id" : ObjectId("554a1b3001a4de043933205c"),
    "answers" : { "5538265701a4de236b938e88" : "palomas_1",
      "5538265701a4de236b938e94" : [ { "5538265701a4de236b938e96" : 40, "5538265701a4de236b938e95" : "caja_360" },
      { "5538265701a4de236b938e96" : 50, "5538265701a4de236b938e95" : "separadores" },
      { "5538265701a4de236b938e96" : 2, "5538265701a4de236b938e95" : "paquetes_de_cono_jumbo" } ],
      "5538265701a4de236b938e98" : { "file_name" : "sign_2015_05_06_08_46_12.png", "file_url" : "uploads/414_jefatura.ti@sanfandila.com/2b74f79a8b43f70fd9017ceb1cfee490695511a1.png" },
      "5538265701a4de236b938e97" : "geras",
      "5538265701a4de236b938e87" : "2015-05-05" }, "folio" : "44580-414" }

'553904c201a4de236a68ac98'

5538265701a4de236b938e95:"paquetes_de_cono_jumbo"

db.form_answer.find({form_id:2714,  deleted_at:{$exists:0},'answers.5538265701a4de236b938e88': {$exists:1}}).count()
db.form_answer.find({form_id:2714, deleted_at:{$exists:0},'answers.5538265701a4de236b938e87': {$exists:1}}).forEach(function(data) {
    print('respuesta' +  data.answers)
    print('campo' + data.answers['5538265701a4de236b938e88'])
    data.answers['553904c201a4de236a68ac96'] =  data.answers['5538265701a4de236b938e88']
    data.answers['553904c201a4de236a68ac95'] = data.answers['5538265701a4de236b938e87']
    data.answers['553904c201a4de236a68ac97'] = data.answers['5538265701a4de236b938e94']
    var group =  data.answers['553904c201a4de236a68ac97'];
    for (i=0; i < group.length; i++){
      group[i]['553904c201a4de236a68ac98'] = group[i]['5538265701a4de236b938e95'] ;
      delete group[i]['5538265701a4de236b938e95']
    }
    data.answers['553904c201a4de236a68ac97'] = group
    delete  data.answers['5538265701a4de236b938e87']
    delete data.answers['5538265701a4de236b938e94']
    delete data.answers['5538265701a4de236b938e88']
    db.form_answer.update({_id:data._id},{$set:{'answers':data.answers}});
    print('NEXT')
})

    data.answers['553904c201a4de236a68ac97'] = group

db.form_answer.find({form_id:2714,  "folio" : "44580-414", deleted_at:{$exists:0},}).forEach(function(data) {
    print('respuesta' +  data.answers)
    print('campo' + data.answers['5538265701a4de236b938e88'])
    data.answers['553904c201a4de236a68ac97'] = data.answers['553904c201a4de236a68ac97']
    var group =  data.answers['553904c201a4de236a68ac97'];
    for (i=0; i < group.length; i++){
      group[i]['553904c201a4de236a68ac98'] = group[i]['5538265701a4de236b938e95'] ;
      delete group[i]['5538265701a4de236b938e95']
    }
    db.form_answer.update({_id:data._id},{$set:{'answers.553904c201a4de236a68ac97':group}});
    print('NEXT')
})
    data.answers['553904c201a4de236a68ac97'] = group

var vv = db.form_answer.find({form_id:2714,  "folio" : "289522-414", deleted_at:{$exists:0},}, {voucher:1})
db.form_answer.find({form_id:2714,  "folio" : "289522-414", deleted_at:{$exists:0},}).forEach(function(data) {
  var vv = db.form_answer.find({form_id:2714,  "folio" : "289522-414", deleted_at:{$exists:0},}, {voucher:1})
  voucher2 = data.voucher
  print('voucher' + vv)
})

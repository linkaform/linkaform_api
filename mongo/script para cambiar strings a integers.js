



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

//Quita el id 99 de las salids de empaque
 use infosync_answers_client_414
 db.form_answer.find({form_id:2725, deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.5538265701a4de236b938e96':{$exists:1}}).count()
 db.form_answer.find({form_id:2725, deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.5538265701a4de236b938e96':{$exists:1}}).forEach(function(data) {
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


//Quita el id 99 de las recepcion de empaque
use infosync_answers_client_414
db.form_answer.find({form_id:2714, deleted_at:{$exists:0},'answers.553904c201a4de236a68ac97.553904c201a4de236a68ac99':{$exists:1}}).count()
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



    print('STARTING' + new_answer)
##quita los nulls
db.form_answer.find({deleted_at:{$exists:0},form_id:6015 }, {answers:1}).count()
db.form_answer.find({deleted_at:{$exists:0}, form_id:6016, folio:'298541-126'}, {answers:1}).forEach(function(data) {
    var new_answer =  {};
    doc2 = db.form_answer.findOne({_id:data['_id']});
    print('_id:' + data['_id']);
    for (key in doc2['answers']) {
        print('type of: ' + typeof data.answers[key])
        if (data.answers[key] == null ){
          delete data.answers[key]
        }
        else if (typeof data.answers[key] != 'object'){
          new_answer[key] = data.answers[key]
        }
        if (typeof data.answers[key] == 'object' ){
          print('answer    ' +  data.answers[key])
          print('key: ' + key)
          new_answer[key] = []
          for (i=0; i < doc2['answers'][key].length; i++ ){
            var group_empty = true;
            print('------------------------ ' +  i)
            var new_group_answer = {}
            for (key_group in doc2['answers'][key][i]) {
                print(' reading key : ' + key_group )
                print('answer: ' + doc2['answers'][key][i][key_group])
                if (doc2['answers'][key][i][key_group] != null && doc2['answers'][key][i][key_group] != true ){
                  print('adding answer')
                  group_empty = false;
                  new_group_answer[key_group] = doc2['answers'][key][i][key_group];
                }
              }
            if (group_empty == false){
              print('pushing group: ' + i)
              new_answer[key].push(new_group_answer)
            }
          }
        }
      }
    db.form_answer.update({_id:data['_id']},{$set:{'answers':new_answer}});
    print('NEXT')
})
    for (i=0; i < data.answers.length; i++){
      print('answer number : ' + i)
      print('res + ' + data.answers[i])
    }
    data.answers['553904c201a4de236a68ac97'] = group
    db.form_answer.update({_id:data._id},{$set:{'answers.553904c201a4de236a68ac97':group}});



db = db.getSiblingDB("admin");
dbs = db.runCommand( { listDatabases: 1 } ).databases;
dbs.forEach(function (database) {
    print ("db=" + database.name);
    db = db.getSiblingDB(database.name)
    db.form_answer.aggregate([
      {$match:{deleted_at:{$exists:0}, folio:{$exists:1}, form_id:{$exists:1}}},
      {$group: {
        _id:{
          folio:'$folio',
          form_id:'$form_id'
      },
        cant :{$sum:1}},
      },
      {$match:{'cant':{$gte:2}}}
      ]).forEach(function(data) {
        print(JSON.stringify(data))
    })
})


db = db.getSiblingDB("admin");
dbs = db.runCommand( { listDatabases: 1 } ).databases;
dbs.forEach(function (database) {
    print ("db=" + database.name);
    db = db.getSiblingDB(database.name)
    db.form_answer.find({'properties.followers':{$exists:0},deleted_at:{$exists:0}}).forEach(function(data) {
      followers = []
      if ( data.user_id !== undefined ) followers.push(data.user_id)
      if ( data.connection_id !== undefined && data.connection_id != data.user_id) followers.push(data.connection_id)
      var properties2 = {'followers':followers}
      print(JSON.stringify(properties2))
      db.form_answer.update({_id:data._id},{$set:{properties:properties2}})
   })
  })
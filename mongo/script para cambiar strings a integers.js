



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

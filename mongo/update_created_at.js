

/*Busca registros de Logistorage que tengan fecha mayor a 2017-01-01
y mes de Diciebre y actualiza poniendo fecha 2016-12-21
*/

use infosync_answers_client_516

db.form_answer.find({'answers.559174f601a4de7bb94f87ed':'diciembre','created_at': {$gte:ISODate('2017-01-01')}}).forEach(function(data) {
    print('folio: ' + data.folio + '| Fecha Captura: ' + data.created_at )
    db.form_answer.update({_id:data._id},{$set:{'created_at':ISODate('2016-12-31')}})
  })

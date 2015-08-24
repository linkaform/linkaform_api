var conn = new Mongo();
var now = new Date();

/* Get list of databases */
var dbList = db.adminCommand('listDatabases');
for(var i in dbList.databases) {
	/* Get current database name and connection */
	var dbName = dbList.databases[i].name;
	var db = conn.getDB(dbName);

	/* Check if form_answer collection exists */
	var collectionExists = db.system.namespaces.find( { name: dbName + '.form_answer' } );
	if(collectionExists) {

		/* Loop through every record */
		var records = db.form_answer.find();
		for(var i = 0; i < records.count(); i++){
			var record = records[i];
			var dateFieldIds = [];

			/* Check which fields are dates or datetimes */
			if(record.voucher && record.voucher.fields) {
				for(var j in record.voucher.fields) {
					var field = record.voucher.fields[j];
					if(['date', 'datetime'].indexOf(field.field_type) !== -1) {
						if(dateFieldIds.indexOf(field.field_id.id) === -1) {
							dateFieldIds.push(field.field_id.id);
						}
					}
				}
			} else {
				printjson(record.answers);
			}

			/* Update every answer of date and datetime fields */
			var answers = {};
			for(var j in dateFieldIds) {
				var fieldId = dateFieldIds[j];
				var actualAnswer = record.answers[fieldId];
				if(actualAnswer) {
					var newAnswer = new Date(actualAnswer);
					answers['answers.' + fieldId] = newAnswer;
				}
			}

			db.form_answer.update({_id: record._id}, { '$set': answers });
		}
	}
}

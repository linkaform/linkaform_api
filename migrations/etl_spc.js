var conn = new Mongo();
printjson(conn);
var now = new Date();

var db = conn.getDB('infosync_answers_client_126');

var orden_servicio = {

    /* Datos iniciales */
    '55e85d9f23d3fd0ca23d7908':'formato_servicio',
    '55e85d9f23d3fd0ca23d7907':'nombre_cliente',
    '55e85d9f23d3fd0ca23d790a':'fecha_servicio',
    '55e85d9f23d3fd0ca23d790c':'ruta_servicio',
    '55e85d9f23d3fd0ca23d790d':'precio_servicio',

    /* Tratamiento */
    '55e85d9f23d3fd0ca23d790f':'producto',
    '55e85d9f23d3fd0ca23d7915':'area',

    /* Cebaderos Roedores Exterior */
    '55e85d9f23d3fd0ca23d7919':'tipo_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791a':'numero_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791b':'condicion_dispositivo_ext',
    '55e85d9f23d3fd0ca23d791d':'accion_realizada_ext',
    '55e881dc23d3fd0ca0bdde64':'rata_ext',
    '55e881dc23d3fd0ca0bdde65':'raton_ext',
    '55e881dc23d3fd0ca0bdde66':'cucaracha_alemana_ext',
    '55e881dc23d3fd0ca0bdde67':'cucaracha_americana_ext',
    '55e881dc23d3fd0ca0bdde68':'hormiga_ext',
    '55e881dc23d3fd0ca0bdde69':'mosca_ext',
    '55e8bf7323d3fd685b7ff0cf':'palomilla_ext',
    '55e8bf7323d3fd685b7ff0d0':'gorgojo_ext',
    '55ee015723d3fd65cb47fbe2':'otra_ext',
    '55eef43f23d3fd6d6a65d4da':'descripcion_otra_ext',


    /* Trampas Mecanicas Roedor Interior */
    '55e85d9f23d3fd0ca23d7920':'tipo_dispositivo_int',
    '55e85d9f23d3fd0ca23d7921':'numero_dispositivos_int',
    '55e85d9f23d3fd0ca23d7922':'condicion_dispositivo_int',
    '55e85d9f23d3fd0ca23d7924':'accion_realizada_int',
    '55e85d9f23d3fd0ca23d7925':'rata_int',
    '55e8875323d3fd0ca1472827':'raton_int',
    '55e8875323d3fd0ca1472828':'cucaracha_alemana_int',
    '55e8875323d3fd0ca1472829':'cucaracha_americana_int',
    '55e889ea23d3fd0ca0bdde72':'hormiga_int',
    '55e8875323d3fd0ca147282a':'mosca_int',
    '55e8bfe923d3fd685de86e35':'palomilla_int',
    '55e8bfe923d3fd685de86e36':'gorgojo_int',
    '55ee065b23d3fd6d6a65d45d':'otra_int',
    '55eef47523d3fd6d69400649':'descripcion_otra_int',

    /* Trampas de Luz UV Voladores */
    '55e85d9f23d3fd0ca23d7927':'tipo_dispositivo_luz',
    '55e85d9f23d3fd0ca23d7928':'numero_dispositivo_luz',
    '55e85d9f23d3fd0ca23d7929':'condicion_dispositivo_luz',
    '55e85d9f23d3fd0ca23d792b':'accion_dispositivo_luz',
    '55e88ab323d3fd0ca23d79d8':'mosca_luz',
    '55e88ab323d3fd0ca23d79d6':'mosca_fruta_luz',
    '55e8cc0223d3fd685de86e53':'mosquita_drenaje_luz',
    '55e88ab323d3fd0ca23d79d9':'mosquito_luz',
    '55e88ab323d3fd0ca23d79da':'gorgojo_luz',
    '55e8c14f23d3fd685de86e37':'palomilla_luz',
    '55e88ab323d3fd0ca23d79db':'termita_luz',
    '55e88ab323d3fd0ca23d79d7':'hormiga_luz',
    '55ee06bf23d3fd6d6a65d460':'otra_luz',
    '55eef4a823d3fd6d6a65d4db':'descripcion_otra_luz',

    /* Trampas de Feromonas */
    '55e85d9f23d3fd0ca23d792e':'tipo_dispositivo_fer',
    '55e85d9f23d3fd0ca23d792f':'numero_dispositivo_fer',
    '55e85d9f23d3fd0ca23d7930':'condicion_dispositivo_fer',
    '55e85d9f23d3fd0ca23d7932':'accion_dispositivo_fer',
    '55e88c1123d3fd0ca147282d':'cucaracha_alemana_fer',
    '55e88c1123d3fd0ca1472830':'gorgojo_fer',
    '55e88c1123d3fd0ca147282e':'palomilla_fer',
    '55e88c1123d3fd0ca147282f':'mosca_fer',
    '55e8c2ce23d3fd685de86e38':'otra_fer',
    '55e8c2ce23d3fd685de86e39':'descripcion_otra_fer',

    /* Otras Trampas */
    '55e85d9f23d3fd0ca23d7935':'tipo_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7936':'numero_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7937':'condicion_dispositivo_otra',
    '55e85d9f23d3fd0ca23d7939':'accion_dispositivo_otra',
    '55e8c39e23d3fd685cc98b12':'cantidad_plaga_encontrada_otra',
    '55ee084c23d3fd6d6940061f':'descripcion_plaga_encontrada_otra',

    /* Acciones Correctivas */
    '55e85d9f23d3fd0ca23d793c':'categoria',
    '55e85d9f23d3fd0ca23d793d':'actividad_pendiente_hacer',
    '55e85d9f23d3fd0ca23d793e':'accion_realizar_parte',
    '55e85d9f23d3fd0ca23d793f':'fecha_compromiso_terminar',
    '55e85d9f23d3fd0ca23d7940':'estatus',
    '55e88f5923d3fd0ca1472836':'fecha_realizado',

    /* Comprobante de Servicio */
    '55e85d9f23d3fd0ca23d7941':'nombre_tecnico',
    '55e85d9f23d3fd0ca23d7943':'nombre_cliente'
    
};

/* Check if form_answer collection exists */
var collectionExists = db.system.namespaces.find( { name: db + '.form_answer' } );
if(collectionExists) {
    /* Loop through every record */
    var records = db.form_answer.find({form_id:{$in:[4534, 4535, 4536]}});
    for(var i = 0; i < records.count(); i++) {
	var record = records[i];
	var dateFieldIds = [];
	printjson(record);
    }
/*
    

    Check which fields are dates or datetimes
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
	
	 Update every answer of date and datetime fields
	var answers = {};
	for(var j in dateFieldIds) {
	    var fieldId = dateFieldIds[j];
	    var actualAnswer = record.answers[fieldId];
	    if(actualAnswer) {
		var newAnswer = new Date(actualAnswer);
		answers['answers.' + fieldId] = newAnswer;
		print(answers['answers.' + fieldId]);
	    }
	}
	db.form_answer.update({_id: record._id}, { '$set': answers });
    }
	*/
}


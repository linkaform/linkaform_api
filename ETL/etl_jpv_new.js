/*
Lista de formas a usar en el ETL
Cada entrada es un diccionario con:
 - id: id del item de la forma
 - user_id: creador de la forma
 - filters: lista de filtros 
*/
var items = [
    { id: 2008, user_id: 126, filters: [] }
];


function get_answer(answer, field){
    // Formatear respuesta dependiendo del tipo de campo
    var field_id = field.field_id.id;
    if(answer){
        if(["geolocation", "signature", "image", "file"].indexOf(field.field_type) >= 0){
            return null;
        // Opcion multiple
        }else if(field.field_type == "checkbox"){
            var options = {}
            for(var i in field.options){
                var option = field.options[i];
                options[option.value] = option.label;
            }
            var new_answer = [];
            for(var i in answer){
                var value = answer[i];
                if(options[value]){
                    new_answer.push(options[value]);
                }
                else{
                    new_answer.push(value);
                }
            }
            return new_answer;
        // Radio
        }else if(field.field_type == "radio" || field.field_type == "select"){
            var options = {}
            for(var i in field.options){
                var option = field.options[i];
                options[option.value] = option.label;
            }
            if(options[answer]){
                return options[answer];
            }
            return answer;
        // Demas tipos
        }else{
            return answer;
        }
    }
    return null;
}


function etl(items){
    /* Aplicar ETL a los registros de cada forma */
    for(var i in items){
        var item = items[i];
        var conn = new Mongo();
        var db = conn.getDB("infosync_answers_client_" + item.user_id);
        db.createCollection('report_answer_new');
        
        var records = db.form_answer.find({form_id: item.id});
        for(var i = 0; i < records.count(); i++){
            var record = records[i];
            var fields = {};
            for(var j in record.voucher.form_pages){
                var page = record.voucher.form_pages[j];
                for(var k in page.page_fields){
                    var field = page.page_fields[k];
                    field.page = page.page_name;
                    fields[field.field_id.id] = field;
                }
            }
            var answers = {};
            var key_count = {};
            for(var field_id in record.answers){
                var answer = record.answers[field_id];
                var field = fields[field_id];
                var answer = get_answer(answer, field);
                var label = field.label.replace(".", "");
                if(!(label in key_count)){
                    key_count[label] = 0;
                }
                key_count[label] += 1;

                if(answer){
                    if(key_count[label] > 1){
                        answers[label + "_" + key_count[label]] = answer;
                    }else{
                        answers[label] = answer;
                    }
                }

            }
            var report = record;
            report.answers = answers;
            delete report.voucher;
            db.report_answer_new.update({_id: report._id}, report, { upsert: true });
        }
    } 
}

etl(items);



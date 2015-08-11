var conn = new Mongo();
var db = conn.getDB("infosync");

var formOrigin = db.form_data.findOne({ form_id: 3509});
var formsDestIds = [3484, 3483, 3470, 3468, 3461, 3465,
    3464, 3467, 3463, 3456, 3466, 3459, 3454, 3469, 3458,
    3453, 3462, 3451, 3457, 3450, 3455, 3449, 3460, 3452,
    3428, 3431];

for(var index in formsDestIds){
    var currentFormId = formsDestIds[index];
    db.form_data.update({
        form_id: currentFormId
    },
    {
        "$set": {
            fields: formOrigin.fields,
            form_pages: formOrigin.form_pages
        }
    });
}


var db_list = db.adminCommand('listDatabases');
var oneday = 24 * 60 * 60;
var date = ISODate("2015-01-01T00:00:00.408Z");
var ids = [];
for(var i in db_list["databases"]){
    var db_name = db_list["databases"][i]["name"];
    var conn = new Mongo();
    var db = conn.getDB(db_name);
    var collection_exists = db.system.namespaces.find( { name: db_name+'.form_answer' } );
    if(collection_exists){
        var record_count = db.form_answer.find({
            "created_at": { "$gte": date }
        }).count();
        if(record_count > 0){
            var strings = db_name.split("_");
            ids.push(strings[strings.length - 1]);
        }
    }
}

print("SELECT username, first_name FROM users_customuser where id in ("+ids+");");

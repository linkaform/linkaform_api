var host = 'localhost';
var port = '27017';
var client = 'infosync_answers_client_414';
var collection = 'form_answers';

function get_user_conn(host, port, client){
    conn = new Mongo();
    db = conn.getDB(client);
    return db;
}

var db = get_user_conn(host, port, client);
var result = db[collection].aggregate([{$group:{_id:{'week':{$week:'$created_at'}}}}, {$sort:{'_id.week':-1}}]);
printjson(result);



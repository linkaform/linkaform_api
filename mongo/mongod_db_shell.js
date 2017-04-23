db.createRole({
 role: 'mongodb',
 privileges:[{ resource: { cluster: true }, actions: [ "serverStatus" ] },
 { resource: { db:'', collection:''},{actions:["insert", "dbStats", "collStats", "compact","read","find", "update"]}],
 roles:[]
 })

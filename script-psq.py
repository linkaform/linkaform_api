import psycopg2
import uuid
"""
 Regresa un archivo para poderlo importar en la base de datos.
"""
conn = psycopg2.connect("dbname='infosync'")
cur = conn.cursor()

get_licenses = "select * from plans_license;"

get_ids = "select id, parent_id from users_customuser order by parent_id, id;"

def put_license(owner_id, user_id, uu_id):
	query =  "insert into plans_license (owner_id, user_id, token, expiration, is_active, plan_id)\
	 VALUES ({ow_id},{us_id},'{uu_id}', '2014-10-01 00:00:00', True, 1);\n".format(ow_id=owner_id,us_id=user_id,uu_id=uu_id)
		
	print ' query', query
	return True

cur.execute(get_ids)

rows = cur.fetchall()
with open("Output.txt", "w") as text_file:
	for row in rows:
		if row[1] == None:
			query =  "insert into plans_license (owner_id, user_id, token, expiration, is_active, plan_id)\
	 VALUES ({ow_id},{us_id},'{uu_id}', '2014-10-01 00:00:00', True, 1);\n".format(ow_id=row[0],us_id=row[0],uu_id=str(uuid.uuid4()))
			#put_license(row[0],row[0],str(uuid.uuid4()))
		else:
			query =  "insert into plans_license (owner_id, user_id, token, expiration, is_active, plan_id)\
	 VALUES ({ow_id},{us_id},'{uu_id}', '2014-10-01 00:00:00', True, 1);\n".format(ow_id=row[1],us_id=row[0],uu_id=str(uuid.uuid4()))
		cur.execute(query)
		cur.execute('commit')
			#put_license(row[1],row[0],str(uuid.uuid4()))

#delete from plans_license;
#psql -d infosync -f Output.txt 
#select id, parent_id from users_customuser order by parent_id, id;

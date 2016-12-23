test = {
	"phone": "4611249680",
	"name": "Age team",
	"email": "gerentebasico@hotmail.com"
}


conekta_client_token = conekta.Customer.create(test)

from account.openerp_api_for_infosync import create_company


test = {'name': " comapanyname",
        'parent_user_id':19999,
        'conekta_client_token':None
}

create_company(test)




db.form_answer.aggregate(
					[{'form_id': {'$in': [10540]}, 'deleted_at' : {'$exists':false}, 'answers.f1054000a030000000000002': 'liquidada'}])
					{"$group": {
					"_id": {
									 'cope':1 "$answers.f1054000a010000000000002",
									 },
					"folioPisa": "$answers.f1054000a010000000000001",
					"folioPisaPlex": "$answers.f1054000a010000000000006",
					"telefono": "$answers.f1054000a010000000000005",
					"materiales": "$answers.f1054000a020000100000005",
					}}
					])

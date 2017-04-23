#coding: utf-8

def get_query():
    query = [
     {'$match':{
        "itype" : "rent",
       "fixed_rent": {'$exists':True}
       }},
      {'$group':{
            '_id': {
                'currency' : "$fixed_rent.currency",
                'client': "$5591627901a4de7bb8eb1ad5",
                'warehouse': "$5591627901a4de7bb8eb1ad4",
                'year': {'$year':"$created_at"},
                'month': {'$month':"$created_at"}

            },
            'total_fixed_rent' : {'$sum':"$fixed_rent.unit_price"},
            'total_office_rent':{'$sum':0.0},
            'total_services': {'$sum': 0.0},
            'total_space_unit' : {'$sum': 0.0}

        }},
        ]
    return query

#coding: utf-8

def get_query():
    query =[
      {'$match':{
            "itype" : "rent",
            "office_rent": {'$exists':True}
        }},
      {'$group':{
            '_id': {
                'currency' : "$office_rent.currency",
                'client': "$5591627901a4de7bb8eb1ad5",
                'warehouse': "$5591627901a4de7bb8eb1ad4",
                'year': {'$year':"$created_at"},
                'month': {'$month':"$created_at"}

            },
            'total_office_rent' : {'$sum':"$office_rent.unit_price"},
            'total_fixed_rent':0.0,
            'total_services': 0.0,
            'total_space_unit' : 0.0
        }},
        ]
    return query

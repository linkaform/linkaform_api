#coding: utf-8

def get_query():
    query =

    db.report_answer.aggregate([
      {'$match':{
            "itype" : "rent",
            '5591627901a4de7bb8eb1ad5':'PLENLIFE',
            '5591627901a4de7bb8eb1ad4':'Monterrey',
            "office_rent": {'$exists':true},
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
        }},
        ]
    return query

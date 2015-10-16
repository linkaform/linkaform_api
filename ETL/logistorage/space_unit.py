#coding: utf-8

def get_query():
    query = [
      {'$match':{
          'itype' : 'space_unit',
        }},
        {'$group':{
            '_id': {
                'currency' : '$558d685701a4de7bba85289f.currency',
                'client': '$5591627901a4de7bb8eb1ad5',
                'warehouse': '$5591627901a4de7bb8eb1ad4',
                'year': {'$year':'$55b7f41623d3fd41daa1c414'},
                'month': {'$month':'$55b7f41623d3fd41daa1c414'}
            },
            'UE_avg' : {'$avg':'$558d685701a4de7bba85289f.qty'},
            'UE_unit_price' : {'$max':'$558d685701a4de7bba85289f.unit_price'},
            'UE_operator': {'$first':'$558d685701a4de7bba85289f.condition.operator'},
            'UE_agreed': {'$max':'$558d685701a4de7bba85289f.condition.qty'},
            'UE_extra_price': {'$max':'$558d685701a4de7bba85289f.extra_price'},
            'fixed_rent' : { '$max' : '$558d685701a4de7bba85289f.fixed_rent' },

            'UEP_avg' : {'$avg':'$55a010c323d3fd2994ab74e8.qty'},
            'UEP_unit_price' : {'$max':'$55a010c323d3fd2994ab74e8.unit_price'},

            'UEE_avg' : {'$avg':'$55a010c323d3fd2994ab74e9.qty'},
            'UEE_unit_price' : {'$max':'$55a010c323d3fd2994ab74e9.unit_price'},

        }},
        {'$project': {
            '_id' : 1,
            'total_fixed_rent' :{'$add':[0.0]},
            'total_office_rent':{'$add':[0.0]},
            'total_services': {'$add': [0.0]},
            'fixed_rent2': {'$add':['$fixed_rent']},
            'UE_agreed2':{'$add':['$UE_agreed']},
            'UE_avg2':{'$add':['$UE_avg']},
            'UE_unit_price2':{'$add':['$UE_unit_price']},
            'total_space_unit' : {
                '$cond': [
                    {'$and': [{'$lte': ['$fixed_rent', 0] }, {'$gt': ['$UE_agreed', 0] }]},
                    { '$cond' : [
                        {'$gt' : [{ '$subtract': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg'] }, '$UE_agreed' ]}, 0 ]},
                        {'$add' : [{ '$multiply': [ '$UE_agreed','$UE_unit_price' ]}, { '$multiply': [ { '$subtract': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg'] }, '$UE_agreed' ] }, '$UE_extra_price' ] }]},
                        { '$multiply': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg']}, '$UE_unit_price']},
                    ]},
                    { '$cond' : [
                        {'$and': [{'$gt': ['$fixed_rent', 0] }, {'$gt': ['$UE_agreed', 0] }]},
                        { '$cond' : [
                            {'$gt' : [ { '$subtract': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg'] }, '$UE_agreed' ] },0]},
                            {'$multiply': [ { '$subtract': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg'] }, '$UE_agreed' ] }, '$UE_unit_price' ] },
                            0]},
                        { '$cond' : [
                            {'$gt':[{ '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg']},0]},
                            {'$multiply': [ { '$add': ['$UE_avg', '$UEP_avg', '$UEE_avg'] }, '$UE_unit_price' ] },
                            0]}
                    ]}
                ]},

            }}]
    return query

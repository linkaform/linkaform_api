[
  {$match:{
        "itype" : "rent",
 "office_rent": {$exists:true}
    }},
  {$group:{
        _id: {
  currency : "$office_rent.currency",
            cliente: "$5591627901a4de7bb8eb1ad5",
            almacen: "$5591627901a4de7bb8eb1ad4",
            year: {$year:"$created_at"},
            month: {$month:"$created_at"}
          
        },
        OFFICE_RENT_total : {$sum:"$office_rent.unit_price"},
    }},

    {$match:{
        _id.year : 2015
    }}
]

db.form_answer.aggregate([
    {$match:{
	"form_id":2050
    }},
    {$group: {
	_id: {
	    marca : "$answers.555f47a901a4de47e4a9363a"
	},
	
	abierto : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "abierto"]},
		    then: 1,
		    else: 0
		}
	    }},
	perdido : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "perdido"]},
		    then: 1,
		    else: 0
		}
	    }},
	cerrado : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "cerrado"]},
		    then: 1,
		    else: 0
		}
	    }},
	cotizando : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "cotizando"]},
		    then: 1,
		    else: 0
		}
	    }},
	compró_otra_marca : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "compró_otra_marca"]},
		    then: 1,
		    else: 0
		}
	    }},
	vendido : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "vendido"]},
		    then: 1,
		    else: 0
		}
	    }},
	nunca_contestó : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "nunca_contestó"]},
		    then: 1,
		    else: 0
		}
	    }},
	cotización_enviada : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "cotización_enviada"]},
		    then: 1,
		    else: 0
		}
	    }},
	cambio_de_rep : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", "cambio_de_rep"]},
		    then: 1,
		    else: 0
		}
	    }},
	indefinido : {
	    $sum:{
		$cond: {
		    if:{ $eq:["$answers.555f6a9f01a4de47e4a9364d", null]},
		    then: 1,
		    else: 0
		}
	    }},
     total : {$sum: 1}
    }}])



cfg = {
	_id : "info_repl",
	"members"  : [
  { _id:0, host: "10.1.66.12:27017"},
	{ _id:1, host: "10.1.66.14:27014"},
	{ _id:2, host: "10.1.66.19:27019"},
	{ _id:3, host: "10.1.66.32:27032"},
		]
	}


rs.initiate(cfg)

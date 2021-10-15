#LinkaForm API
This API si created to use in python the services of the Linkaform API

### Using JWT as Authentication method

1. Rquest your JWT KEY **at the login funcion, send the parameter get_jwt=True**
> net = network.Network(settings)
jwt_key = net.login('', 'you_password', 'you_email@email.com', get_jwt=True)
2. Set the jwt_key to you settings
> from linkaform_api import settings
settings.config['JWT_KEY'] = res

## How to use Odoo API

Example on how to use de Odoo API
```
from linkaform_api import  odoo

oo= odoo.Odoo()
oo.user=''
oo.pwd = ''
oo.dbname=''
oo.host=''
oo.protocol = 'https'



partner_ids = oo.getMethod(args=[[['is_company', '=', True]]])
partners = oo.getMethod(metodo='read',args=[partner_ids], args2={'fields': ['name', 'country_id', 'email']})

prod_fields =['code', 'name', 'price', 'barcode', 'type', 'description','description_sale','uom_id', 'default_code', 'categ_id','uom_name','list_price','route_ids','display_name']
products = oo.getMethod(model='product.product',metodo='search_read', args2={'fields':prod_fields })

```

partner_fields =['_last_updated', 'name', 'vat', 'type', 'street', 'stree_name','stree_number','stree_number_2','stree2', 'city', 'state_id','zip','country_id','phone',
'mobile','email','']
partners = oo.getMethod(metodo='search_read',args=[[['is_company', '=', True],['is_client', '=', True]]], args2={'fields':partner_fields})

Documentacion en https://www.odoo.com/documentation/13.0/es/developer/misc/api/odoo.html

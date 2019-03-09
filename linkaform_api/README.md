#LinkaForm API
This API si created to use in python the services of the Linkaform API

### Using JWT as Authentication method

1. Rquest your JWT KEY **at the login funcion, send the parameter get_jwt=True**
> net = network.Network(settings)
jwt_key = net.login('', 'you_password', 'you_email@email.com', get_jwt=True)
2. Set the jwt_key to you settings
> from linkaform_api import settings
settings.config['JWT_KEY'] = res


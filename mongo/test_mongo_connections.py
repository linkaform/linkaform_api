

#para arrancar el ambiente correr desde infosync-api/backend
#python manage.py shell

from pymongo import MongoClient

from mongoengine.context_managers import switch_db
from mongoengine.fields import ValidationError

from base.utils import register_connection_answer
from forms.models import FormAnswer



mongo_hosts = '10.1.66.12:27017,10.1.66.14:27014,10.1.66.19:27019,10.1.66.32:27032'
mongo_replicaSet = 'info_repl'
mongo_readPreference='secondaryPreferred'

MONGODB_URI = 'mongodb://%s/?replicaSet=%s&readPreference=%s'%(mongo_hosts, mongo_replicaSet, mongo_readPreference)
#connect('infosync', host=MONGODB_URI)


c = MongoClient(MONGODB_URI)
all_dbs = c.database_names()

all_clientes = []

for client in all_dbs:




register_connection_answer(123)

with switch_db(FormAnswer, alias_current_user) as model:
  print FormAnswer.objects.count()

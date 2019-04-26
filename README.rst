# API de Linkaform

[![N|Solid](https://f001.backblazeb2.com/file/lkf-media/company_pictures/company_pic_2793.thumbnail)](https://app.linkaform.com/)

El API de Linkaform permite consumir los servicios del backend linkaform, como:

  - Crear formularios, catálogos
  - Crear/editar/borrar/obtener registros de formularios
  - Descargar registros de formularios
  - Exportar registros a excel y pdf

### Installation

Para utilizar la API de Linkaform se requiere instalar:
* [Python](https://www.python.org/)
* [Pymongo](https://api.mongodb.com/python/current/)
* [Psycopg](initd.org/)
* [Bson](bsonspec.org/)

Instala las dependencias, después descargar el tar.gz e instalarlo de la siguiente manera:

```sh
$ wget https://f001.backblazeb2.com/file/lkf-resources/linkaform_api-0.1.tar.gz
$ pip install linkaform_api-0.1.tar.gz
```

#### Crear tar.gz
Para crear un tar.gz solo se tienen que ejecutar las siguientes líneas de comando
```sh
$ rm -r dist
$ python setup.py sdist
```
Para subir el .tar.gz a backblaze se tiene que iniciar sesión en b2 y subir el tar.gz a:
```sh
$ b2 upload_file lkf-resources dist/linkaform_api-0.1.tar.gz linkaform_api-0.1.tar.gz
```

   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>



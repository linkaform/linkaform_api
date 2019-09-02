#!/bin/bash

echo Removiendo antiguo tar
rm -rf dist
echo Creando nuevo tar
python setup.py sdist
echo Authorizando cuenta en b2
$(which b2) authorize-account f5fde066eaac 001bada2501283bc9014a905a767c55761ecb3136c
echo Subiendo...
b2 upload_file lkf-resources dist/linkaform_api-0.1.tar.gz linkaform_api-0.1.tar.gz

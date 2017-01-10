#####
# Made by Jose Patricio VM
#####
# Script que contiene las reglas para el archivo de carga de Telmex Cobre
#
#
#####


def set_construccion(answers):
    #Construccion de linea de cliente basica de 1 par (bajante)
    #Construccion de linea de cliente basica de 2 pares (bajante)
    #Construccion de linea de cliente basica de 1 par blindado (bajante)
    #Construccion de linea de cliente basica con cable autosoportado (bajante)
    return [1,'','','']

def set_plusvalia(answers):
    #Plusvalia por tramo adicional de 50m. con bajante de 1 par
    #Plusvalia por tramo adicional de 50m. con bajante 2 pares
    #Plusvalia por tramo adicional de 50m. con bajante de 1 par blindado
    #Plusvalia por tramo adicional de 50m. con cable autosoportado acreebgh (bajante)
    metros = answers['f1054000a020000000000007']
    plusvalias = metros / 50
    if plusvalias > 5:
        plusvalias = 5
    if plusvalias == 0:
        plusvalias = ''
    return [plusvalias, '', '', '']


def set_recontratacion(record):
    return ['', '', '', '']


def set_instalacion_poste(record):
    return ['', '']

def set_bonificaion(record):
    return ['', '', '', '']


def set_montaje_puente(record):
    return ['']


def set_insalacion_cadena(record):
    return ['']


def set_prueba_transmicion(record):
    return ['']


def set_cableado_interior(record):
    return [1, '']


def set_prueba_transmicion_datos(record):
    return ['']


def set_ubicacion_cliente(record):
    return ['']


def set_prueba_transmicion_vsdl(record):
    return ['']

def set_libreria(record):
    return ['MEX']

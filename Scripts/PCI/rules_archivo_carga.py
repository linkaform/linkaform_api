#####
# Made by Jose Patricio VM
#####
# Script que contiene las reglas para el archivo de carga de Telmex Cobre
#
#
#####


def set_construccion(record):
    #Construccion de linea de cliente basica de 1 par (bajante)
    #Construccion de linea de cliente basica de 2 pares (bajante)
    #Construccion de linea de cliente basica de 1 par blindado (bajante)
    #Construccion de linea de cliente basica con cable autosoportado (bajante)
    tipo = False
    if record.has_key('f1054000a010000000000021') and record['f1054000a010000000000021']:
        tipo = record['f1054000a010000000000021'][2:4]

    #La ordenes tipo TE que son publicas no llevan Construccion
    if 'TE' in tipo.upper():
        return ['','','','']

    return [1,'','','']


def set_plusvalia(record):
    #Plusvalia por tramo adicional de 50m. con bajante de 1 par
    #Plusvalia por tramo adicional de 50m. con bajante 2 pares
    #Plusvalia por tramo adicional de 50m. con bajante de 1 par blindado
    #Plusvalia por tramo adicional de 50m. con cable autosoportado acreebgh (bajante)
    try:
        metros = record['f1054000a020000000000007']
        plusvalias = metros / 51
    except KeyError:
        plusvalias = 0
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
    bonificacion = False
    if record.has_key('f1054000a020000100000008'):
        bonificacion = record['f1054000a020000100000008']
    if bonificacion == 'de_1_a_5':
        return [1, '', '', '']
    if bonificacion == 'de_6_a_15':
        return ['', 1, '', '']
    if bonificacion == 'de_16_a_25':
        return ['', '', 1, '']
    if bonificacion == 'mas_de_25':
        return ['', '', '', 1]
    return ['', '', '', '']


def set_montaje_puente(record):
    tipo = ''
    puente = 0
    if record.has_key('f1054000a020000100000007') and record['f1054000a020000100000007']:
        puente = record['f1054000a020000100000007']
    if record.has_key('f1054000a010000000000021') and record['f1054000a010000000000021']:
        tipo = record['f1054000a010000000000021'][2:4]
    if 'L' in tipo.upper() and puente == 2:
        return [2,]
    if ('10' == tipo or '20' == tipo) and puente ==1:
        return [1,]
    if 'L' in tipo.upper() and puente == 1:
        return 'Error: Tipo de OS L y solo 1 punete indicado'
    if ('10' == tipo or '20' == tipo) and puente ==2:
        return 'Error: Tipo de OS 10 o 20 y 2 punetes indicado'
    return ['',]


def set_insalacion_cadena(record):
    return ['',]


def set_prueba_transmicion(record):
    tipo = ''
    test = True
    if record.has_key('f1054000a010000000000021') and record['f1054000a010000000000021']:
        tipo = record['f1054000a010000000000021'][2:4]
    if record.has_key('f1054000a020000100000010') and record['f1054000a020000100000010']:
        test = True
    if 'L' in tipo.upper() and tipo:
        if test:
            return [1,]
    return ['',]


def set_cableado_interior(record):
    tipo = False
    if record.has_key('f1054000a010000000000021') and record['f1054000a010000000000021']:
        tipo = record['f1054000a010000000000021'][:4]
    if 'A049' == tipo.upper():
        return ['','']
    if 'TE' in tipo.upper():
        extensiones = 1
        if record.has_key('f1054000a020000100000007') and record['f1054000a020000100000007']:
                try:
                    extensiones = int(record['f1054000a020000100000007'])
                except:
                    extensiones = 1
        return ['', extensiones]
    return [1,'']


def set_prueba_transmicion_datos(record):
    return ['']


def set_ubicacion_cliente(record):
    return ['']


def set_prueba_transmicion_vsdl(record):
    return ['']


def set_libreria(record):
    area = False
    if record.has_key('f1054000a010000000000003') and record['f1054000a010000000000003']:
        area = record['f1054000a010000000000003'][:4]
    if area.lower() in ['acapulco','chilpancingo','cuernavaca']:
        return ['CVA']
    return ['MEX']

# -*- coding: utf-8 -*-
import sys, simplejson
from datetime import datetime
import facturapi
from facturapi import configure
#from facturapi.resources.invoices import InvoiceItem
from facturapi.resources.invoices import InvoiceRequest
from class_invoice_nomina import InvoiceNomina
from facturapi.types import FileType

# Configuracion del API KEY
configure(api_key='sk_test_aPvVRjg72M6A1zZDVMd3ZYyWrGl830DK')

class Invoices:
    def __init__(self, lkf_api, cr):
        self.lkf_api = lkf_api
        self.cr = cr

    def get_val_from_readonly(self, dict_to_eval, id_field_readonly):
        val = ''
        list_val = dict_to_eval.get( id_field_readonly, [] )
        if list_val and list_val[0]:
            val = list_val[0]
        return val

    def calculate_days( self, f1, f2 ):
        df1 = datetime.strptime(f1, '%Y-%m-%d')
        df2 = datetime.strptime(f2, '%Y-%m-%d')
        diff_dates = df2 - df1
        return diff_dates.days

    def upload_file_geted( self, path_file, form_id, file_field_id, type_file='' ):
        nomina_file = open( path_file, 'rb' )
        nomina_file_dir = {'File': nomina_file}
        try:
            upload_data = {'form_id': form_id, 'field_id': file_field_id}
            upload_url = self.lkf_api.post_upload_file(data=upload_data, up_file=nomina_file_dir,  jwt_settings_key='USER_JWT_KEY')
            print("******************** upload_url:",upload_url)
        except Exception as e:
            print("No se pudo cargar el documento: ",str(e))
            return {'error': "No se pudo cargar el documento"}
        nomina_file.close()
        try:
            file_url = upload_url['data']['file']
            res_uploaded = {file_field_id: {'file_name':'Factura de nomina.{}'.format(type_file), 'file_url':file_url}}
        except KeyError:
            print('could not save file Errores')
        return res_uploaded

    def generate_invoce( self, invoice_request, current_record, record_id, type_text_invoce='Nomina' ):
        try:
            invoice = facturapi.Invoice.create(data=invoice_request)
        except Exception as e:
            print('ERRORRRRRR==', e)
            current_record['answers']['eeeee0000000000000000001'] = 'error'
            current_record['answers']['eeeee0000000000000000002'] = 'Ocurrió un error al querer generar las facturas'
            self.lkf_api.patch_record(current_record, record_id, jwt_settings_key='USER_JWT_KEY')
            return False

        #print("invoice=",invoice)
        # Resource is now created an can be used to access data or perform actions.
        total = invoice.total
        id_facturaGenerada = invoice.id

        print('total=',total)

        # Descargar la factura en formato PDF
        invoice_file = facturapi.Invoice.download(
            id=id_facturaGenerada, file_type=FileType.pdf
            )
        with open( '/tmp/{}_{}.pdf'.format(type_text_invoce, id_facturaGenerada), 'wb' ) as f:
            f.write(invoice_file)

        pdf_file = self.upload_file_geted( '/tmp/{}_{}.pdf'.format(type_text_invoce, id_facturaGenerada), current_record['form_id'], 'eeeee0000000000000000003', type_file='pdf' )

        # Descargar la factura en formato XML
        invoice_file_xml = facturapi.Invoice.download(
            id=id_facturaGenerada, file_type=FileType.xml
            )
        with open( '/tmp/{}_{}.xml'.format(type_text_invoce, id_facturaGenerada), 'wb' ) as f:
            f.write(invoice_file_xml)

        xml_file = self.upload_file_geted( '/tmp/{}_{}.xml'.format(type_text_invoce, id_facturaGenerada), current_record['form_id'], 'eeeee0000000000000000004', type_file='xml' )
        status_set = 'terminado'
        comentarios_proceso = ''
        if pdf_file.get('error') or xml_file.get('error'):
            status_set = 'error'
            comentarios_proceso = 'Ocurrió un error al cargar los documentos de la factura'
        current_record['answers']['eeeee0000000000000000001'] = status_set
        current_record['answers']['eeeee0000000000000000002'] = comentarios_proceso
        if not pdf_file.get('error'):
            current_record['answers'].update( pdf_file )
        if not xml_file.get('error'):
            current_record['answers'].update( xml_file )
        self.lkf_api.patch_record(current_record, record_id, jwt_settings_key='USER_JWT_KEY')

    def generar_factura_nomina(self, current_record, record_id, created_at):

        # Obtengo los campos de tipo catálogo para ver sus ids en la forma
        form_fields = self.lkf_api.get_form_id_fields(current_record['form_id'], jwt_settings_key='USER_JWT_KEY')
        fields = form_fields[0]['fields']
        fields_catalog = [ f for f in fields if f['field_type'] == 'catalog' ]

        field_id_catalog_empleado = None
        field_id_catalog_tipo_percepcion = None
        field_id_catalog_tipo_hrs = None
        field_id_catalog_tipo_deduccion = None
        field_id_catalog_tipo_otro_pago = None
        field_id_catalog_tipo_incapacidad = None
        for fc in fields_catalog:
            if 'e00000000000000000000001' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_empleado = fc.get('field_id')
            if 'b50000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_tipo_percepcion = fc.get('field_id')
            if 'b60000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_tipo_hrs = fc.get('field_id')
            if 'b70000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_tipo_deduccion = fc.get('field_id')
            if 'b80000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_tipo_otro_pago = fc.get('field_id')
            if 'b90000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_tipo_incapacidad = fc.get('field_id')

        if not all( [ field_id_catalog_empleado, field_id_catalog_tipo_percepcion, field_id_catalog_tipo_hrs, field_id_catalog_tipo_deduccion, \
            field_id_catalog_tipo_otro_pago, field_id_catalog_tipo_incapacidad] ):
            current_record['answers']['eeeee0000000000000000001'] = 'error'
            current_record['answers']['eeeee0000000000000000002'] = 'La forma no tiene configurada los catálogos necesarios, favor de revisar'
            self.lkf_api.patch_record(current_record, record_id, jwt_settings_key='USER_JWT_KEY')
            return False

        a = current_record.get('answers', {})
        all_info_empleado = a.get(field_id_catalog_empleado, {})
        fecha_pago = created_at.strftime("%Y-%m-%d")
        dict_complements = dict(
            type= "nomina", # Constante
            data= {
                # Tipo de nómina. Puede tener los valores “O” (Ordinaria), cuando corresponde a un pago que se realiza de manera habitual, como sueldos;
                # ó “E” (Extraordinaria) para pagos fuera de lo habitual, como liquidaciones, aguinaldos o bonos.
                "tipo_nomina": "O",
                "fecha_pago": fecha_pago,
                "fecha_inicial_pago": a.get('eeeee0000000000000000005'),
                "fecha_final_pago": a.get('eeeee0000000000000000006'),
                # Calcular los días transcurridos entre la fecha incial y final de la quincena
                "num_dias_pagados": self.calculate_days( a.get('eeeee0000000000000000005'), a.get('eeeee0000000000000000006') ),
                # Información del trabajador
                "receptor": {
                    "curp": self.get_val_from_readonly(all_info_empleado, 'e00000000000000000000002'),
                    "tipo_contrato": self.get_val_from_readonly(all_info_empleado, 'b00000000000000000000001'), # Del catálogo Tipo de Contrato
                    "tipo_regimen": self.get_val_from_readonly(all_info_empleado, 'b20000000000000000000001'), # Del catálogo Tipo de Régimen
                    "num_empleado": self.get_val_from_readonly(all_info_empleado, 'e00000000000000000000004'), # Número interno del empleado en string
                    "clave_ent_fed": "NLE"
                }
            }
        )

        ########################################################
        # Agrego los valores opcionales del receptor
        ########################################################
        receptor_nss = self.get_val_from_readonly(all_info_empleado, 'e00000000000000000000003')
        if receptor_nss:
            dict_complements['data']['receptor'].update({ "num_seguridad_social": receptor_nss })
        receptor_f_inicio_relacion = self.get_val_from_readonly(all_info_empleado, 'e00000000000000000000005')
        if receptor_f_inicio_relacion:
            dict_complements['data']['receptor'].update({ "fecha_inicio_rel_laboral": receptor_f_inicio_relacion })
        receptor_sindicalizado = self.get_val_from_readonly(all_info_empleado, 'e00000000000000000000006')
        if receptor_sindicalizado:
            dict_complements['data']['receptor'].update({ "sindicalizado": receptor_sindicalizado })
        receptor_tipo_jornada = self.get_val_from_readonly(all_info_empleado, 'b10000000000000000000001')
        if receptor_tipo_jornada:
            dict_complements['data']['receptor'].update({ "tipo_jornada": receptor_tipo_jornada })
        receptor_depto = self.get_val_from_readonly(all_info_empleado, 'd00000000000000000000001')
        if receptor_depto:
            dict_complements['data']['receptor'].update({ "departamento": receptor_depto })
        receptor_puesto = self.get_val_from_readonly(all_info_empleado, 'dd0000000000000000000001')
        if receptor_puesto:
            dict_complements['data']['receptor'].update({ "puesto": receptor_puesto })
        receptor_riesgo_puesto = self.get_val_from_readonly(all_info_empleado, 'b30000000000000000000001')
        if receptor_riesgo_puesto:
            dict_complements['data']['receptor'].update({ "riesgo_puesto": receptor_riesgo_puesto })
        receptor_periodicidad = self.get_val_from_readonly(all_info_empleado, 'b40000000000000000000001')
        if receptor_periodicidad:
            dict_complements['data']['receptor'].update({ "periodicidad_pago": receptor_periodicidad })

        ########################################################
        # Percepciones Opcional pero reviso si el registro tiene info
        ########################################################
        percepciones = a.get('aaaaa0000000000000000001', [])
        list_percepciones = []
        if percepciones:
            for p in percepciones:
                dict_p = {
                    "tipo_percepcion": self.get_val_from_readonly(p.get(field_id_catalog_tipo_percepcion, {}), 'b50000000000000000000001'), # Del catálogo Tipo de percepcion
                    "clave": p.get('aaaaa00000000000000001a2', ''), # Clave de control interno que asigna el patron a cada percepción de nómina propia de su contabilidad
                    "importe_gravado": p.get('aaaaa00000000000000001a3', 0), # Importe gravado por el concepto indicado en el tipo de percepción.
                    "importe_exento": p.get('aaaaa00000000000000001a4', 0), # Importe exento por el concepto indicado en el tipo de percepción.
                    "concepto": p.get('aaaaa00000000000000001a1', None), # Opcional si no se envia un string entonces Del catálogo Tipo de percepcion
                }
                # Opcionales para las percepciones
                hrs_extra = {}
                hrs_codigo = self.get_val_from_readonly( p.get(field_id_catalog_tipo_hrs, {}), 'b60000000000000000000001' )
                if hrs_codigo:
                    hrs_extra.update({
                        "tipo_horas": hrs_codigo, # Del catálogo Tipo de Horas
                        "dias": p.get('aaaaa000000000000001a5e1', 0), # Número de días en que el trabajador laboró horas extras
                        "horas_extra": p.get('aaaaa000000000000001a5e2', 0), # Número de horas extra trabajadas en el periodo
                        "importe_pagado": p.get('aaaaa000000000000001a5e3', 0) # Importe pagado por las horas extra
                    })
                if hrs_extra:
                    dict_p.update({
                        "horas_extra": [ hrs_extra ]
                    })
                list_percepciones.append( dict_p )
        if list_percepciones:
            dict_complements['data'].update({
                'percepciones': {
                    'percepcion': list_percepciones
                }
            })

        ########################################################
        # Deducciones Opcional pero reviso si el registro tiene info
        ########################################################
        deducciones = a.get('bbbbb0000000000000000001', [])
        list_deducciones = []
        for d in deducciones:
            dict_d = {
                "tipo_deduccion": self.get_val_from_readonly( d.get(field_id_catalog_tipo_deduccion, {}), 'b70000000000000000000001' ), # Del catálogo Tipo de deducción
                "clave": d.get('bbbbb00000000000000001a2', ''), # Clave de control interno
                "importe": d.get('bbbbb00000000000000001a3', 0) # Importe del concepto de deducción
            }
            if d.get('bbbbb00000000000000001a1', False):
                dict_d.update({
                    "concepto": d.get('bbbbb00000000000000001a1', None) # Opcional concepto de la deduccion
                })
            list_deducciones.append( dict_d )
        if list_deducciones:
            dict_complements['data'].update({
                'deducciones': list_deducciones
            })

        ########################################################
        # Otros Pagos Opcional pero reviso si el registro tiene info
        ########################################################
        otros_pagos = a.get('ccccc0000000000000000001', [])
        list_otros_pagos = []
        for o in otros_pagos:
            dict_o = {
                "tipo_otro_pago": self.get_val_from_readonly( o.get(field_id_catalog_tipo_otro_pago, {}), 'b80000000000000000000001' ), # Clave del catálogo Tipo de Otro Pago
                "clave": o.get('ccccc00000000000000001a1', ''), # Clave de otro pago de nómina propia de contabilidad interna
                "importe": o.get('ccccc00000000000000001a2', 0) # Importe por concepto de otro pago
            }
            list_otros_pagos.append(dict_o)
        if list_otros_pagos:
            dict_complements['data'].update({
                'otros_pagos': list_otros_pagos
            })

        ########################################################
        # Incapacidades Opcional pero reviso si el registro tiene info
        ########################################################
        incapacidades = a.get('ddddd0000000000000000001', [])
        list_incapacidades = []
        for i in incapacidades:
            dict_i = {
                "dias_incapacidad": i.get('ddddd00000000000000001a1', 0), # Número de días enteros que el trabajador se incapacitó en el periodo.
                "tipo_incapacidad": self.get_val_from_readonly( i.get(field_id_catalog_tipo_incapacidad, {}), 'b90000000000000000000001' ), # Del catálogo Tipo de Incapacidad
                "importe_monetario": i.get('ddddd00000000000000001a2', 0) # Opcional Monto del importe monetario de la incapacidad
            }
            list_incapacidades.append(dict_i)
        if list_incapacidades:
            dict_complements['data'].update({
                'incapacidades': list_incapacidades
            })

        invoice_request = InvoiceNomina(
            type= "N", # Constante
            #
            # Esta info podría obtenerse de un catálogo de empleados
            #
            customer= {
                "legal_name": all_info_empleado.get('e00000000000000000000001'), # Nombre
                "email": self.get_val_from_readonly( all_info_empleado, 'e00000000000000000000008' ), # email
                "tax_id": self.get_val_from_readonly( all_info_empleado, 'e00000000000000000000007' ) # RFC
            },
            # Es opcional y entero, podria ser el folio del registro pero sin el guión
            folio_number= int( current_record['folio'].replace('-', '') ),
            
            # Identificador opcional que puedes usar para relacionar esta factura con tus registros y poder hacer búsquedas usando este identificador
            # Aqui se puede utilizar el id del registro linkaform
            external_id= record_id,

            complements= [
                dict_complements
            ]
        )
        print(invoice_request)

        self.generate_invoce( invoice_request, current_record, record_id )

    """
    # Regresa el contenido del registro en MongoDB
    # Aplica cuando el registro es demasiado grande y no contiene el índice 'answers'
    """
    def get_record_from_db(self, form_id, folio):
        query = {
            'form_id': form_id,
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1,'_id':1,'connection_id':1,'created_at':1,'other_versions':1,'timezone':1}
        record_found = self.cr.find(query, select_columns)
        return record_found.next()

    def generar_factura_trabajo(self, current_record, record_id, created_at):
        # Obtengo los campos de tipo catálogo para ver sus ids en la forma
        form_fields = self.lkf_api.get_form_id_fields(current_record['form_id'], jwt_settings_key='USER_JWT_KEY')
        fields = form_fields[0]['fields']
        fields_catalog = [ f for f in fields if f['field_type'] == 'catalog' ]

        field_id_catalog_empresas = None
        field_id_catalog_taxes = None
        field_id_catalog_conceptos = None
        field_id_catalog_forma_pago = None
        for fc in fields_catalog:
            if 'ddee00000000000000000001' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_empresas = fc.get('field_id')
            if 'ddaa00000000000000000001' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_taxes = fc.get('field_id')
            if 'ddff00000000000000000001' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_conceptos = fc.get('field_id')
            if 'a00000000000000000000002' in fc.get('catalog', {}).get('view_fields', []):
                field_id_catalog_forma_pago = fc.get('field_id')

        if not all( [field_id_catalog_empresas] ):
            current_record['answers']['eeeee0000000000000000001'] = 'error'
            current_record['answers']['eeeee0000000000000000002'] = 'La forma no tiene configurada los catálogos necesarios, favor de revisar'
            self.lkf_api.patch_record(current_record, record_id, jwt_settings_key='USER_JWT_KEY')
            return False

        a = current_record.get('answers', {})
        all_info_empresa = a.get(field_id_catalog_empresas, {})

        dict_product = dict(
            # Si se requiere que el atributo "price" sea el precio unitario, se debe enviar el parámetro "tax_included" con el valor "False"
            # Si es True se considera que el precio lleva el IVA incluido
            tax_included= False
        )

        ########################################################
        # Impuestos es opcional pero si no trae info se entiende que es exento
        ########################################################
        impuestos = a.get('aaaaa0000000000000000002', [])
        list_impuestos = []
        for i in impuestos:
            is_retencion = self.get_val_from_readonly( i.get(field_id_catalog_taxes, {}), 'ddaa00000000000000000004' ), # ¿Es retencion?
            bool_retencion = True if is_retencion or is_retencion != 'No' else False
            # taxes   array   Lista de impuestos que deberán aplicarse a este producto. Si la lista está vacía, se entiende que el producto está excento de impuestos.
            # taxes[].rate    decimal Tasa del impuesto.
            # taxes[].type    string  Tipo de impuesto. Puede tener los valores "IVA", "ISR" o "IEPS".
            # taxes[].ieps_mode   string  Si el tipo de impuesto es "IEPS", indica la manera de cobrar el impuesto, y puede tener los valores “sum_before_taxes” o “break_down”.
            # taxes[].factor  string  Tipo factor. Puede tener los valores "Tasa", "Cuota" o "Exento".
            # taxes[].withholding boolean true: el impuesto es una retención. false: el impuesto es un traslado (impuesto normal).
            dict_i = {
                "rate": self.get_val_from_readonly( i.get(field_id_catalog_taxes, {}), 'ddaa00000000000000000002' ), # Porcentaje
                "type": self.get_val_from_readonly( i.get(field_id_catalog_taxes, {}), 'ddaa00000000000000000003' ), # Tipo
                "withholding": bool_retencion,
                "factor": self.get_val_from_readonly( i.get(field_id_catalog_taxes, {}), 'ddaa00000000000000000005' ), # Factor
            }
            list_impuestos.append(dict_i)

        ########################################################
        # Conceptos de los productos que se facturarán
        ########################################################
        conceptos = a.get('aaaaa0000000000000000001', [])
        list_conceptos = []
        pos_c = 0
        for c in conceptos:
            pos_c += 1
            dict_c = dict(
                description = c.get(field_id_catalog_conceptos, {}).get('ddff00000000000000000001', ''), # Descripcion
                price = self.get_val_from_readonly( i.get(field_id_catalog_conceptos, {}), 'ddff00000000000000000002' ), # Precio
                product_key= '{}{}'.format( current_record['folio'].replace('-', ''), pos_c ),
            )
            if list_impuestos:
                dict_c.update({
                    'taxes': list_impuestos
                })
            list_conceptos.append( dict(
                product= dict_c,
                quantity= c.get('aaaaa00000000000000001a2', 0),
                discount= c.get('aaaaa00000000000000001a3', 0)
            ) )
        
        ######################################################
        # Código de la Forma de pago
        ######################################################
        codigo_forma_pago = self.get_val_from_readonly( a.get(field_id_catalog_forma_pago, {}), 'a00000000000000000000001' )
        if not codigo_forma_pago:
            codigo_forma_pago = None

        invoice_request = InvoiceRequest(
            # Puedo usar el id del cliente si está creado
            # customer=customer.id,
            # O también puedo pasar la información del cliente si no existe
            customer = {
                "legal_name": all_info_empresa.get('ddee00000000000000000001'), # Nombre de la Empresa
                "email": self.get_val_from_readonly( all_info_empresa, 'ddee00000000000000000002' ), # email
                "tax_id": self.get_val_from_readonly( all_info_empresa, 'ddee00000000000000000003' ) # RFC
            },
            
            items=list_conceptos,
            payment_form=codigo_forma_pago,
        )
        print(invoice_request)
        #invoice = facturapi.Invoice.create(data=invoice_request)
        self.generate_invoce( invoice_request, current_record, record_id )

class SepoMex(Form):

    ALIMENTO_RECIBIDO = 3015
    PESO_SEMANAL = 4627
    ABC_LOTES = 4886
    ALIMENTO_CONSUMO_DIARIO = 3295
    PEDIDO_ALIMENTO_SEMANAL = 2925
    VENTAS_Y_TRASPASOS = 2754
    CERDOS_RECIBIDOS = 2760
    MORTALIDADES_MODULOS = 3288
    MORTALIDADES_SANFANDILA_ABC = 4706
    PARAMETROS = 4879
    CAPACIDAD_LAGOS = 1234
    TESTING = 5106

    def __init__(self, **kwargs):
        super(SanfandilaForm, self).__init__(**kwargs)
        if self.form_id is None:
            self.form_id = self.get_form_id(kwargs["file_path"])


    def __str__():
        return super(SanfandilaForm, self).__str__()

    def get_form(self):
        return self.clean_file_structure({
            "form_id" : self.form_id,
            "geolocation" : self.geolocation,
            "start_timestamp" : self.start_timestamp,
            "end_timestamp" : self.end_timestamp,
            "answers" : self.get_answers()
            #"created_at" : self.convert_to_epoch(self.created_at),
        })

    def get_form_id(self, filename):
        form_id_filenames_map = {
            self.ALIMENTO_RECIBIDO : 'alimento_recibido',
            self.PESO_SEMANAL : 'peso_semanal',
            self.ABC_LOTES : 'abc_lotes',
            self.ALIMENTO_CONSUMO_DIARIO : 'alimento_consumo_diario',
            self.ALIMENTO_RECIBIDO : 'alimento_recibido',
            self.PEDIDO_ALIMENTO_SEMANAL : 'pedido_alimento_semanal',
            self.VENTAS_Y_TRASPASOS : 'ventas_y_traspasos',
            self.CERDOS_RECIBIDOS : 'cerdos_recibidos',
            self.MORTALIDADES_MODULOS : 'mortalidades_modulos',
            self.MORTALIDADES_SANFANDILA_ABC : 'mortalidades_sanfandila_abc',
            self.PARAMETROS : 'parametros',
            self.CAPACIDAD_LAGOS : 'capacidad_lagos',
            self.TESTING : 'testing'
        }

        for key, value in form_id_filenames_map.iteritems():
            if value in filename:
                return key
        raise ValueError("invalid filename!")


    def get_answers(self):
        answer_keys = self.answers.keys()
        if self.created_at is None:
            try:
                self.created_at = self.get_answer_for_field_id(answer_keys, self.answers, 'fecha_creacion', '')
            except:
                self.created_at = ''
        return self.recursive_extraction_answers(self.get_variables_definition(), answer_keys)


    def recursive_extraction_answers(self, configuration, answer_keys):
        answers = {}
        for item in configuration:
            if isinstance(item, dict):
                for field_form_file, field_form_collection in item.iteritems():
                    if field_form_collection[0] == FieldType.ONE_FIELD:
                        result = self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2])
                        if field_form_collection[2] == 'int' and result == '':
                            result = 0
                        answers[field_form_collection[1]] = result

                    elif field_form_collection[0] == FieldType.GROUP_FIELD:
                        try:
                            answers_in_group = field_form_file.split(',')
                            answers_list_group = list()
                            for answer in answers_in_group:
                                answers_list_group.append(self.get_answer_for_field_id(answer_keys, self.answers, field_form_file, field_form_collection[2]))
                            answers[field_form_collection[1]] = answers_list_group
                        except:
                            raise TypeError("Error to parse a multiple field")
                    elif field_form_collection[0] == FieldsType.REPETITIVE_FIELDS:
                        answers[field_form_collection[1]] = [self.recursive_extraction_answers(field_form_collection, answer_keys)]
                    else:
                        raise TypeError("Error to parse configuration")
        return answers

    def get_variables_definition(self):
        form_id_fields_map =  {
            self.ALIMENTO_RECIBIDO : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'alimento' : (FieldsType.REPETITIVE_FIELDS, '301500000000000000000003', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, '301500000000000000000004', 'select'),
                    'origen_alimento' : (FieldType.ONE_FIELD, '301500000000000000000005', 'select'),
                    'cantidad' : (FieldType.ONE_FIELD, '301500000000000000000006', 'int')
                })
            }],

            self.PESO_SEMANAL : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'tamano_muestra' : (FieldType.ONE_FIELD, '462700000000000000000003', 'float'),
                'kilos_total' : (FieldType.ONE_FIELD, '462700000000000000000004', 'float'),
                'edad_sem' : (FieldType.ONE_FIELD, '462700000000000000000005', 'int')
            }],

            self.ABC_LOTES : [{
                'lote' : (FieldType.ONE_FIELD, '488600000000000000000001', 'float'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'etapa' : (FieldType.ONE_FIELD, '488600000000000000000003', 'select'),
                'flujo' : (FieldType.ONE_FIELD, '488600000000000000000004', 'select'),
                'fecha_inicio' : (FieldType.ONE_FIELD, '000000000000000000000005', 'date'),
                'estatus' : (FieldType.ONE_FIELD, '488600000000000000000006', 'select'),
            }],

            self.ALIMENTO_CONSUMO_DIARIO : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'alimento' : (FieldsType.REPETITIVE_FIELDS, '329500000000000000000003', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, '329500000000000000000004', 'select'),
                    'lote' : (FieldType.ONE_FIELD, '329500000000000000000005', 'int'),
                    'kilos' : (FieldType.ONE_FIELD, '329500000000000000000006', 'float')
                })
            }],

            self.PEDIDO_ALIMENTO_SEMANAL : [{
                'numero_semana_pedido' : (FieldType.ONE_FIELD, '292500000000000000000001', ''),
                'granja' : (FieldType.ONE_FIELD, '292500000000000000000002', 'select'),
                'pedido_alimento' : (FieldsType.REPETITIVE_FIELDS, '292500000000000000000003', {
                    'tipo_alimento' : (FieldType.ONE_FIELD, '292500000000000000000004', 'select'),
                    'cantidad' : (FieldType.ONE_FIELD, '292500000000000000000005', 'float'),
                    'dia' : (FieldType.ONE_FIELD, '292500000000000000000006', 'select'),
                })
            }],

            self.VENTAS_Y_TRASPASOS : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'tipo_movimiento' : (FieldsType.REPETITIVE_FIELDS, '275400000000000000000003', {
                    'movimiento' : (FieldType.ONE_FIELD, '275400000000000000000004', 'select'),
                    'traspaso_granja_destino' : (FieldType.ONE_FIELD, '275400000000000000000005', 'select'),
                    'cantidad' : (FieldType.ONE_FIELD, '275400000000000000000006', 'int'),
                    'kilos_totales' : (FieldType.ONE_FIELD, '275400000000000000000007', 'int'),
                    'dias_totales' : (FieldType.ONE_FIELD, '275400000000000000000008', 'int'),
                    'lote' : (FieldType.ONE_FIELD, '275400000000000000000009', 'int'),
                    'flujo' : (FieldType.ONE_FIELD, '275400000000000000000010', 'select')
                })
            }],

            self.CERDOS_RECIBIDOS : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'flujo' : (FieldType.ONE_FIELD, '276000000000000000000003', 'select'),
                'granja_origen' : (FieldType.ONE_FIELD, '276000000000000000000004', 'select'),
                'lote' : (FieldType.ONE_FIELD, '276000000000000000000005', 'int'),
                'cerdos_recibidos' : (FieldType.ONE_FIELD, '276000000000000000000006', 'float'),
                'kilos_total' : (FieldType.ONE_FIELD, '276000000000000000000007', 'float'),
                'edad_total' : (FieldType.ONE_FIELD, '276000000000000000000008', 'float')
            }],

            self.MORTALIDADES_MODULOS : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'total_muertos' : (FieldType.ONE_FIELD, '328800000000000000000003', 'int'),
                'descripcion_muertes' : (FieldsType.REPETITIVE_FIELDS, '328800000000000000000004', {
                    'causa_muerte' : (FieldType.ONE_FIELD, '328800000000000000000005', 'select'),
                    'muerto_por_esta_causa' : (FieldType.ONE_FIELD, '328800000000000000000006', 'int'),
                    'lote' : (FieldType.ONE_FIELD, '328800000000000000000007', 'int'),
                    'flujo' : (FieldType.ONE_FIELD, '328800000000000000000008', 'select')
                })
            }],

            self.MORTALIDADES_SANFANDILA_ABC : [{
                'fecha' : (FieldType.ONE_FIELD, '000000000000000000000001', 'date'),
                'granja' : (FieldType.ONE_FIELD, '000000000000000000000002', 'select'),
                'total_muertos' : (FieldType.ONE_FIELD, '470600000000000000000003', 'int'),
                'descripcion_muertes' : (FieldsType.REPETITIVE_FIELDS, '470600000000000000000004', {
                    'causa_muerte' : (FieldType.ONE_FIELD, '470600000000000000000005', 'select'),
                    'muerto_por_esta_causa' : (FieldType.ONE_FIELD, '470600000000000000000006', 'select'),
                    'lote' : (FieldType.ONE_FIELD, '470600000000000000000007', 'int'),
                    'flujo' : (FieldType.ONE_FIELD, '470600000000000000000008', 'select')
                })
            }],

            self.PARAMETROS : [{
                'sem_edad' : (FieldType.ONE_FIELD, '487900000000000000000001', 'float'),
                'alimento_consumo_semanal' : (FieldType.ONE_FIELD, '487900000000000000000002', 'float'),
                'alimento_consumo_diario' : (FieldType.ONE_FIELD, '487900000000000000000003', 'float'),
                'ganancia_diaria' : (FieldType.ONE_FIELD, '487900000000000000000004', 'float'),
                'gsp' : (FieldType.ONE_FIELD, '487900000000000000000005', 'float'),
                'peso' : (FieldType.ONE_FIELD, '487900000000000000000006', 'float'),
                'porcentaje_desecho' : (FieldType.ONE_FIELD, '487900000000000000000007', 'float'),
                'peso_retrasado' : (FieldType.ONE_FIELD, '487900000000000000000008', 'float'),
                'conversion_alimenticia' : (FieldType.ONE_FIELD, '487900000000000000000009', 'float'),
                'mortalidad' : (FieldType.ONE_FIELD, '487900000000000000000010', 'float'),
                'consumo_semanal' : (FieldType.ONE_FIELD, '487900000000000000000011', 'float'),
                'consumo_diario' : (FieldType.ONE_FIELD, '487900000000000000000012', 'float'),
                'kg_carne' : (FieldType.ONE_FIELD, '487900000000000000000013', 'float'),
                'dias_edad' : (FieldType.ONE_FIELD, '487900000000000000000014', 'float'),
                'sitios' : (FieldType.ONE_FIELD, '487900000000000000000015', ''),
                'alimento' : (FieldType.ONE_FIELD, '487900000000000000000016', ''),
                'consumo_alimento' : (FieldType.ONE_FIELD, '487900000000000000000017', 'float'),
                'peso_desecho' : (FieldType.ONE_FIELD, '487900000000000000000018', 'float'),
                'porcentaje_desecho' : (FieldType.ONE_FIELD, '487900000000000000000019', 'float'),
                'inventario_inicial' : (FieldType.ONE_FIELD, '487900000000000000000020', 'float'),
                'inventario_final' : (FieldType.ONE_FIELD, '487900000000000000000021', 'float'),
                'inventario_desecho' : (FieldType.ONE_FIELD, '487900000000000000000022', 'float'),
                'inventario_retrasado' : (FieldType.ONE_FIELD, '487900000000000000000023', 'float'),
                'cantidad_alimento_consumido' : (FieldType.ONE_FIELD, '487900000000000000000024', 'float'),
                'cantidad_alimento_acumulado' : (FieldType.ONE_FIELD, '487900000000000000000025', 'float')
            }],

            self.CAPACIDAD_LAGOS : [{
                'capacidad' : (FieldType.ONE_FIELD, '123400000000000000000001', 'float'),
                'granja' : (FieldType.ONE_FIELD, '123400000000000000000002', 'select')
            }],

            self.TESTING : [{
                'testing' : (FieldType.ONE_FIELD, '012345678901234567890123', ''),
                'testing2' : (FieldType.ONE_FIELD, '012345678901234567890124', '')
            }]

        }
        return form_id_fields_map[self.form_id]

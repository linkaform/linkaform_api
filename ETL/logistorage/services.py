#coding: utf-8

def get_query():
    query = [{"$match": {"itype":"service"}},# ,"559174f601a4de7bb94f87ed" : "SEPTIEMBRE",'5591627901a4de7bb8eb1ad4':'Monterrey' }},

            {"$group": {
           "_id": {
                     'currency': "$currency",
                     'client': "$5591627901a4de7bb8eb1ad5",
                     'warehouse': "$5591627901a4de7bb8eb1ad4",
                     'year': {"$year": "$created_at"},
                     'month':"$559174f601a4de7bb94f87ed",
              },
        'SAC_qty':{'$sum': "$5591627901a4de7bb8eb1ad9.qty"},
        'SAC_unit_price': {'$max': "$5591627901a4de7bb8eb1ad9.unit_price"},
        'SAC_total': {'$sum': "$5591627901a4de7bb8eb1ad9.total"},

        'SAC_no_charge_qty': { '$sum':{'$multiply': ["$5591627901a4de7bb8eb1ad9.qty",{ '$cond': [
                     {'$gt': ["$5591627901a4de7bb8eb1ae1.qty",0] }, 1, 0 ]}]}},

        'SAE_qty': {'$sum': "$559167ed01a4de7bba852991.qty"},
        'SAE_unit_price': {'$max': "$559167ed01a4de7bba852991.unit_price"},
        'SAE_total': {'$sum': "$559167ed01a4de7bba852991.total"},

        'SAD_qty': {'$sum': "$5591627901a4de7bb8eb1ada.qty"},
        'SAD_unit_price': {'$max': "$5591627901a4de7bb8eb1ada.unit_price"},
        'SAD_total': {'$sum': "$5591627901a4de7bb8eb1ada.total"},

        'SAP_qty': {'$sum': "$559167ed01a4de7bba852992.qty"},
        'SAP_unit_price': {'$max': "$559167ed01a4de7bba852992.unit_price"},
        'SAP_total': {'$sum': "$559167ed01a4de7bba852992.total"},

        'SE_qty': {'$sum': "$5591627901a4de7bb8eb1adb.qty"},
        'SE_unit_price': {'$max': "$5591627901a4de7bb8eb1adb.unit_price"},
        'SE_total': {'$sum': "$5591627901a4de7bb8eb1adb.total"},

        'SEPONY_qty': {'$sum': "$5591627901a4de7bb8eb1adc.qty"},
        'SEPONY_unit_price': {'$max': "$5591627901a4de7bb8eb1adc.unit_price"},
        'SEPONY_total': {'$sum': "$5591627901a4de7bb8eb1adc.total"},

        'SAT_qty': {'$sum': "$559167ed01a4de7bba852993.qty"},
        'SAT_unit_price': {'$max': "$559167ed01a4de7bba852993.unit_price"},
        'SAT_total': {'$sum': "$559167ed01a4de7bba852993.total"},

        'SPY_qty': {'$sum': "$559167ed01a4de7bba852994.qty"},
        'SPY_unit_price': {'$max': "$559167ed01a4de7bba852994.unit_price"},
        'SPY_total': {'$sum': "$559167ed01a4de7bba852994.total"},

        'TCH_qty': {'$sum': "$5591627901a4de7bb8eb1add.qty"},
        'TCH_unit_price': {'$max': "$5591627901a4de7bb8eb1add.unit_price"},
        'TCH_total': {'$sum': "$5591627901a4de7bb8eb1add.total"},

        'TCOSTCO_qty': {'$sum': "$5591627901a4de7bb8eb1ade.qty"},
        'TCOSTCO_unit_price': {'$max': "$5591627901a4de7bb8eb1ade.unit_price"},
        'TCOSTCO_total': {'$sum': "$5591627901a4de7bb8eb1ade.total"},

        'STD_qty': {'$sum': "$55916a6f01a4de7bba852997.qty"},
        'STD_unit_price': {'$max': "$55916a6f01a4de7bba852997.unit_price"},
        'STD_total': {'$sum': "$55916a6f01a4de7bba852997.total"},

        'TNL_qty': {'$sum': "$5591627901a4de7bb8eb1adf.qty"},
        'TNL_unit_price': {'$max': "$5591627901a4de7bb8eb1adf.unit_price"},
        'TNL_total': {'$sum': "$5591627901a4de7bb8eb1adf.total"},

        'TERMO_qty': {'$sum': "$5591627901a4de7bb8eb1ae0.qty"},
        'TERMO_unit_price': {'$max': "$5591627901a4de7bb8eb1ae0.unit_price"},
        'TERMO_total': {'$sum': "$5591627901a4de7bb8eb1ae0.total"},

        'SD_qty': {'$sum': "$55916a6f01a4de7bba852998.qty"},
        'SD_unit_price': {'$max': "$55916a6f01a4de7bba852998.unit_price"},
        'SD_total': {'$sum': "$55916a6f01a4de7bba852998.total"},

        'RM_qty': {'$sum': "$55916a6f01a4de7bba852999.qty"},
        'RM_unit_price': {'$max': "$55916a6f01a4de7bba852999.unit_price"},
        'RM_total': {'$sum': "$55916a6f01a4de7bba852999.total"},

        'PALLET_IN_qty': {'$sum': "$55916a6f01a4de7bba85299a.qty"},
        'PALLET_IN_unit_price': {'$max': "$55916a6f01a4de7bba85299a.unit_price"},
        'PALLET_IN_total': {'$sum': "$55916a6f01a4de7bba85299a.total"},

        'PALLET_OUT_qty': {'$sum': "$55916a6f01a4de7bba85299b.qty"},
        'PALLET_OUT_unit_price': {'$max': "$55916a6f01a4de7bba85299b.unit_price"},
        'PALLET_OUT_total': {'$sum': "$55916a6f01a4de7bba85299b.total"},

        'KIT_PLAYERAS_qty': {'$sum': "$55916a6f01a4de7bba85299c.qty"},
        'KIT_PLAYERAS_unit_price': {'$max': "$55916a6f01a4de7bba85299c.unit_price"},
        'KIT_PLAYERAS_total': {'$sum': "$55916a6f01a4de7bba85299c.total"},

        'SERVICIO_REEMPACADO_qty': {'$sum': "$55916a6f01a4de7bba85299d.qty"},
        'SERVICIO_REEMPACADO_unit_price': {'$max': "$55916a6f01a4de7bba85299d.unit_price"},
        'SERVICIO_REEMPACADO_total': {'$sum': "$55916a6f01a4de7bba85299d.total"},

        'SERVICIO_REETIQUETADO_qty': {'$sum': "$55916a6f01a4de7bba85299e.qty"},
        'SERVICIO_REETIQUETADO_unit_price': {'$max': "$55916a6f01a4de7bba85299e.unit_price"},
        'SERVICIO_REETIQUETADO_total': {'$sum': "$55916a6f01a4de7bba85299e.total"},

        'SAEXH_qty': {'$sum': "$55916a6f01a4de7bba85299f.qty"},
        'SAEXH_unit_price': {'$max': "$55916a6f01a4de7bba85299f.unit_price"},
        'SAEXH_total': {'$sum': "$55916a6f01a4de7bba85299f.total"},

        'MI_qty': {'$sum': "$55916a6f01a4de7bba8529a0.qty"},
        'MI_unit_price': {'$max': "$55916a6f01a4de7bba8529a0.unit_price"},
        'MI_total': {'$sum': "$55916a6f01a4de7bba8529a0.total"},

        'TARIMA_NEGRA_MILLER_qty': {'$sum': "$5591627901a4de7bb8eb1ae1.qty"},
        'TARIMA_NEGRA_MILLER_unit_price': {'$max': "$5591627901a4de7bb8eb1ae1.unit_price"},
        'TARIMA_NEGRA_MILLER_total': {'$sum': "$5591627901a4de7bb8eb1ae1.total"},

        'MANO_OBRA_qty': {'$sum': "$5591627901a4de7bb8eb1ae2.qty"},
        'MANO_OBRA_unit_price': {'$max': "$5591627901a4de7bb8eb1ae2.unit_price"},
        'MANO_OBRA_total': {'$sum': "$5591627901a4de7bb8eb1ae2.total"},

        'PICK_AND_PACK_qty': {'$sum': "$55916a6f01a4de7bba8529a1.qty"},
        'PICK_AND_PACK_unit_price': {'$max': "$55916a6f01a4de7bba8529a1.unit_price"},
        'PICK_AND_PACK_total': {'$sum': "$55916a6f01a4de7bba8529a1.total"},

        'ENTRADA_DETALLE_qty': {'$sum': "$55916a6f01a4de7bba8529a2.qty"},
        'ENTRADA_DETALLE_unit_price': {'$max': "$55916a6f01a4de7bba8529a2.unit_price"},
        'ENTRADA_DETALLE_total': {'$sum': "$55916a6f01a4de7bba8529a2.total"},

        'FLEJE_VENTA_qty': {'$sum': "$55cb86f423d3fd09737bcc1a.qty"},
        'FLEJE_VENTA_unit_price': {'$max': "$55cb86f423d3fd09737bcc1a.unit_price"},
        'FLEJE_VENTA_total': {'$sum': "$55cb86f423d3fd09737bcc1a.total"},

#        "55cb692523d3fd4818dd2195":"55cb786023d3fd4818dd21b7",
        'PERSONAL_DEDICADO_PROYECTO_qty': {'$sum': "$55cb692523d3fd4818dd2195.qty"},
        'PERSONAL_DEDICADO_PROYECTO_unit_price': {'$max': "$55cb692523d3fd4818dd2195.unit_price"},
        'PERSONAL_DEDICADO_PROYECTO_total': {'$sum': "$55cb692523d3fd4818dd2195.total"},

        'CROSS_DOCK_qty': {'$sum': "$55cb692523d3fd4818dd2196.qty"},
        'CROSS_DOCK_unit_price': {'$max': "$55cb692523d3fd4818dd2196.unit_price"},
        'CROSS_DOCK_total': {'$sum': "$55cb692523d3fd4818dd2196.total"},

        'CROSS_DOCK_20_qty': {'$sum': "$55cb692523d3fd4818dd2197.qty"},
        'CROSS_DOCK_20_unit_price': {'$max': "$55cb692523d3fd4818dd2197.unit_price"},
        'CROSS_DOCK_20_total': {'$sum': "$55cb692523d3fd4818dd2197.total"},

        'CROSS_DOCK_40_qty': {'$sum': "$55cb692523d3fd4818dd2198.qty"},
        'CROSS_DOCK_40_unit_price': {'$max': "$55cb692523d3fd4818dd2198.unit_price"},
        'CROSS_DOCK_40_total': {'$sum': "$55cb692523d3fd4818dd2198.total"},

        'ALMACENAJE_TARIMA_qty': {'$sum': "$55cb692523d3fd4818dd2199.qty"},
        'ALMACENAJE_TARIMA_unit_price': {'$max': "$55cb692523d3fd4818dd2199.unit_price"},
        'ALMACENAJE_TARIMA_total': {'$sum': "$55cb692523d3fd4818dd2199.total"},

        'TIEMPO_EXTRA_X_HORA_qty': {'$sum': "$55cb692523d3fd4818dd219a.qty"},
        'TIEMPO_EXTRA_X_HORA_unit_price': {'$max': "$55cb692523d3fd4818dd219a.unit_price"},
        'TIEMPO_EXTRA_X_HORA_total': {'$sum': "$55cb692523d3fd4818dd219a.total"},

        'CROSS_DOCK_20_NOCTURNO_qty': {'$sum': "$55cb692523d3fd4818dd219b.qty"},
        'CROSS_DOCK_20_NOCTURNO_unit_price': {'$max': "$55cb692523d3fd4818dd219b.unit_price"},
        'CROSS_DOCK_20_NOCTURNO_total': {'$sum': "$55cb692523d3fd4818dd219b.total"},

        'CROSS_DOCK_40_NOCTURNO_qty': {'$sum': "$55cb692523d3fd4818dd219c.qty"},
        'CROSS_DOCK_40_NOCTURNO_unit_price': {'$max': "$55cb692523d3fd4818dd219c.unit_price"},
        'CROSS_DOCK_40_NOCTURNO_total': {'$sum': "$55cb692523d3fd4818dd219c.total"},

        'TIEMPO_EXTRA_X_HORA_NOCTURNO_qty': {'$sum': "$55cb692523d3fd4818dd219d.qty"},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_unit_price': {'$max': "$55cb692523d3fd4818dd219d.unit_price"},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_total': {'$sum': "$55cb692523d3fd4818dd219d.total"},

        'CROSS_DOCK_40_2_qty': {'$sum': "$55cb692523d3fd4818dd219e.qty"},
        'CROSS_DOCK_40_2_unit_price': {'$max': "$55cb692523d3fd4818dd219e.unit_price"},
        'CROSS_DOCK_40_2_total': {'$sum': "$55cb692523d3fd4818dd219e.total"},

        'SAP_MAS_15_qty': {'$sum': "$55cb692523d3fd4818dd219f.qty"},
        'SAP_MAS_15_unit_price': {'$max': "$55cb692523d3fd4818dd219f.unit_price"},
        'SAP_MAS_15_total': {'$sum': "$55cb692523d3fd4818dd219f.total"},

        'SAP_MENOS_15_qty': {'$sum': "$55cb692523d3fd4818dd21a0.qty"},
        'SAP_MENOS_15_unit_price': {'$max': "$55cb692523d3fd4818dd21a0.unit_price"},
        'SAP_MENOS_15_total': {'$sum': "$55cb692523d3fd4818dd21a0.total"},

        'SERVICIO_ARMADO_CARRETES_qty': {'$sum': "$55cb692523d3fd4818dd21a1.qty"},
        'SERVICIO_ARMADO_CARRETES_unit_price': {'$max': "$55cb692523d3fd4818dd21a1.unit_price"},
        'SERVICIO_ARMADO_CARRETES_total': {'$sum': "$55cb692523d3fd4818dd21a1.total"},

        'SERVICIO_ARMADO_CARRETES_URGENTES_qty': {'$sum': "$55cb692523d3fd4818dd21a2.qty"},
        'SERVICIO_ARMADO_CARRETES_URGENTES_unit_price': {'$max': "$55cb692523d3fd4818dd21a2.unit_price"},
        'SERVICIO_ARMADO_CARRETES_URGENTES_total': {'$sum': "$55cb692523d3fd4818dd21a2.total"},

        'UNIDAD_ESPACIO_TEMPORAL_qty': {'$sum': "$55cb7f0923d3fd0328736629.qty"},
        'UNIDAD_ESPACIO_TEMPORAL_unit_price': {'$max': "$55cb7f0923d3fd0328736629.unit_price"},
        'UNIDAD_ESPACIO_TEMPORAL_total': {'$sum': "$55cb7f0923d3fd0328736629.total"},

        'COSTO_MENSUAL_UE_qty': {'$sum': "$558db23301a4de7bba8528e5.qty"},
        'COSTO_MENSUAL_UE_unit_price': {'$max': "$558db23301a4de7bba8528e5.unit_price"},
        'COSTO_MENSUAL_UE_total': {'$sum': "$558db23301a4de7bba8528e5.total"},

        'COSTO_MENSUAL_UE_EXTRA_qty': {'$sum': "$55c5392c23d3fd4817ed01d0.qty"},
        'COSTO_MENSUAL_UE_EXTRA_unit_price': {'$max': "$55c5392c23d3fd4817ed01d0.unit_price"},
        'COSTO_MENSUAL_UE_EXTRA_total': {'$sum': "$55c5392c23d3fd4817ed01d0.total"},

        'PRECIO_TIEMPO_EXTRA_X_DIA_qty': {'$sum': "$5594677423d3fd7d311a4580.qty"},
        'PRECIO_TIEMPO_EXTRA_X_DIA_unit_price': {'$max': "$5594677423d3fd7d311a4580.unit_price"},
        'PRECIO_TIEMPO_EXTRA_X_DIA_total': {'$sum': "$5594677423d3fd7d311a4580.total"},

        'PRECIO_RENTA_FIJA_qty': {'$sum': "$5595a5ae23d3fd7d304980c3.qty"},
        'PRECIO_RENTA_FIJA_unit_price': {'$max': "$5595a5ae23d3fd7d304980c3.unit_price"},
        'PRECIO_RENTA_FIJA_total': {'$sum': "$5595a5ae23d3fd7d304980c3.total"},

        'PRECIO_RENTA_OFICINA_qty': {'$sum': "$5594688623d3fd7d311a4583.qty"},
        'PRECIO_RENTA_OFICINA_unit_price': {'$max': "$5594688623d3fd7d311a4583.unit_price"},
        'PRECIO_RENTA_OFICINA_total': {'$sum': "$5594688623d3fd7d311a4583.total"},

        'METROS_ACORDADOS_qty': {'$sum': "$5594688623d3fd7d311a4584.qty"},
        'METROS_ACORDADOS_unit_price': {'$max': "$5594688623d3fd7d311a4584.unit_price"},
        'METROS_ACORDADOS_total': {'$sum': "$5594688623d3fd7d311a4584.total"},
        #Nuevos Servicios
        'SD_DESCARGA_35_qty': {'$sum': "$55db956d23d3fd30f2ce9dec.qty"},
        'SD_DESCARGA_35_unit_price': {'$max': "$55db956d23d3fd30f2ce9dec.unit_price"},
        'SD_DESCARGA_35_total': {'$sum': "$55db956d23d3fd30f2ce9dec.total"},

        'SD_DESCARGA_TORTON_qty': {'$sum': "$55db956d23d3fd30f2ce9ded.qty"},
        'SD_DESCARGA_TORTON_unit_price': {'$max': "$55db956d23d3fd30f2ce9ded.unit_price"},
        'SD_DESCARGA_TORTON_total': {'$sum': "$55db956d23d3fd30f2ce9ded.total"},

        'SD_DESCARGA_TRAILER_qty': {'$sum': "$55db956d23d3fd30f2ce9dee.qty"},
        'SD_DESCARGA_TRAILER_unit_price': {'$max': "$55db956d23d3fd30f2ce9dee.unit_price"},
        'SD_DESCARGA_TRAILER_total': {'$sum': "$55db956d23d3fd30f2ce9dee.total"},

        'CM_CARGA_MATERIAL_35_qty': {'$sum': "$55db956d23d3fd30f2ce9def.qty"},
        'CM_CARGA_MATERIAL_35_unit_price': {'$max': "$55db956d23d3fd30f2ce9def.unit_price"},
        'CM_CARGA_MATERIAL_35_total': {'$sum': "$55db956d23d3fd30f2ce9def.total"},

        'CM_CARGA_MATERIAL_TORTON_qty': {'$sum': "$55db956d23d3fd30f2ce9df0.qty"},
        'CM_CARGA_MATERIAL_TORTON_unit_price': {'$max': "$55db956d23d3fd30f2ce9df0.unit_price"},
        'CM_CARGA_MATERIAL_TORTON_total': {'$sum': "$55db956d23d3fd30f2ce9df0.total"},

        'CM_CARGA_MATERIAL_TRAILER_qty': {'$sum': "$55db956d23d3fd30f2ce9df1.qty"},
        'CM_CARGA_MATERIAL_TRAILER_unit_price': {'$max': "$55db956d23d3fd30f2ce9df1.unit_price"},
        'CM_CARGA_MATERIAL_TRAILER_total': {'$sum': "$55db956d23d3fd30f2ce9df1.total"},

        'TARIFA_GUIA_qty': {'$sum': "$55db5bd923d3fd157a97dfd6.qty"},
        'TARIFA_GUIA_unit_price': {'$max': "$55db5bd923d3fd157a97dfd6.unit_price"},
        'TARIFA_GUIA_total': {'$sum': "$55db5bd923d3fd157a97dfd6.total"},

        'TARIMAS_NEGRAS_FLEJADAS_qty': {'$sum': "$55fb84cf23d3fd7817c11955.qty"},
        'TARIMAS_NEGRAS_FLEJADAS_unit_price': {'$max': "$55fb84cf23d3fd7817c11955.unit_price"},
        'TARIMAS_NEGRAS_FLEJADAS_total': {'$sum': "$55fb84cf23d3fd7817c11955.total"},

    }},

    {'$project': {
        '_id' : 1,

        'SAC_total_org':{'$multiply': ["$SAC_qty","$SAC_unit_price"]},
        'SAC_total': {'$add':[
                                {'$multiply': ["$SAC_qty","$SAC_unit_price"]},
                                {'$multiply': ["$SAC_no_charge_qty", -1, { '$cond': [{'$gt': ["$SAC_unit_price",0] },'$SAC_unit_price' , 0 ]}]}
                            ]
                        },
        'SAC_no_charge_total':  {'$multiply': ["$SAC_no_charge_qty", -1, { '$cond': [{'$gt': ["$SAC_unit_price",0] },'$SAC_unit_price' , 0 ]}]},

        #'SAC_no_charge_total' : {'$multiply': ["$SAC_no_charge_qty","$SAC_unit_price"]},
        'SAC_total2': {'$multiply': ["$SAE_qty","$SAE_unit_price"]},
        'SAE_total' : {'$multiply': ["$SAE_qty","$SAE_unit_price"]},

        'SAD_total': {'$multiply': ["$SAD_qty","$SAD_unit_price"]},

        'SAP_total':  {'$multiply': ["$SAP_qty","$SAP_unit_price"]},

        'SE_total': {'$multiply': ["$SE_qty","$SE_unit_price"]},

        'SEPONY_total': {'$multiply': ["$SEPONY_qty","$SEPONY_unit_price"]},

        'SAT_total': {'$multiply': ["$SAT_qty","$SAT_unit_price"]},

        'SPY_total': {'$multiply': ["$SPY_qty","$SPY_unit_price"]},

        'TCH_total': {'$multiply': ["$TCH_qty","$TCH_unit_price"]},

        'TCOSTCO_total': {'$multiply': ["$TCOSTCO_qty","$TCOSTCO_unit_price"]},

        'STD_total': {'$multiply': ["$STD_qty","$STD_unit_price"]},

        'TNL_total': {'$multiply': ["$TNL_qty","$TNL_unit_price"]},

        'TERMO_total': {'$multiply': ["$TERMO_qty","$TERMO_unit_price"]},

        'SD_total': {'$multiply': ["$SD_qty","$SD_unit_price"]},

        'RM_total': {'$multiply': ["$RM_qty","$RM_unit_price"]},

        'PALLET_IN_total': {'$multiply': ["$PALLET_IN_qty","$PALLET_IN_unit_price"]},

        'PALLET_OUT_total': {'$multiply': ["$PALLET_OUT_qty","$PALLET_OUT_unit_price"]},

        'KIT_PLAYERAS_total': {'$multiply': ["$KIT_PLAYERAS_qty","$KIT_PLAYERAS_unit_price"]},

        'SERVICIO_REEMPACADO_total': {'$multiply': ["$SERVICIO_REEMPACADO_qty","$SERVICIO_REEMPACADO_unit_price"]},

        'SERVICIO_REETIQUETADO_total': {'$multiply': ["$SERVICIO_REETIQUETADO_qty","$SERVICIO_REETIQUETADO_unit_price"]},

        'SAEXH_total': {'$multiply': ["$SAEXH_qty","$SAEXH_unit_price"]},

        'MI_total': {'$multiply': ["$MI_qty","$MI_unit_price"]},

        'TARIMA_NEGRA_MILLER_total': {'$multiply': ["$TARIMA_NEGRA_MILLER_qty","$TARIMA_NEGRA_MILLER_unit_price"]},

        'MANO_OBRA_total': {'$multiply': ["$MANO_OBRA_qty","$MANO_OBRA_unit_price"]},

        'PICK_AND_PACK_total': {'$multiply': ["$PICK_AND_PACK_qty","$PICK_AND_PACK_unit_price"]},

        'ENTRADA_DETALLE_total': {'$multiply': ["$ENTRADA_DETALLE_qty","$ENTRADA_DETALLE_unit_price"]},

        'FLEJE_VENTA_total': {'$multiply': ["$FLEJE_VENTA_qty","$FLEJE_VENTA_unit_price"]},

        'PERSONAL_DEDICADO_PROYECTO_total': {'$multiply': ["$PERSONAL_DEDICADO_PROYECTO_qty","$PERSONAL_DEDICADO_PROYECTO_unit_price"]},

        'CROSS_DOCK_total': {'$multiply': ["$CROSS_DOCK_qty","$CROSS_DOCK_unit_price"]},

        'CROSS_DOCK_20_total': {'$multiply': ["$CROSS_DOCK_20_qty","$CROSS_DOCK_20_unit_price"]},

        'CROSS_DOCK_40_total': {'$multiply': ["$CROSS_DOCK_40_qty","$CROSS_DOCK_40_unit_price"]},

        'ALMACENAJE_TARIMA_total': {'$multiply': ["$ALMACENAJE_TARIMA_qty","$ALMACENAJE_TARIMA_unit_price"]},

        'TIEMPO_EXTRA_X_HORA_total': {'$multiply': ["$TIEMPO_EXTRA_X_HORA_qty","$TIEMPO_EXTRA_X_HORA_unit_price"]},

        'CROSS_DOCK_20_NOCTURNO_total': {'$multiply': ["$CROSS_DOCK_20_NOCTURNO_qty","$CROSS_DOCK_20_NOCTURNO_unit_price"]},

        'CROSS_DOCK_40_NOCTURNO_total': {'$multiply': ["$CROSS_DOCK_40_NOCTURNO_qty","$CROSS_DOCK_40_NOCTURNO_unit_price"]},

        'TIEMPO_EXTRA_X_HORA_NOCTURNO_total': {'$multiply': ["$TIEMPO_EXTRA_X_HORA_NOCTURNO_qty","$TIEMPO_EXTRA_X_HORA_NOCTURNO_unit_price"]},

        'CROSS_DOCK_40_2_total': {'$multiply': ["$CROSS_DOCK_40_2_qty","$CROSS_DOCK_40_2_unit_price"]},

        'SAP_MAS_15_total': {'$multiply': ["$SAP_MAS_15_qty","$SAP_MAS_15_unit_price"]},

        'SERVICIO_ARMADO_CARRETES_total': {'$multiply': ["$SERVICIO_ARMADO_CARRETES_qty","$SERVICIO_ARMADO_CARRETES_unit_price"]},

        'SERVICIO_ARMADO_CARRETES_URGENTES_total': {'$multiply': ["$SERVICIO_ARMADO_CARRETES_URGENTES_qty","$SERVICIO_ARMADO_CARRETES_URGENTES_unit_price"]},

        'UNIDAD_ESPACIO_TEMPORAL_total': {'$multiply': ["$UNIDAD_ESPACIO_TEMPORAL_qty","$UNIDAD_ESPACIO_TEMPORAL_unit_price"]},

        'COSTO_MENSUAL_UE_total': {'$multiply': ["$COSTO_MENSUAL_UE_qty","$COSTO_MENSUAL_UE_unit_price"]},

        'COSTO_MENSUAL_UE_EXTRA_total': {'$multiply': ["$COSTO_MENSUAL_UE_EXTRA_qty","$COSTO_MENSUAL_UE_EXTRA_unit_price"]},

        'PRECIO_TIEMPO_EXTRA_X_DIA_total': {'$multiply': ["$PRECIO_TIEMPO_EXTRA_X_DIA_qty","$PRECIO_TIEMPO_EXTRA_X_DIA_unit_price"]},

        'PRECIO_RENTA_FIJA_total': {'$multiply': ["$PRECIO_RENTA_FIJA_qty","$PRECIO_RENTA_FIJA_unit_price"]},

        'PRECIO_RENTA_OFICINA_total': {'$multiply': ["$PRECIO_RENTA_OFICINA_qty","$PRECIO_RENTA_OFICINA_unit_price"]},

        'METROS_ACORDADOS_total': {'$multiply': ["$METROS_ACORDADOS_qty","$METROS_ACORDADOS_unit_price"]},

        'SD_DESCARGA_35_total': {'$multiply': ["$SD_DESCARGA_35_qty","$SD_DESCARGA_35_unit_price"]},
        'SD_DESCARGA_TORTON_total': {'$multiply': ["$SD_DESCARGA_TORTON_qty","$SD_DESCARGA_TORTON_unit_price"]},
        'SD_DESCARGA_TRAILER_total': {'$multiply': ["$SD_DESCARGA_TRAILER_qty","$SD_DESCARGA_TRAILER_unit_price"]},
        'CM_CARGA_MATERIAL_35_total': {'$multiply': ["$CM_CARGA_MATERIAL_35_qty","$CM_CARGA_MATERIAL_35_unit_price"]},
        'CM_CARGA_MATERIAL_TORTON_total': {'$multiply': ["$CM_CARGA_MATERIAL_TORTON_qty","$CM_CARGA_MATERIAL_TORTON_unit_price"]},
        'CM_CARGA_MATERIAL_TRAILER_total': {'$multiply': ["$CM_CARGA_MATERIAL_TRAILER_qty","$CM_CARGA_MATERIAL_TRAILER_unit_price"]},
        'TARIFA_GUIA_total': {'$multiply': ["$TARIFA_GUIA_qty","$TARIFA_GUIA_unit_price"]},
        'TARIMAS_NEGRAS_FLEJADAS_total': {'$multiply': ["$TARIMAS_NEGRAS_FLEJADAS_qty","$TARIMAS_NEGRAS_FLEJADAS_unit_price"]},

        'total_services': {'$add': [ '$SAE_total' , '$SAD_total', '$SAP_total', '$SE_total', '$SEPONY_total','$SAT_total', '$SPY_total', '$TCH_total',
        '$TCOSTCO_total', '$STD_total','$TNL_total','$TERMO_total', '$SD_total','$RM_total','$PALLET_IN_total','$PALLET_OUT_total',
        '$KIT_PLAYERAS_total','$SERVICIO_REEMPACADO_total','$SERVICIO_REETIQUETADO_total','$SAEXH_total','$MI_total','$TARIMA_NEGRA_MILLER_total',
        '$MANO_OBRA_total','$PICK_AND_PACK_total','$ENTRADA_DETALLE_total','$FLEJE_VENTA_total',
        '$PERSONAL_DEDICADO_PROYECTO_total','$CROSS_DOCK_total','$CROSS_DOCK_20_total','$CROSS_DOCK_40_total',
        '$ALMACENAJE_TARIMA_total','$TIEMPO_EXTRA_X_HORA_total','$CROSS_DOCK_20_NOCTURNO_total','$CROSS_DOCK_40_NOCTURNO_total',
        '$TIEMPO_EXTRA_X_HORA_NOCTURNO_total','$CROSS_DOCK_40_2_total','$SAP_MAS_15_total','$SERVICIO_ARMADO_CARRETES_total',
        '$SERVICIO_ARMADO_CARRETES_URGENTES_total','$UNIDAD_ESPACIO_TEMPORAL_total','$COSTO_MENSUAL_UE_total',
        '$COSTO_MENSUAL_UE_EXTRA_total','$PRECIO_TIEMPO_EXTRA_X_DIA_total','$PRECIO_RENTA_FIJA_total',
        '$PRECIO_RENTA_OFICINA_total','$METROS_ACORDADOS_total','$SD_DESCARGA_35_total','$SD_DESCARGA_TORTON_total',
        '$SD_DESCARGA_TRAILER_total','$CM_CARGA_MATERIAL_35_total', '$CM_CARGA_MATERIAL_TORTON_total',
        '$CM_CARGA_MATERIAL_TRAILER_total','$TARIFA_GUIA_total','$TARIMAS_NEGRAS_FLEJADAS_total'  ]}
        }},
        {'$project':{
        '_id':1,
        'total_services':{'$add':["$total_services", { '$cond': [{'$gt': ["$SAC_total",0] },"$SAC_total" , 0 ]}]},
        'total_office_rent' : {'$add':[0.0]},
        'total_fixed_rent':{'$add':[0.0]},
        'total_space_unit' : {'$add':[0.0]}

    }}
    ]
    return query

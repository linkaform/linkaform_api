#coding: utf-8

def get_query():
    query = [{"$match": {"itype":"service"}},
    
            {"$group": {
           "_id": {

                     'client': "$5591627901a4de7bb8eb1ad5",
                     'warehouse': "$5591627901a4de7bb8eb1ad4",
                     'year': {"$year": "$created_at"},
                     'month':"$559174f601a4de7bb94f87ed",
              },
        'SAC_qty':{'$sum': "$5591627901a4de7bb8eb1ad9.qty"},
        'SAC_unit_price': {'$max': "$5591627901a4de7bb8eb1ad9.unit_price"},
        'SAC_currency': {'$last': "$5591627901a4de7bb8eb1ad9.currency"},
        'SAC_total': {'$sum': "$5591627901a4de7bb8eb1ad9.total"},

        'SAE_qty': {'$sum': "$559167ed01a4de7bba852991.qty"},
        'SAE_unit_price': {'$max': "$559167ed01a4de7bba852991.unit_price"},
        'SAE_currency': {'$last': "$559167ed01a4de7bba852991.currency"},
        'SAE_total': {'$sum': "$559167ed01a4de7bba852991.total"},

        'SAD_qty': {'$sum': "$5591627901a4de7bb8eb1ada.qty"},
        'SAD_unit_price': {'$max': "$5591627901a4de7bb8eb1ada.unit_price"},
        'SAD_currency': {'$last': "$5591627901a4de7bb8eb1ada.currency"},
        'SAD_total': {'$sum': "$5591627901a4de7bb8eb1ada.total"},

        'SAP_qty': {'$sum': "$559167ed01a4de7bba852992.qty"},
        'SAP_unit_price': {'$max': "$559167ed01a4de7bba852992.unit_price"},
        'SAP_currency': {'$last': "$559167ed01a4de7bba852992.currency"},
        'SAP_total': {'$sum': "$559167ed01a4de7bba852992.total"},

        'SE_qty': {'$sum': "$5591627901a4de7bb8eb1adb.qty"},
        'SE_unit_price': {'$max': "$5591627901a4de7bb8eb1adb.unit_price"},
        'SE_currency': {'$last': "$5591627901a4de7bb8eb1adb.currency"},
        'SE_total': {'$sum': "$5591627901a4de7bb8eb1adb.total"},

        'SEPONY_qty': {'$sum': "$5591627901a4de7bb8eb1adc.qty"},
        'SEPONY_unit_price': {'$max': "$5591627901a4de7bb8eb1adc.unit_price"},
        'SEPONY_currency': {'$last': "$5591627901a4de7bb8eb1adc.currency"},
        'SEPONY_total': {'$sum': "$5591627901a4de7bb8eb1adc.total"},

        'SAT_qty': {'$sum': "$559167ed01a4de7bba852993.qty"},
        'SAT_unit_price': {'$max': "$559167ed01a4de7bba852993.unit_price"},
        'SAT_currency': {'$last': "$559167ed01a4de7bba852993.currency"},
        'SAT_total': {'$sum': "$559167ed01a4de7bba852993.total"},

        'SPY_qty': {'$sum': "$559167ed01a4de7bba852994.qty"},
        'SPY_unit_price': {'$max': "$559167ed01a4de7bba852994.unit_price"},
        'SPY_currency': {'$last': "$559167ed01a4de7bba852994.currency"},
        'SPY_total': {'$sum': "$559167ed01a4de7bba852994.total"},

        'TCH_qty': {'$sum': "$5591627901a4de7bb8eb1add.qty"},
        'TCH_unit_price': {'$max': "$5591627901a4de7bb8eb1add.unit_price"},
        'TCH_currency': {'$last': "$5591627901a4de7bb8eb1add.currency"},
        'TCH_total': {'$sum': "$5591627901a4de7bb8eb1add.total"},

        'TCOSTCO_qty': {'$sum': "$5591627901a4de7bb8eb1ade.qty"},
        'TCOSTCO_unit_price': {'$max': "$5591627901a4de7bb8eb1ade.unit_price"},
        'TCOSTCO_currency': {'$last': "$5591627901a4de7bb8eb1ade.currency"},
        'TCOSTCO_total': {'$sum': "$5591627901a4de7bb8eb1ade.total"},

        'STD_qty': {'$sum': "$55916a6f01a4de7bba852997.qty"},
        'STD_unit_price': {'$max': "$55916a6f01a4de7bba852997.unit_price"},
        'STD_currency': {'$last': "$55916a6f01a4de7bba852997.currency"},
        'STD_total': {'$sum': "$55916a6f01a4de7bba852997.total"},

        'TNL_qty': {'$sum': "$5591627901a4de7bb8eb1adf.qty"},
        'TNL_unit_price': {'$max': "$5591627901a4de7bb8eb1adf.unit_price"},
        'TNL_currency': {'$last': "$5591627901a4de7bb8eb1adf.currency"},
        'TNL_total': {'$sum': "$5591627901a4de7bb8eb1adf.total"},

        'TERMO_qty': {'$sum': "$5591627901a4de7bb8eb1ae0.qty"},
        'TERMO_unit_price': {'$max': "$5591627901a4de7bb8eb1ae0.unit_price"},
        'TERMO_currency': {'$last': "$5591627901a4de7bb8eb1ae0.currency"},
        'TERMO_total': {'$sum': "$5591627901a4de7bb8eb1ae0.total"},

        'SD_qty': {'$sum': "$55916a6f01a4de7bba852998.qty"},
        'SD_unit_price': {'$max': "$55916a6f01a4de7bba852998.unit_price"},
        'SD_currency': {'$last': "$55916a6f01a4de7bba852998.currency"},
        'SD_total': {'$sum': "$55916a6f01a4de7bba852998.total"},

        'RM_qty': {'$sum': "$55916a6f01a4de7bba852999.qty"},
        'RM_unit_price': {'$max': "$55916a6f01a4de7bba852999.unit_price"},
        'RM_currency': {'$last': "$55916a6f01a4de7bba852999.currency"},
        'RM_total': {'$sum': "$55916a6f01a4de7bba852999.total"},

        'PALLET_IN_qty': {'$sum': "$55916a6f01a4de7bba85299a.qty"},
        'PALLET_IN_unit_price': {'$max': "$55916a6f01a4de7bba85299a.unit_price"},
        'PALLET_IN_currency': {'$last': "$55916a6f01a4de7bba85299a.currency"},
        'PALLET_IN_total': {'$sum': "$55916a6f01a4de7bba85299a.total"},

        'PALLET_OUT_qty': {'$sum': "$55916a6f01a4de7bba85299b.qty"},
        'PALLET_OUT_unit_price': {'$max': "$55916a6f01a4de7bba85299b.unit_price"},
        'PALLET_OUT_currency': {'$last': "$55916a6f01a4de7bba85299b.currency"},
        'PALLET_OUT_total': {'$sum': "$55916a6f01a4de7bba85299b.total"},

        'KIT_PLAYERAS_qty': {'$sum': "$55916a6f01a4de7bba85299c.qty"},
        'KIT_PLAYERAS_unit_price': {'$max': "$55916a6f01a4de7bba85299c.unit_price"},
        'KIT_PLAYERAS_currency': {'$last': "$55916a6f01a4de7bba85299c.currency"},
        'KIT_PLAYERAS_total': {'$sum': "$55916a6f01a4de7bba85299c.total"},

        'SERVICIO_REEMPACADO_qty': {'$sum': "$55916a6f01a4de7bba85299d.qty"},
        'SERVICIO_REEMPACADO_unit_price': {'$max': "$55916a6f01a4de7bba85299d.unit_price"},
        'SERVICIO_REEMPACADO_currency': {'$last': "$55916a6f01a4de7bba85299d.currency"},
        'SERVICIO_REEMPACADO_total': {'$sum': "$55916a6f01a4de7bba85299d.total"},

        'SERVICIO_REETIQUETADO_qty': {'$sum': "$55916a6f01a4de7bba85299e.qty"},
        'SERVICIO_REETIQUETADO_unit_price': {'$max': "$55916a6f01a4de7bba85299e.unit_price"},
        'SERVICIO_REETIQUETADO_currency': {'$last': "$55916a6f01a4de7bba85299e.currency"},
        'SERVICIO_REETIQUETADO_total': {'$sum': "$55916a6f01a4de7bba85299e.total"},

        'SAEXH_qty': {'$sum': "$55916a6f01a4de7bba85299f.qty"},
        'SAEXH_unit_price': {'$max': "$55916a6f01a4de7bba85299f.unit_price"},
        'SAEXH_currency': {'$last': "$55916a6f01a4de7bba85299f.currency"},
        'SAEXH_total': {'$sum': "$55916a6f01a4de7bba85299f.total"},

        'MI_qty': {'$sum': "$55916a6f01a4de7bba8529a0.qty"},
        'MI_unit_price': {'$max': "$55916a6f01a4de7bba8529a0.unit_price"},
        'MI_currency': {'$last': "$55916a6f01a4de7bba8529a0.currency"},
        'MI_total': {'$sum': "$55916a6f01a4de7bba8529a0.total"},

        'TARIMA_NEGRA_MILLER_qty': {'$sum': "$5591627901a4de7bb8eb1ae1.qty"},
        'TARIMA_NEGRA_MILLER_unit_price': {'$max': "$5591627901a4de7bb8eb1ae1.unit_price"},
        'TARIMA_NEGRA_MILLER_currency': {'$last': "$5591627901a4de7bb8eb1ae1.currency"},
        'TARIMA_NEGRA_MILLER_total': {'$sum': "$5591627901a4de7bb8eb1ae1.total"},

        'MANO_OBRA_qty': {'$sum': "$5591627901a4de7bb8eb1ae2.qty"},
        'MANO_OBRA_unit_price': {'$max': "$5591627901a4de7bb8eb1ae2.unit_price"},
        'MANO_OBRA_currency': {'$last': "$5591627901a4de7bb8eb1ae2.currency"},
        'MANO_OBRA_total': {'$sum': "$5591627901a4de7bb8eb1ae2.total"},

        'PICK_AND_PACK_qty': {'$sum': "$55916a6f01a4de7bba8529a1.qty"},
        'PICK_AND_PACK_unit_price': {'$max': "$55916a6f01a4de7bba8529a1.unit_price"},
        'PICK_AND_PACK_currency': {'$last': "$55916a6f01a4de7bba8529a1.currency"},
        'PICK_AND_PACK_total': {'$sum': "$55916a6f01a4de7bba8529a1.total"},

        'ENTRADA_DETALLE_qty': {'$sum': "$55916a6f01a4de7bba8529a2.qty"},
        'ENTRADA_DETALLE_unit_price': {'$max': "$55916a6f01a4de7bba8529a2.unit_price"},
        'ENTRADA_DETALLE_currency': {'$last': "$55916a6f01a4de7bba8529a2.currency"},
        'ENTRADA_DETALLE_total': {'$sum': "$55916a6f01a4de7bba8529a2.total"},

        'FLEJE_VENTA_qty': {'$sum': "$55cb86f423d3fd09737bcc1a.qty"},
        'FLEJE_VENTA_unit_price': {'$max': "$55cb86f423d3fd09737bcc1a.unit_price"},
        'FLEJE_VENTA_currency': {'$last': "$55cb86f423d3fd09737bcc1a.currency"},
        'FLEJE_VENTA_total': {'$sum': "$55cb86f423d3fd09737bcc1a.total"},

        'PERSONAL_DEDICADO_PROYECTO_qty': {'$sum': "$55cb786023d3fd4818dd21b7.qty"},
        'PERSONAL_DEDICADO_PROYECTO_unit_price': {'$max': "$55cb786023d3fd4818dd21b7.unit_price"},
        'PERSONAL_DEDICADO_PROYECTO_currency': {'$last': "$55cb786023d3fd4818dd21b7.currency"},
        'PERSONAL_DEDICADO_PROYECTO_total': {'$sum': "$55cb786023d3fd4818dd21b7.total"},

        'CROSS_DOCK_qty': {'$sum': "$55c5389623d3fd4818dd1dad.qty"},
        'CROSS_DOCK_unit_price': {'$max': "$55c5389623d3fd4818dd1dad.unit_price"},
        'CROSS_DOCK_currency': {'$last': "$55c5389623d3fd4818dd1dad.currency"},
        'CROSS_DOCK_total': {'$sum': "$55c5389623d3fd4818dd1dad.total"},

        'CROSS_DOCK_20_qty': {'$sum': "$55cb786023d3fd4818dd21b8.qty"},
        'CROSS_DOCK_20_unit_price': {'$max': "$55cb786023d3fd4818dd21b8.unit_price"},
        'CROSS_DOCK_20_currency': {'$last': "$55cb786023d3fd4818dd21b8.currency"},
        'CROSS_DOCK_20_total': {'$sum': "$55cb786023d3fd4818dd21b8.total"},

        'CROSS_DOCK_40_qty': {'$sum': "$55cb786023d3fd4818dd21b9.qty"},
        'CROSS_DOCK_40_unit_price': {'$max': "$55cb786023d3fd4818dd21b9.unit_price"},
        'CROSS_DOCK_40_currency': {'$last': "$55cb786023d3fd4818dd21b9.currency"},
        'CROSS_DOCK_40_total': {'$sum': "$55cb786023d3fd4818dd21b9.total"},

        'ALMACENAJE_TARIMA_qty': {'$sum': "$55cb786023d3fd4818dd21ba.qty"},
        'ALMACENAJE_TARIMA_unit_price': {'$max': "$55cb786023d3fd4818dd21ba.unit_price"},
        'ALMACENAJE_TARIMA_currency': {'$last': "$55cb786023d3fd4818dd21ba.currency"},
        'ALMACENAJE_TARIMA_total': {'$sum': "$55cb786023d3fd4818dd21ba.total"},

        'TIEMPO_EXTRA_X_HORA_qty': {'$sum': "$55cb786023d3fd4818dd21bb.qty"},
        'TIEMPO_EXTRA_X_HORA_unit_price': {'$max': "$55cb786023d3fd4818dd21bb.unit_price"},
        'TIEMPO_EXTRA_X_HORA_currency': {'$last': "$55cb786023d3fd4818dd21bb.currency"},
        'TIEMPO_EXTRA_X_HORA_total': {'$sum': "$55cb786023d3fd4818dd21bb.total"},

        'CROSS_DOCK_20_NOCTURNO_qty': {'$sum': "$55cb786023d3fd4818dd21bc.qty"},
        'CROSS_DOCK_20_NOCTURNO_unit_price': {'$max': "$55cb786023d3fd4818dd21bc.unit_price"},
        'CROSS_DOCK_20_NOCTURNO_currency': {'$last': "$55cb786023d3fd4818dd21bc.currency"},
        'CROSS_DOCK_20_NOCTURNO_total': {'$sum': "$55cb786023d3fd4818dd21bc.total"},

        'CROSS_DOCK_40_NOCTURNO_qty': {'$sum': "$55cb786023d3fd4818dd21bd.qty"},
        'CROSS_DOCK_40_NOCTURNO_unit_price': {'$max': "$55cb786023d3fd4818dd21bd.unit_price"},
        'CROSS_DOCK_40_NOCTURNO_currency': {'$last': "$55cb786023d3fd4818dd21bd.currency"},
        'CROSS_DOCK_40_NOCTURNO_total': {'$sum': "$55cb786023d3fd4818dd21bd.total"},

        'TIEMPO_EXTRA_X_HORA_NOCTURNO_qty': {'$sum': "$55cb786023d3fd4818dd21be.qty"},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_unit_price': {'$max': "$55cb786023d3fd4818dd21be.unit_price"},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_currency': {'$last': "$55cb786023d3fd4818dd21be.currency"},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_total': {'$sum': "$55cb786023d3fd4818dd21be.total"},

        'CROSS_DOCK_40_2_qty': {'$sum': "$55cb786023d3fd4818dd21bf.qty"},
        'CROSS_DOCK_40_2_unit_price': {'$max': "$55cb786023d3fd4818dd21bf.unit_price"},
        'CROSS_DOCK_40_2_currency': {'$last': "$55cb786023d3fd4818dd21bf.currency"},
        'CROSS_DOCK_40_2_total': {'$sum': "$55cb786023d3fd4818dd21bf.total"},

        'SAP_MAS_15_qty': {'$sum': "$55cb786023d3fd4818dd21c0.qty"},
        'SAP_MAS_15_unit_price': {'$max': "$55cb786023d3fd4818dd21c0.unit_price"},
        'SAP_MAS_15_currency': {'$last': "$55cb786023d3fd4818dd21c0.currency"},
        'SAP_MAS_15_total': {'$sum': "$55cb786023d3fd4818dd21c0.total"},

        'SAP_MENOS_15_qty': {'$sum': "$55cb786023d3fd4818dd21c1.qty"},
        'SAP_MENOS_15_unit_price': {'$max': "$55cb786023d3fd4818dd21c1.unit_price"},
        'SAP_MENOS_15_currency': {'$last': "$55cb786023d3fd4818dd21c1.currency"},
        'SAP_MENOS_15_total': {'$sum': "$55cb786023d3fd4818dd21c1.total"},

        'SERVICIO_ARMADO_CARRETES_qty': {'$sum': "$55cb786023d3fd4818dd21c2.qty"},
        'SERVICIO_ARMADO_CARRETES_unit_price': {'$max': "$55cb786023d3fd4818dd21c2.unit_price"},
        'SERVICIO_ARMADO_CARRETES_currency': {'$last': "$55cb786023d3fd4818dd21c2.currency"},
        'SERVICIO_ARMADO_CARRETES_total': {'$sum': "$55cb786023d3fd4818dd21c2.total"},

        'SERVICIO_ARMADO_CARRETES_URGENTES_qty': {'$sum': "$55cb786023d3fd4818dd21c3.qty"},
        'SERVICIO_ARMADO_CARRETES_URGENTES_unit_price': {'$max': "$55cb786023d3fd4818dd21c3.unit_price"},
        'SERVICIO_ARMADO_CARRETES_URGENTES_currency': {'$last': "$55cb786023d3fd4818dd21c3.currency"},
        'SERVICIO_ARMADO_CARRETES_URGENTES_total': {'$sum': "$55cb786023d3fd4818dd21c3.total"},

        'UNIDAD_ESPACIO_TEMPORAL_qty': {'$sum': "$55cb7f5323d3fd032873662a.qty"},
        'UNIDAD_ESPACIO_TEMPORAL_unit_price': {'$max': "$55cb7f5323d3fd032873662a.unit_price"},
        'UNIDAD_ESPACIO_TEMPORAL_currency': {'$last': "$55cb7f5323d3fd032873662a.currency"},
        'UNIDAD_ESPACIO_TEMPORAL_total': {'$sum': "$55cb7f5323d3fd032873662a.total"},

        'COSTO_MENSUAL_UE_qty': {'$sum': "$558db23301a4de7bba8528e5.qty"},
        'COSTO_MENSUAL_UE_unit_price': {'$max': "$558db23301a4de7bba8528e5.unit_price"},
        'COSTO_MENSUAL_UE_currency': {'$last': "$558db23301a4de7bba8528e5.currency"},
        'COSTO_MENSUAL_UE_total': {'$sum': "$558db23301a4de7bba8528e5.total"},

        'COSTO_MENSUAL_UE_EXTRA_qty': {'$sum': "$55c5392c23d3fd4817ed01d0.qty"},
        'COSTO_MENSUAL_UE_EXTRA_unit_price': {'$max': "$55c5392c23d3fd4817ed01d0.unit_price"},
        'COSTO_MENSUAL_UE_EXTRA_currency': {'$last': "$55c5392c23d3fd4817ed01d0.currency"},
        'COSTO_MENSUAL_UE_EXTRA_total': {'$sum': "$55c5392c23d3fd4817ed01d0.total"},

        'PRECIO_TIEMPO_EXTRA_X_DIA_qty': {'$sum': "$5594677423d3fd7d311a4580.qty"},
        'PRECIO_TIEMPO_EXTRA_X_DIA_unit_price': {'$max': "$5594677423d3fd7d311a4580.unit_price"},
        'PRECIO_TIEMPO_EXTRA_X_DIA_currency': {'$last': "$5594677423d3fd7d311a4580.currency"},
        'PRECIO_TIEMPO_EXTRA_X_DIA_total': {'$sum': "$5594677423d3fd7d311a4580.total"},

        'PRECIO_RENTA_FIJA_qty': {'$sum': "$5595a5ae23d3fd7d304980c3.qty"},
        'PRECIO_RENTA_FIJA_unit_price': {'$max': "$5595a5ae23d3fd7d304980c3.unit_price"},
        'PRECIO_RENTA_FIJA_currency': {'$last': "$5595a5ae23d3fd7d304980c3.currency"},
        'PRECIO_RENTA_FIJA_total': {'$sum': "$5595a5ae23d3fd7d304980c3.total"},

        'PRECIO_RENTA_OFICINA_qty': {'$sum': "$5594688623d3fd7d311a4583.qty"},
        'PRECIO_RENTA_OFICINA_unit_price': {'$max': "$5594688623d3fd7d311a4583.unit_price"},
        'PRECIO_RENTA_OFICINA_currency': {'$last': "$5594688623d3fd7d311a4583.currency"},
        'PRECIO_RENTA_OFICINA_total': {'$sum': "$5594688623d3fd7d311a4583.total"},

        'METROS_ACORDADOS_qty': {'$sum': "$5594688623d3fd7d311a4584.qty"},
        'METROS_ACORDADOS_unit_price': {'$max': "$5594688623d3fd7d311a4584.unit_price"},
        'METROS_ACORDADOS_currency': {'$last': "$5594688623d3fd7d311a4584.currency"},
        'METROS_ACORDADOS_total': {'$sum': "$5594688623d3fd7d311a4584.total"}
    }},

    {'$project': {
        '_id' : 1,

        'SAC_total': {'$multiply': ["$SAC_qty","$SAC_unit_price"]},
        'SAC_currency' : "$SAC_currency",

        'SAE_total' : {'$multiply': ["$SAE_qty","$SAE_unit_price"]},
        'SAE_currency' : "$SAE_currency",

        'SAD_total': {'$multiply': ["$SAD_qty","$SAD_unit_price"]},
        'SAD_currency' : "$SAD_currency",

        'SAP_total':  {'$multiply': ["$SAP_qty","$SAP_unit_price"]},
        'SAP_currency' : "$SAP_currency",

        'SE_total': {'$multiply': ["$SE_qty","$SE_unit_price"]},
        'SE_currency' : "$SE_currency",

        'SEPONY_total': {'$multiply': ["$SEPONY_qty","$SEPONY_unit_price"]},
        'SEPONY_currency' : "$SEPONY_currency",

        'SAT_total': {'$multiply': ["$SAT_qty","$SAT_unit_price"]},
        'SAT_currency' : "$SAT_currency",

        'SPY_total': {'$multiply': ["$SPY_qty","$SPY_unit_price"]},
        'SPY_currency' : "$SPY_currency",

        'TCH_total': {'$multiply': ["$TCH_qty","$TCH_unit_price"]},
        'TCH_currency' : "$TCH_currency",

        'TCOSTCO_total': {'$multiply': ["$TCOSTCO_qty","$TCOSTCO_unit_price"]},
        'TCOSTCO_currency' : "$TCOSTCO_currency",

        'STD_total': {'$multiply': ["$STD_qty","$STD_unit_price"]},
        'STD_currency' : "$STD_currency",

        'TNL_total': {'$multiply': ["$TNL_qty","$TNL_unit_price"]},
        'TNL_currency' : "$TNL_currency",

        'TERMO_total': {'$multiply': ["$TERMO_qty","$TERMO_unit_price"]},
        'TERMO_currency' : "$TERMO_currency",

        'SD_total': {'$multiply': ["$SD_qty","$SD_unit_price"]},
        'SD_currency' : "$SD_currency",

        'RM_total': {'$multiply': ["$RM_qty","$RM_unit_price"]},
        'RM_currency' : "$RM_currency",

        'PALLET_IN_total': {'$multiply': ["$PALLET_IN_qty","$PALLET_IN_unit_price"]},
        'PALLET_IN_currency' : "$PALLET_IN_currency",

        'PALLET_OUT_total': {'$multiply': ["$PALLET_OUT_qty","$PALLET_OUT_unit_price"]},
        'PALLET_OUT_currency' : "$PALLET_OUT_currency",

        'KIT_PLAYERAS_total': {'$multiply': ["$KIT_PLAYERAS_qty","$KIT_PLAYERAS_unit_price"]},
        'KIT_PLAYERAS_currency' : "$KIT_PLAYERAS_currency",

        'SERVICIO_REEMPACADO_total': {'$multiply': ["$SERVICIO_REEMPACADO_qty","$SERVICIO_REEMPACADO_unit_price"]},
        'SERVICIO_REEMPACADO_currency' : "$SERVICIO_REEMPACADO_currency",

        'SERVICIO_REETIQUETADO_total': {'$multiply': ["$SERVICIO_REETIQUETADO_qty","$SERVICIO_REETIQUETADO_unit_price"]},
        'SERVICIO_REETIQUETADO_currency' : "$SERVICIO_REETIQUETADO_currency",

        'SAEXH_total': {'$multiply': ["$SAEXH_qty","$SAEXH_unit_price"]},
        'SAEXH_currency' : "$SAEXH_currency",

        'MI_total': {'$multiply': ["$MI_qty","$MI_unit_price"]},
        'MI_currency' : "$MI_currency",

        'TARIMA_NEGRA_MILLER_total': {'$multiply': ["$TARIMA_NEGRA_MILLER_qty","$TARIMA_NEGRA_MILLER_unit_price"]},
        'TARIMA_NEGRA_MILLER_currency' : "$TARIMA_NEGRA_MILLER_currency",

        'MANO_OBRA_total': {'$multiply': ["$MANO_OBRA_qty","$MANO_OBRA_unit_price"]},
        'MANO_OBRA_currency' : "$MANO_OBRA_currency",

        'PICK_AND_PACK_total': {'$multiply': ["$PICK_AND_PACK_qty","$PICK_AND_PACK_unit_price"]},
        'PICK_AND_PACK_currency' : "$PICK_AND_PACK_currency",

        'ENTRADA_DETALLE_total': {'$multiply': ["$ENTRADA_DETALLE_qty","$ENTRADA_DETALLE_unit_price"]},
        'ENTRADA_DETALLE_currency' : "$ENTRADA_DETALLE_currency",

        'FLEJE_VENTA_total': {'$multiply': ["$FLEJE_VENTA_qty","$FLEJE_VENTA_unit_price"]},
        'FLEJE_VENTA_currency' : "$FLEJE_VENTA_currency",

        'PERSONAL_DEDICADO_PROYECTO_total': {'$multiply': ["$PERSONAL_DEDICADO_PROYECTO_qty","$PERSONAL_DEDICADO_PROYECTO_unit_price"]},
        'PERSONAL_DEDICADO_PROYECTO_currency' : "$PERSONAL_DEDICADO_PROYECTO_currency",

        'CROSS_DOCK_total': {'$multiply': ["$CROSS_DOCK_qty","$CROSS_DOCK_unit_price"]},
        'CROSS_DOCK_currency' : "$CROSS_DOCK_currency",

        'CROSS_DOCK_20_total': {'$multiply': ["$CROSS_DOCK_20_qty","$CROSS_DOCK_20_unit_price"]},
        'CROSS_DOCK_20_currency' : "$CROSS_DOCK_20_currency",

        'CROSS_DOCK_40_total': {'$multiply': ["$CROSS_DOCK_40_qty","$CROSS_DOCK_40_unit_price"]},
        'CROSS_DOCK_40_currency' : "$CROSS_DOCK_40_currency",

        'ALMACENAJE_TARIMA_total': {'$multiply': ["$ALMACENAJE_TARIMA_qty","$ALMACENAJE_TARIMA_unit_price"]},
        'ALMACENAJE_TARIMA_currency' : "$ALMACENAJE_TARIMA_currency",

        'TIEMPO_EXTRA_X_HORA_total': {'$multiply': ["$TIEMPO_EXTRA_X_HORA_qty","$TIEMPO_EXTRA_X_HORA_unit_price"]},
        'TIEMPO_EXTRA_X_HORA_currency' : "$TIEMPO_EXTRA_X_HORA_currency",

        'CROSS_DOCK_20_NOCTURNO_total': {'$multiply': ["$CROSS_DOCK_20_NOCTURNO_qty","$CROSS_DOCK_20_NOCTURNO_unit_price"]},
        'CROSS_DOCK_20_NOCTURNO_currency' : "$CROSS_DOCK_20_NOCTURNO_currency",

        'CROSS_DOCK_40_NOCTURNO_total': {'$multiply': ["$CROSS_DOCK_40_NOCTURNO_qty","$CROSS_DOCK_40_NOCTURNO_unit_price"]},
        'CROSS_DOCK_40_NOCTURNO_currency' : "$CROSS_DOCK_40_NOCTURNO_currency",

        'TIEMPO_EXTRA_X_HORA_NOCTURNO_total': {'$multiply': ["$TIEMPO_EXTRA_X_HORA_NOCTURNO_qty","$TIEMPO_EXTRA_X_HORA_NOCTURNO_unit_price"]},
        'TIEMPO_EXTRA_X_HORA_NOCTURNO_currency' : "$TIEMPO_EXTRA_X_HORA_NOCTURNO_currency",

        'CROSS_DOCK_40_2_total': {'$multiply': ["$CROSS_DOCK_40_2_qty","$CROSS_DOCK_40_2_unit_price"]},
        'CROSS_DOCK_40_2_currency' : "$CROSS_DOCK_40_2_currency",

        'SAP_MAS_15_total': {'$multiply': ["$SAP_MAS_15_qty","$SAP_MAS_15_unit_price"]},
        'SAP_MAS_15_currency' : "$SAP_MAS_15_currency",

        'SERVICIO_ARMADO_CARRETES_total': {'$multiply': ["$SERVICIO_ARMADO_CARRETES_qty","$SERVICIO_ARMADO_CARRETES_unit_price"]},
        'SERVICIO_ARMADO_CARRETES_currency' : "$SERVICIO_ARMADO_CARRETES_currency",

        'SERVICIO_ARMADO_CARRETES_URGENTES_total': {'$multiply': ["$SERVICIO_ARMADO_CARRETES_URGENTES_qty","$SERVICIO_ARMADO_CARRETES_URGENTES_unit_price"]},
        'SERVICIO_ARMADO_CARRETES_URGENTES_currency' : "$SERVICIO_ARMADO_CARRETES_URGENTES_currency",

        'UNIDAD_ESPACIO_TEMPORAL_total': {'$multiply': ["$UNIDAD_ESPACIO_TEMPORAL_qty","$UNIDAD_ESPACIO_TEMPORAL_unit_price"]},
        'UNIDAD_ESPACIO_TEMPORAL_currency' : "$UNIDAD_ESPACIO_TEMPORAL_currency",

        'COSTO_MENSUAL_UE_total': {'$multiply': ["$COSTO_MENSUAL_UE_qty","$COSTO_MENSUAL_UE_unit_price"]},
        'COSTO_MENSUAL_UE_currency' : "$COSTO_MENSUAL_UE_currency",

        'COSTO_MENSUAL_UE_EXTRA_total': {'$multiply': ["$COSTO_MENSUAL_UE_EXTRA_qty","$COSTO_MENSUAL_UE_EXTRA_unit_price"]},
        'COSTO_MENSUAL_UE_EXTRA_currency' : "$COSTO_MENSUAL_UE_EXTRA_currency",

        'PRECIO_TIEMPO_EXTRA_X_DIA_total': {'$multiply': ["$PRECIO_TIEMPO_EXTRA_X_DIA_qty","$PRECIO_TIEMPO_EXTRA_X_DIA_unit_price"]},
        'PRECIO_TIEMPO_EXTRA_X_DIA_currency' : "$PRECIO_TIEMPO_EXTRA_X_DIA_currency",

        'PRECIO_RENTA_FIJA_total': {'$multiply': ["$PRECIO_RENTA_FIJA_qty","$PRECIO_RENTA_FIJA_unit_price"]},
        'PRECIO_RENTA_FIJA_currency' : "$PRECIO_RENTA_FIJA_currency",

        'PRECIO_RENTA_OFICINA_total': {'$multiply': ["$PRECIO_RENTA_OFICINA_qty","$PRECIO_RENTA_OFICINA_unit_price"]},
        'PRECIO_RENTA_OFICINA_currency' : "$PRECIO_RENTA_OFICINA_currency",

        'METROS_ACORDADOS_total': {'$multiply': ["$METROS_ACORDADOS_qty","$METROS_ACORDADOS_unit_price"]},
        'METROS_ACORDADOS_currency' : "$METROS_ACORDADOS_currency",
    }}
    ]
    return query

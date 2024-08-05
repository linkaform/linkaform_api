# -*- coding: utf-8 -*-
#####
# Script para generar códigos QR
#####
import qrcode, os
from PIL import Image
from linkaform_api import settings, utils

class LKF_QR:
    def __init__(self, settings={}):
        self.settings = settings
        self.lkf_api = utils.Cache(settings)
    """
    Funciones para la creación del QR
    """
    def upload_qr(self, rutapdf, nombre_archivo, upload_data):
        #lkf_api = utils.Cache(settings)
        pdf_file = open(rutapdf,'rb')
        pdf_file_dir = {'File': pdf_file}
        #try:
        res = {}
        if True:
            upload_url = self.lkf_api.post_upload_file(data=upload_data, up_file=pdf_file_dir)
            pdf_file.close()
            if upload_url.get('status_code',0) == 200:
                res = upload_url.get('json', upload_url.get('data',{}))
                res.update({'file_url':res.get('file')})
        #except KeyError, e:
        #    print 'No pudo subir el archivo' , e
        return res

    def procesa_qr(self, url_for_qr, name_qr, form_id, img_field_id='604826d2a204b970e3d12e29'):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url_for_qr)
        qr.make(fit=True)
        # img = qr.make_image(fill_color="white", back_color="black").convert('RGB')
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        ruta_to_save = "/tmp/"
        name_to_save = "{}.png".format(name_qr)
        complete_path = ruta_to_save + name_to_save
        os.chdir(ruta_to_save)
        img.save( complete_path )
        upload_data = { 'form_id': form_id, 'field_id': img_field_id}
        respuesta_carga_qr = self.upload_qr(complete_path, name_to_save,  upload_data)
        return respuesta_carga_qr
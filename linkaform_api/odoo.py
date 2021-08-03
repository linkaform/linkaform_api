# -*- coding: utf-8 -*-
# Coded by:
# Jose Patricio Villareal - josepato@linkaform.com

import xmlrpc.client

class Odoo(object):

    def __init__(self):
        self.object = 'object'
        self.protocol = 'http'
        self.port=None
        self.host = ''
        self.user=''
        self.pwd=''
        self.dbname=''
        self.con =False
        self.uid = False


#         db='my-qorp'
#         username='linkaform-odoo@fixser.lat'
#         password = 'Fixser-2021$$'
#         db='my-qorp'
#
# common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# print(common.version())
# uid = common.authenticate(db, username, password, {})
# print('userid', uid)
# models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#
# res = models.execute_kw(db, uid, password,
#      'res.partner', 'search',
#      [[['is_company', '=', True]]])
# print('res',res)

    def getWSOdoo(self, host, object, user, pwd, dbname, port=None):
        print('getWSOdoo', self.host)
        if port:
            common = xmlrpc.client.ServerProxy('{}://{}:{}/xmlrpc/2/common'.format(self.protocol, self.host, self.port))
        else:
            common = xmlrpc.client.ServerProxy('{}://{}/xmlrpc/2/common'.format(self.protocol, self.host))
        self.uid = common.authenticate(self.dbname, self.user, self.pwd, {})
        if port:
            self.con = xmlrpc.client.ServerProxy('{}://{}:{}/xmlrpc/2/object'.format(self.protocol, self.host,  self.port, self.object),
            allow_none=True)
        else:
            self.con = xmlrpc.client.ServerProxy('{}://{}/xmlrpc/2/object'.format(self.protocol, self.host, self.object),allow_none=True)
        return  dbname, pwd

    def getMethod(self, model='res.partner', metodo='search', port=None, args=[], args2=[],
                  args3=[], args4=[]):
        if not port:
            port = self.port
        self.getWSOdoo(self.host, self.object, self.uid, self.pwd, self.dbname, port)
        # try:
        if True:
            if args4:
                res = self.con.execute_kw(self.dbname, self.uid, self.pwd, model, metodo, args, args2,
                                  args3, args4)
            elif args3:
                res = self.con.execute_kw(self.dbname, self.uid, self.pwd, model, metodo, args, args2,
                                  args3)
            elif args2:
                res = self.con.execute_kw(self.dbname, self.uid, self.pwd, model, metodo, args, args2)
            else:
                res = self.con.execute_kw(self.dbname, self.uid, self.pwd, model, metodo, args)
            return res
        # except Exception as e:
        #     if e.faultCode:
        #         return e.faultCode
        #     return None

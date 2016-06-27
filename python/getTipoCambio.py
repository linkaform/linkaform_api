#! /usr/bin/python

import urllib2, HTMLParser, time
import xmlrpclib

def getHTML(url, agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080404 Iceweasel/2.0.0.14 (Debian-2.0.0.14-0etch1)", referer=""):
    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", agent), ("referer", referer)]
    fid = opener.open(url)
    data = fid.read()
    fid.close()
    return data


def getTipoCambio(dia, mes, agnio):
    try:
        url = "http://dof.gob.mx/indicadores_detalle.php?cod_tipo_indicador=158&dfecha=%02i%%2F%02i%%2F%i&hfecha=%02i%%2F%02i%%2F%i" %(dia, mes, agnio, dia, mes, agnio)
        htmldata = getHTML(url).split("\n")
        for linenum in range(len(htmldata)):
            line = htmldata[linenum]
            if line.find("Celda") >= 0:
                break
        if linenum >= (len(htmldata) - 3):
            return None
        datestr = "%02i-%02i-%i" %(dia, mes, agnio)
        linenum += 1
        fechaline = htmldata[linenum]
        if fechaline.find(datestr) < 0:
            return None
        linenum += 1
        dataline = htmldata[linenum]
        startpos = dataline.find(">")
        endpos = dataline.find("</td")
        if (startpos < 0) or (endpos < 0):
            return None
        return float(dataline[startpos+1:endpos])
    except:
        return None


def getUltimoTipoCambio(dia=0, mes=0, agnio=0):
    if (not dia) and (not mes) and (not agnio):
        tt = time.time()
        (agnio, mes, dia, x1, x2, x3, x4, x5, x5) = time.localtime(tt)
    else:
        tt = time.mktime((agnio, mes, dia, 12, 0, 0, 0, 0, 0))
    count = 0
    valor = getTipoCambio(dia, mes, agnio) 
    while (valor == None) and (count < 10):
        tt -= 24 * 3600
        (agnio, mes, dia, x1, x2, x3, x4, x5, x5) = time.localtime(tt)
        valor = getTipoCambio(dia, mes, agnio)
        count += 1
    return valor



def getWSTiny(host='localhost',object='object',user='duglas',pwd='duglas.admon',dbname='Minerales'):
    con= xmlrpclib.ServerProxy('http://%s:8069/xmlrpc/common'%(host))
    uid=con.login(dbname,user,pwd)
    con=xmlrpclib.ServerProxy('http://%s:8069/xmlrpc/%s'%(host,object))
    return con, uid, dbname, pwd

def getMethod(model='res.partner', metodo='search', args=[],args2=[]):
    con,uid,dbname,pwd=getWSTiny()
    res=con.execute(dbname, uid, pwd, model, metodo, args,args2)
    return res


def getCuerrencyId(currency_name=''):
    currency_id = getMethod('res.currency','search',[('code','=',currency_name)])
    return currency_id

def writeTipoDeCambio(rate, currency_name, date):
    currency_id = getCuerrencyId(currency_name)[0]
    rate_id = getMethod('res.currency.rate','create',{'currency_id':currency_id, 'rate':1/rate, 'name':date, 'rate_inv':rate})
    return True



(agnio, mes, dia, x1, x2, x3, x4, x5, x5) = time.localtime()


currency_name = 'USD'
rate = getTipoCambio(dia, mes, agnio)



if rate != None:
    writeTipoDeCambio(rate, currency_name, '%d-%02d-%02d'%(agnio, mes, dia))

import cx_Oracle
import requests
import xmltodict
import untangle
import string
import random
import datetime
from datetime import date, timedelta
import re

cx_Oracle.init_oracle_client(
        lib_dir=r"C:\tue\instantclient-basic-windows.x64-19.10.0.0.0dbru\instantclient_19_10")
def connectdb():   
    con = cx_Oracle.connect('PA', 'password', '10.1.6.25/STR')
    cur = con.cursor()
    return cur


def getmaxsequenpnr(pnr,cur):
    sqlcommand = "select Max(sequencenmbr) from itdev.pa_booking  where recordlocator ="+"'"+pnr+"'"
    cur.execute(sqlcommand)
    res = cur.fetchall()
    return res[0][0]

def getpnrsdatastream(flightno, date,cur):
    dep = datetime.datetime.strptime(date, '%d-%b-%Y')
    depadd1 = dep + datetime.timedelta(days=1)
    stringdep = dep.strftime('%d-%b-%Y')
    stringdepadd1 = depadd1.strftime('%d-%b-%Y')
    sqlcommand = ""
    sqlcommand += "select recordlocator, MAX(sequencenmbr)"
    sqlcommand += "from itdev.pa_booking_seg "
    sqlcommand += "where operfltnumair ="+"'"+flightno+"'" + "and departdatetime >=" + \
        "'"+stringdep+"'" + "and departdatetime <"+"'"+stringdepadd1+"'"
    sqlcommand += "group by recordlocator"
    #print(sqlcommand)
    cur.execute(sqlcommand)
    res = cur.fetchall()
    pnrs = []
    for row in res:
        if row[1] == getmaxsequenpnr(row[0],cur):
            pnrs.append(row[0])
    return pnrs
def getpaxcontactandticket(pnr,cur):
    sqlcommand = ""
    sqlcommand += "Select distinct b.recordlocator, bp.withinfant, bp.lastname, bp.firstname, bp.emailaddress, bp.gender,bph.*,bt.* "
    sqlcommand += "From itdev.pa_booking b "
    sqlcommand += "INNER JOIN itdev.pa_booking_pax bp "
    sqlcommand += "ON b.bk_pk = bp.bk_pk "
    sqlcommand += "AND b.sequencenmbr =(select Max(sequencenmbr) from itdev.pa_booking  where recordlocator ='"+pnr+"' ) and b.bk_pk = (select Max(bk_pk) from itdev.pa_booking  where recordlocator ='"+pnr+"' ) "
    sqlcommand += '''INNER JOIN (SELECT bk_pk, agencylocation, LISTAGG(ticketnumber, ', ') WITHIN GROUP (ORDER BY ticketnumber) "ticketnumber" FROM itdev.pa_booking_ticket group by bk_pk,agencylocation) bt '''
    sqlcommand += "ON b.bk_pk = bt.bk_pk "
    sqlcommand += '''LEFT JOIN (SELECT bk_pk, LISTAGG(number1, ', ') WITHIN GROUP (ORDER BY number1) "phone" FROM itdev.pa_booking_phone group by bk_pk) bph '''
    sqlcommand += "ON b.bk_pk = bph.bk_pk "
    #print(sqlcommand)
    cur.execute(sqlcommand)
    res = cur.fetchall()
    return res


if __name__ == "__main__":
    cur = connectdb()
    pnrsfromdatastream = getpnrsdatastream('6442', '03-mar-2021',cur)
    for pnr in pnrsfromdatastream:
        paxphones = getpaxcontact(pnr,cur)
        for paxphone in paxphones:
            print(paxphone)
            
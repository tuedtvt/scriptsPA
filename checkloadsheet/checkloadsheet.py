import requests
import xmltodict
import untangle
from Flightmodel import Flight
import connectsqlserver
from datetime import date
from datetime import timedelta  
import json
import automated_email
import time

def checkloadsheet(flightno,flightdate):
    #fields = "field1, field2, field3, field4"
    table = "Loadsheets"
    conditions = "Flightno='"+flightno + "'AND Flightdate='"+flightdate+"'"
    
    sql = (f"SELECT * "
           f"FROM {table} "
           f"WHERE {conditions};")
    cursor = connectsqlserver.query(sql)
    #print(len(cursor.fetchall()))
    #for row in cursor.fetchall():
        #print (row[1])
    #print(cursor)
    return cursor.fetchall() 

def getflightschedule(flightdate):
    url = "http://crew.jetstarpacificair.com:8383/aslwebservice/"    
   
    querystring = {"plandate":flightdate,"dataname":"FlightPlan"}
    headers = {
        'authorization': "Basic amV0c3Rhcjp3Mzg1M1J2MUMzLiM=",
        'cache-control': "no-cache",
        }    
    response = requests.request("POST", url, headers=headers, params=querystring)
    doc = untangle.parse(response.text)    
    return doc 
def checkloadsheetforaday():
    todaytime = date.today()#+timedelta(days=-1)  
    today = todaytime.strftime("%d-%b-%y")
    doc = getflightschedule(today)    
    bodymail=""
    for flight in doc.asl.flight:
        #check gio bay
        deph = flight.etd_eta.cdata[0:2]
        depmin =flight.etd_eta.cdata[2:4]
        fulldeptimestring = str(today + " " + deph+":"+depmin)
        deptime = datetime.strptime(fulldeptimestring, '%d-%b-%y %H:%M')
        curenttime = datetime.now()
        subject = "check loadsheet!!!" + str(today)
        if (deptime<curenttime):
            if (flight.flight_no.cdata !="DUMMY"): #khac chuyen test va da bay roi            
                listchuyenbaytrave = checkloadsheet(flight.flight_no.cdata,today)
                if len(listchuyenbaytrave) ==0:      
                    print(flight.flight_no.cdata + " date: " + str(today))
                    bodymail +=flight.flight_no.cdata + " date: " + str(today)+'\n'
    #print(bodymail)
    if (bodymail==""):
        bodymail= str(curenttime.hour)+":" +str(curenttime.minute) + ": cac chuyen bay da bay roi deu co loadsheet"
    automated_email.sendmail(['tue.it@pacificairlines.com.vn','tung.truongthanh@pacificairlines.com.vn','hieu.tranminh@pacificairlines.com.vn','cuong.vutuan@pacificairlines.com.vn','dong.tran@pacificairlines.com.vn'],bodymail,subject)

from datetime import datetime, timedelta
from threading import Timer

while True:
    # chay theo gio dinh san
    '''
    x=datetime.today()
    #9h
    y9h = x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0) #+ timedelta(days=1)
    delta_t9h=y9h-x
    secs9h=delta_t9h.total_seconds()
    t9h = Timer(secs9h, checkloadsheetforaday)
    #3hchieu
    
    y15h = x.replace(day=x.day, hour=15, minute=0, second=0, microsecond=0) #+ timedelta(days=1)
    delta_t15h=y15h-x
    secs15h=delta_t15h.total_seconds()
    t15h = Timer(secs15h, checkloadsheetforaday)
    #23h toi
    
    y23h = x.replace(day=x.day, hour=23, minute=0, second=0, microsecond=0) #+ timedelta(days=1)
    delta_t23h=y23h-x
    secs23h=delta_t23h.total_seconds()
    t23h = Timer(secs23h, checkloadsheetforaday)
    
    ts =[t9h,t15h,t23h]
    for t in ts:
        t.start()
    '''
    checkloadsheetforaday()
    time.sleep(10800)
#This will execute a function (eg. hello_world) in the next day at 1a.m.




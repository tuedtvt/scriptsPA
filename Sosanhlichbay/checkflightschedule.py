import requests
import xmltodict
import untangle
import string
import random
import datetime
from dateutil.parser import parse
from datetime import  timedelta
import re
from threading import Timer
import automated_email
import time
def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

ConversationId = id_generator()
MessageId = "mid:20001209-133003-2333@clientofsabre.com";
TimeStamp =str(datetime.datetime.now() )
Domain = 'VN'
sDomain='VN'
sPseudo_City_Code=''
Token_Key = ""
if (sPseudo_City_Code==''):    
    Pseudo_City_Code = sDomain          
else:
    Pseudo_City_Code = sPseudo_City_Code

def gettoken(): 
    User_Name = '600666'
    Password = ''
    Organization = 'VN'
    url = "https://webservices.havail.sabre.com"
    xml = "";
    xml += "<soap-env:Envelope xmlns:soap-env=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:eb=\"http://www.ebxml.org/namespaces/messageHeader\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:xsd=\"http://www.w3.org/1999/XMLSchema\">";
    xml += "   <soap-env:Header>";
    xml += "      <eb:MessageHeader soap-env:mustUnderstand=\"1\" eb:version=\"1.0\">";
    xml += "         <eb:From>";
    xml += "            <eb:PartyId/>";
    xml += "         </eb:From>";
    xml += "         <eb:To>";
    xml += "            <eb:PartyId/>";
    xml += "         </eb:To>";
    xml += "         <eb:CPAId>VN</eb:CPAId>";
    xml += "         <eb:ConversationId>" + ConversationId + "</eb:ConversationId>";
    xml += "         <eb:Service>SessionCreateRQ</eb:Service>";
    xml += "         <eb:Action>SessionCreateRQ</eb:Action>";
    xml += "         <eb:MessageData>";
    xml += "            <eb:MessageId>" + MessageId + "</eb:MessageId>";
    xml += "            <eb:Timestamp>" + TimeStamp + "</eb:Timestamp>";
    xml += "         </eb:MessageData>";
    xml += "      </eb:MessageHeader>";
    xml += "      <wsse:Security xmlns:wsse=\"http://schemas.xmlsoap.org/ws/2002/12/secext\" xmlns:wsu=\"http://schemas.xmlsoap.org/ws/2002/12/utility\">";
    xml += "         <wsse:UsernameToken>";
    xml += "             <wsse:Username>" + User_Name + "</wsse:Username>";
    xml += "            <wsse:Password>" + Password + "</wsse:Password>";
    xml += "            <Organization>" + Organization + "</Organization>";
    xml += "            <Domain>" + Domain + "</Domain>";
    xml += "         </wsse:UsernameToken>";
    xml += "      </wsse:Security>";
    xml += "   </soap-env:Header>";
    xml += "   <soap-env:Body>";
    xml += "      <eb:Manifest soap-env:mustUnderstand=\"1\" eb:version=\"1.0\">";
    xml += "         <eb:Reference xlink:href=\"cid:rootelement\" xlink:type=\"simple\"/>";
    xml += "      </eb:Manifest>";
    xml += "      <SessionCreateRQ>";
    xml += "         <POS>";
    xml += "            <Source PseudoCityCode=\"" + Pseudo_City_Code + "\"/>";
    xml += "         </POS>";
    xml += "      </SessionCreateRQ>";
    xml += "      <ns:SessionCreateRQ xmlns:ns=\"http://www.opentravel.org/OTA/2002/11\"/>";
    xml += "   </soap-env:Body>";
    xml += "</soap-env:Envelope>";
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache"
        }    
    response = requests.request("POST", url, data=xml, headers=headers)
    doc = untangle.parse(response.text)    
    return (doc.soap_env_Envelope.soap_env_Header.wsse_Security.wsse_BinarySecurityToken.cdata)

def getflightschedule(date):    
    aCommand = "VDS/"+date
    global Token_Key
    if Token_Key=="":        
        Token_Key=gettoken()
    url = "https://webservices.havail.sabre.com"
    xml = "";
    xml += "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:sec=\"http://schemas.xmlsoap.org/ws/2002/12/secext\" xmlns:mes=\"http://www.ebxml.org/namespaces/messageHeader\" xmlns:ns=\"http://webservices.sabre.com/sabreXML/2003/07\">";
    xml += "    <soapenv:Header>";
    xml += "        <sec:Security>";
    xml += "            <sec:BinarySecurityToken>" + Token_Key + "</sec:BinarySecurityToken>";
    xml += "        </sec:Security>";
    xml += "        <mes:MessageHeader mes:id=\"?\" mes:version=\"?\">";
    xml += "            <mes:From>";
    xml += "            <!--1 or more repetitions:-->";
    xml += "                <mes:PartyId>WebServiceClient</mes:PartyId>";
    xml += "            </mes:From>";
    xml += "            <mes:To>";
    xml += "            <!--1 or more repetitions:-->";
    xml += "                <mes:PartyId >WebServiceSupplier</mes:PartyId>";
    xml += "            </mes:To>";
    xml += "            <mes:CPAId>VN</mes:CPAId>";
    xml += "            <mes:ConversationId>" + ConversationId + "</mes:ConversationId>";
    xml += "            <mes:Service>Session</mes:Service>";
    xml += "            <mes:Action>SabreCommandLLSRQ</mes:Action>";
    xml += "            <mes:MessageData>";
    xml += "                <mes:MessageId>" + MessageId + "</mes:MessageId>";
    xml += "                <mes:Timestamp>" + TimeStamp + "</mes:Timestamp>";
    xml += "            </mes:MessageData>";
    xml += "        </mes:MessageHeader>";
    xml += "    </soapenv:Header>";
    xml += "    <soapenv:Body>";
    xml += "        <ns:SabreCommandLLSRQ xmlns=\"http://webservices.sabre.com/sabreXML/2003/07\" xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" TimeStamp=\"2011-03-09T15:00:47-06:00\" Version=\"1.6.1\">";
    xml += "            <ns:Request Output=\"SCREEN\" CDATA=\"true\">";
    xml += "                <ns:HostCommand>" + aCommand.upper() + "</ns:HostCommand>";
    xml += "            </ns:Request>";
    xml += "        </ns:SabreCommandLLSRQ>";
    xml += "    </soapenv:Body>";
    xml += "</soapenv:Envelope>";
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache"
        }    
    response = requests.request("POST", url, data=xml, headers=headers)
    doc = untangle.parse(response.text)   
    #print(doc.soap_env_Envelope.soap_env_Body.SabreCommandLLSRS.Response.cdata) 
    allflight = doc.soap_env_Envelope.soap_env_Body.SabreCommandLLSRS.Response.cdata    
    regexchuyenbaydau6 = r"6\d{3}\s{2}\w{3}/\w{3}\s{4}\d{4}/\d{4}"
    chuyenbaydau6= re.findall(regexchuyenbaydau6,allflight)              
    return chuyenbaydau6

def getflightscheduleny (date):
    
    url = "http://crew.jetstarpacificair.com:8383/aslwebservice/"

    querystring = {"plandate":date,"dataname":"FlightPlan"}
    
    headers = {
        'authorization': "Basic amV0c3RhcmludGVybmFsOnczODUzUnYxQzMuIw==",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "c25e9dcb-36f1-c767-7400-e9db83f58f17"
        }
    
    response = requests.request("POST", url, headers=headers, params=querystring)    
    doc = untangle.parse(response.text)
    return (doc.asl.children)

def getflightdetailny(date,flightno):

    url = "http://crew.jetstarpacificair.com:8383/aslwebservice/"
    
    querystring = {"plandate":date,"dataname":"SectorDetail","flightno":flightno}
    
    headers = {
        'authorization': "Basic amV0c3RhcmludGVybmFsOnczODUzUnYxQzMuIw==",
        'cache-control': "no-cache",
        'postman-token': "60ed865c-59cb-7b14-0a49-47c5836da13c"
        }
    
    response = requests.request("POST", url, headers=headers, params=querystring)
    doc = untangle.parse(response.text)
    
    return (doc.asl.detail)


def doichieuthieusotlichbaytrensabre(listlichbaysabre,datecheckny):
    stringdoichieu=''
    listlichbayny = getflightscheduleny(datecheckny)       
    for chuyenbayny in listlichbayny:
        if (chuyenbayny.ac_reg.cdata !='DUMMY'):
            sohieuchuyenbayny =(chuyenbayny.flight_no.cdata.replace('BL',''))      
            if not any(sohieuchuyenbayny in thongtinchuyenbaysabre for  thongtinchuyenbaysabre in listlichbaysabre):
                stringdoichieu+= 'Ngay: '+datecheckny+ 'thieu chuyen bay '+ sohieuchuyenbayny +'tren sabre' + '\r\n'
    
    return stringdoichieu

def checklichbay():
    bodymail="\r\n"
    today = datetime.datetime.today()
    subject="So sanh lich bay tu ngay "+today.strftime('%d-%b-%y')
    for i in range (0,7):
        datecheck = today +  timedelta(days=i)      
        datecheckny = datecheck.strftime('%d-%b-%y')
        datechecksabre = datecheckny.split('-')[0]+datecheckny.split('-')[1]           
        listflightsabre = getflightschedule(datechecksabre)
        for flightsabre in listflightsabre:
            regexlightno = r"6\d{3}"
            flightnumber =re.search(regexlightno,flightsabre).group(0)                 
            regexroute = r"[A-Z]{3}/[A-Z]{3}"
            route =re.search(regexroute,flightsabre).group(0)            
            regextime = r"\d{4}/\d{4}"
            time =re.search(regextime,flightsabre).group(0)   
             #newyork           
            try:
                flightdetailny = getflightdetailny(datecheckny,'BL'+flightnumber)   
            
                routeny = flightdetailny.estdep.cdata +'/'+flightdetailny.estarr.cdata
            
                datetimeetdny = datetime.datetime.strptime(flightdetailny.etd.cdata, '%H%M')+ timedelta(hours=7)
                datetimeetany = datetime.datetime.strptime(flightdetailny.eta.cdata, '%H%M')+ timedelta(hours=7)
                
                stringetdny = datetimeetdny.strftime('%H%M')
                stringetany = datetimeetany.strftime('%H%M')
                
                timenewyorklocal = stringetdny +'/'+stringetany
                  
                if (route!=routeny) or (time!=timenewyorklocal):
                    bodymail +=datecheckny+' : '+flightnumber+' gio newyork: '+timenewyorklocal+ ' gio sabre: '+time+'\r\n'
                    #print(datecheckny,':',flightnumber,' gio newyork:',timenewyorklocal, 'gio sabre: ',time)
                    print('...')
            except  AttributeError:
                bodymail = bodymail+' Ngay '+datecheckny+' khong ton tai chuyen '+flightnumber+' tren newyork ' +'\r\n'
            
        try:
            bodymail+=doichieuthieusotlichbaytrensabre(listflightsabre,datecheckny)
        except:
            print('cant doi chieu lich bay')
            bodymail+=doichieuthieusotlichbaytrensabre(listflightsabre,datecheckny)
                #print('Ngay ',datecheckny,' khong ton tai chuyen ',flightnumber,' tren newyork')    
    automated_email.sendmail(['tue.it@pacificairlines.com.vn','support@pacificairlines.com.vn'],bodymail,subject)            
    print(bodymail)


def signoutsabre(Token_Key):

    url = "https://webservices.havail.sabre.com"
    xml = "";
    xml += "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:sec=\"http://schemas.xmlsoap.org/ws/2002/12/secext\" xmlns:eb=\"http://www.ebxml.org/namespaces/messageHeader\" xmlns:ns=\"http://webservices.sabre.com/sabreXML/2003/07\">";
    xml += "   <soapenv:Header>";
    xml += "      <eb:MessageHeader soapenv:mustUnderstand=\"1\" eb:version=\"1.0\">";
    xml += "         <eb:ConversationId>" + ConversationId + "</eb:ConversationId>";
    xml += "         <eb:From>";
    xml += "            <eb:PartyId type=\"urn:x12.org:IO5:01\">99999</eb:PartyId>";
    xml += "         </eb:From>";
    xml += "         <eb:To>";
    xml += "            <eb:PartyId type=\"urn:x12.org:IO5:01\">123123</eb:PartyId>";
    xml += "         </eb:To>";
    xml += "         <eb:CPAId>IPCC</eb:CPAId>";
              
    xml += "         <eb:Service eb:type=\"OTA\">SessionCloseRQ</eb:Service>";
    xml += "         <eb:Action>SessionCloseRQ</eb:Action>";
    xml += "         <eb:MessageData>";
    xml += "            <eb:MessageId>" + MessageId + "</eb:MessageId>";
    xml += "            <eb:Timestamp>" + TimeStamp + "</eb:Timestamp>";
    xml += "            <eb:TimeToLive>" + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") +"</eb:TimeToLive>";
    xml += "         </eb:MessageData>";
    xml += "      </eb:MessageHeader>";
    xml += "    <sec:Security>";
    xml += "        <sec:BinarySecurityToken>" + Token_Key + "</sec:BinarySecurityToken>";
    xml += "    </sec:Security>";
    xml += "   </soapenv:Header>";
    xml += "   <soapenv:Body>";
    xml += "<SessionCloseRQ>";
    xml += "    <POS>";
    xml += "        <Source PseudoCityCode=\"" + Pseudo_City_Code + "\"/>";
    xml += "    </POS>";
    xml += "</SessionCloseRQ>";
    xml += "<ns1:SessionCloseRQ xmlns:ns1=\"http://www.opentravel.org/OTA/2002/11\"><ns1:POS/></ns1:SessionCloseRQ></soapenv:Body>";
    xml += "</soapenv:Envelope>";
    headers = {
        'content-type': "text/xml",
        'cache-control': "no-cache"
        }    
    response = requests.request("POST", url, data=xml, headers=headers)
    print(response.text)

if __name__ == "__main__":

    while True:
        try:   
            checklichbay()
            print(Token_Key)
            signoutsabre(Token_Key)   
            Token_Key = ""       
        except:
            print('Something when wrong, reruning')    
            checklichbay()
            print(Token_Key)
            signoutsabre(Token_Key)   
            Token_Key = ""
        print('sleeping and waiting for next running')
        time.sleep(24*60*60-300)

    


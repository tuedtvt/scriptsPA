from smtplib import SMTP as smtp
import json
import configparser
import os   
from datetime import date
from datetime import timedelta,datetime

today = date.today()#+timedelta(days=-1)  
today = today.strftime("%d-%b-%y")

emailaddress = 'ops_noreply@pacificairlines.com.vn'
emailpassword = 'jetstarpacific'

def sendmail(reciever_add, text,subject):
    #text = text.encode('utf-8').strip()
    curenttime = datetime.now()
    SUBJECT = subject
    #SUBJECT = "Flights have not received the loadsheet!!! - "+str(today)
    message = 'Subject: {}\n\n{}'.format(SUBJECT, text) #.encode('utf-8')
    server = smtp('smtp.gmail.com:587')
    server.starttls()
    server.login(emailaddress, emailpassword)
    server.sendmail(emailaddress, reciever_add, message)
    print(str(today)+" "+str(curenttime.hour)+":" +str(curenttime.minute)+": Mail sent succesfully....!")

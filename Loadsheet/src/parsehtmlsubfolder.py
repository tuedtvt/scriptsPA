from bs4 import BeautifulSoup
import glob, os
import time
import stat

# Fetch the html file
path="D:\\eclipse-workspace\\anhDong\\src\\messages"
list_ngay = [f.path for f in os.scandir(path) if f.is_dir()]
from pathlib import Path

for ngay in list_ngay:
    list_chuyenbay = [f.path for f in os.scandir(ngay) if f.is_dir()]
    for chuyenbay in list_chuyenbay:
        pathchuyenbay =Path(chuyenbay+r"\\")           
        os.chdir(pathchuyenbay)
        htmlflies = glob.glob("*.html")
        for htmlfile in htmlflies:
            modTimesinceEpoc = os.path.getmtime(htmlfile)
# Convert seconds since epoch to readable timestamp
            modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
            print(htmlfile," : ",modificationTime)
        if len(htmlflies)>0:
            
            if len(htmlflies)>1:           
                latest_file = max(htmlflies, key=os.path.getctime)
            elif len(htmlflies)==1:
                latest_file=htmlflies[0]
                #for htmlfile in htmlflies:         
            with open(latest_file, 'r') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                data = []              
                tables = soup.find_all('table')
                    #tablechuathong tin chuyen bay
                         #table_body = tables[1].find('tbody')  
                ''' 
                rowstable1 = tables[0].find_all('tr')
                for row in rowstable1:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele]) # Get rid of empty values
                '''
                    
                rowstable2 = tables[1].find_all('tr')
                for row in rowstable2:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele]) # Get rid of empty values
                        #tablechuathong tin khach
                rowstable3 = tables[2].find_all('tr')
                for row in rowstable3:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele]) # Get rid of empty values
  
            #print(data2loadsheet)   
        #data[3][1],data[3][4]
        #print(data[4])         
        #print(data[1][1]," ",data[1][4]," ",data[5][2])

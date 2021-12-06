from bs4 import BeautifulSoup
import glob, os
from datetime import datetime
import time
import shutil
import os
# Fetch the html file
import connectsqlserver
def coppyfilefromloadsheetfolder(src_dir,dest_dir,move_dir):   
    # path to source directory
    #src_dir = '/Volumes/MacintoshHD/foldertest1/'   
    # path to destination directory
    #dest_dir = '/Volumes/MacintoshHD/foldertest2/'
    #move_dir = '/Volumes/MacintoshHD/foldertest3/'
    
    # getting all the files in the source directory
    files = os.listdir(src_dir)
    for fname in files:
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src_dir,fname), dest_dir)
        shutil.move(os.path.join(src_dir,fname), move_dir)


def insertflight(flightno,flightdate,totalpax,version,timereceive): 
    sql = "INSERT INTO Loadsheets (Flightno,Flightdate,totalpax,version,timereceive) VALUES (?,?,?,?,?)"
    val = (flightno,flightdate,totalpax,version,timereceive)   
    connectsqlserver.insert(sql,val)
def readandimporttodb():
    path=r'D:\\eclipse-workspace\\anhDong\\src\\messages\\31082020\\BL 320\\'
    pathtomove=r'D:\\testls\\'
    os.chdir(path)
    htmlflies = glob.glob("*.html")        
    if len(htmlflies)>0:                
        for htmlfile in htmlflies:  
            modTimesinceEpoc = os.path.getmtime(htmlfile)
            modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
            data = []                    
            with open(htmlfile, 'rb') as f:
                contents = f.read().decode('utf-8', 'ignore')
                soup = BeautifulSoup(contents, 'lxml')                              
                tables = soup.find_all('table')
                        #tablechuathong tin version
                rowstable1 = tables[0].find_all('tr')
                for row in rowstable1:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele]) # Get rid of empty values
                        #tablechuathong tin chuyen bay                                        
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
            #         %d%b%y
            flightdate = datetime.strptime(data[3][4], '%d%b%y')  
            print((data[7]))
            if (len(data[1])>2):            
                insertflight(data[3][1],flightdate,data[7][2],data[1][3],modificationTime) 
                print(data[3][1]," ",flightdate," ",data[7][2],data[1][3],modificationTime)
            elif (len(data[1])==2):
                insertflight(data[3][1],flightdate,data[7][2],data[1][1],modificationTime)
                print(data[3][1]," ",flightdate," ",data[7][2],data[1][1],modificationTime)       
            currentpath = path + htmlfile
            newpath = pathtomove + htmlfile 
            os.replace(currentpath, newpath)   
while True:
    readandimporttodb()
    #coppyfilefromloadsheetfolder()
    time.sleep(600)

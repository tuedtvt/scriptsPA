def connectsql():
    import pyodbc 
    import configparser
    import os   
    config = configparser.ConfigParser()
    config.read([os.path.abspath('D:\\eclipse-workspace\\anhDong\\src\\setting.ini')])
    hostname = config.get('server', 'hostname')
    username = config.get('account', 'username')
    password = config.get('account', 'password')
    dbname   = config.get('server','dbname')
    
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server='+hostname+';'
                          'Database='+dbname+';'
                          'uid='+username+';'
                          'pwd='+password+';'
                          'Trusted_Connection=no;')
    
    #cursor = conn.cursor()
    #cursor.execute('SELECT * FROM testtable')
    
    #for row in cursor:
        #print(row)    
    return conn
def excecute(command):    
    conn = connectsql()
    cursor= conn.cursor()
    cursor.execute(command)
    conn.commit()
def query(commandquery):
    conn = connectsql()
    cursor= conn.cursor()
    cursor.execute(commandquery)
    '''
    for row in cursor:
        print(row)  
        '''
    return cursor
        
def insert(sql,value):    
    conn = connectsql()
    cursor= conn.cursor()
    cursor.execute(sql,value)
    conn.commit()   
    

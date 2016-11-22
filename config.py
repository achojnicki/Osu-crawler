class log:
    logging=True
    logToFile=False
    logFile="log.log"
    terminal=False
    
    screenMessageLevel=0
    fileMessageLevel=0
class database:
    backend='mysql'
    
    #only sqlite
    file="baza.db"
    
    #only mysql
    host='localhost'
    user='user'
    password='password'
    database='database'
    
class osuapi:
    key="osu api key"
class beatmaps:
    since="2016-10-05"
import time
import log
import sys

import config
import parser
import fetcher
import process
import db

class main:
    def __init__(self):
        self.working=True
        self.threads=[]
        
        self.log=log.Log(self)

        self.fetcher=fetcher.Fetcher(self)
        self.process=process.Process(self)
        self.db=db.Db(self)
        
        self.fetcher.start()
        self.process.start()
        self.db.start()
        
    def exit(self,l=0):
        self.working=False
        sys.exit(l)
    def start(self):
        while 1:
            time.sleep(1)
if __name__=="__main__":
    a=main()
    a.start()
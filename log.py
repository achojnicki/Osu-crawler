#!/usr/bin/Python
import config
import time, codecs, traceback, sys
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Log:
    def __init__(self,main):
        self.main=main
        self.busy=False
        self.screenmessagelevel=config.log.screenMessageLevel
        self.filemessagelevel=config.log.fileMessageLevel
        
        self.colours=config.log.terminal
        self.log=config.log.logging
        self.saveToFile=config.log.logToFile
        self.file=config.log.logFile
        
        if self.saveToFile:
            try:
                self.plik=open(self.file,'a')
            except:
                self.plik=open(self.file,'w')
            self.plik.write(u'-----------------------------------------------------------\n')
            self.plik.close()
    def msg(self,level,msg, code='',):
        while self.busy==True:
            time.sleep(0.1)
        self.busy=True
        if level>=self.screenmessagelevel and self.log:
            x=''
            if level>=10 and level <50:
                if level %2==0:
                    x=bcolors.OKBLUE
                else:
                    x=bcolors.WARNING
            elif level>=50:
                x=bcolors.FAIL
            if self.colours:
                print x+time.strftime(u"%d/%m/%Y %H:%M:%S")+u' '+unicode(level)+u' '+unicode(msg)+u' '+code+bcolors.ENDC
            else:
                print time.strftime(u"%d/%m/%Y %H:%M:%S")+u' '+unicode(level)+u' '+unicode(msg)+u' '+code
        if level>=self.filemessagelevel and self.saveToFile:
            self.plik=codecs.open(self.file,'a','utf-8')
            self.plik.write(time.strftime(u"%d/%m/%Y %H:%M:%S")+u' {0} {1} {2}\n'.format(level,msg,code))
            self.plik.close()
        self.busy=False
    def excep(self):
        w=traceback.format_exception(sys.exc_info()[0],  sys.exc_info()[1],  sys.exc_info()[2])
        w=w[0]+w[1]+w[2]
        self.msg(100,w+u"""\nGlobals: {0}\nLocals: {1}\nDir: {2}""".format(globals(), locals(), dir()))
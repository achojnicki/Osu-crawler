import re
import Queue
import threading
import config

class Process:
    def __init__(self,main):
        self.main=main
        self.dbQueue=Queue.Queue()

    def worker(self):
        self.main.log.msg('0','Process: Thread started.')
        while self.main.working:
            
            maxscore=0
            minscore=100000000000000000000
            avgscore=0
            amplscore=0
            
            maxCombo=0
            minCombo=1000000000000000000000
            avgCombo=0.0
            amplCombo=0.0
            
            
            
            avgPerfect=0.0
            
            a=self.main.fetcher.processQueue.get()
            details=a[0]
            plays=a[1]
            
            for a in plays:
                score=int(a[0])
                if score>maxscore:
                    maxscore=score
                if score<minscore:
                    minscore=score
                    
                combo=int(a[6])
                if combo>maxCombo:
                    maxCombo=combo
                if combo<minCombo:
                    minCombo=combo
                    
                avgCombo+=combo
                avgscore+=score
                avgPerfect+=int(a[9])
            
            top100count=len(plays)
            if top100count>0:    
                avgCombo=avgCombo/top100count
                avgscore=avgscore/top100count
                avgPerfect=avgPerfect/top100count
            else:
                minscore=0
                minCombo=0
            amplscore=maxscore-minscore
            amplCombo=maxCombo-minCombo
            x=[maxscore, minscore, avgscore, amplscore, maxCombo, minCombo, avgCombo, amplCombo, avgPerfect, top100count]
            for a in x:
                details.append(a)
            self.dbQueue.put([details,plays])
    def start(self):
        self.main.log.msg('0','Process: Starting thread.')
        a=threading.Thread(target=self.worker,args=[])
        self.main.threads.append(a)
        a.start()
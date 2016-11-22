import time
import config
import threading
import varcheck

class Db:
    def __init__(self,main):
        self.main=main
        self.dbInit()
        if config.database.backend=='sqlite3':
            self.close()
        
    def dbInit(self):
        if config.database.backend=='sqlite3':
            import sqlite3 as baza
            self.baza=baza.connect(config.database.file)
        elif config.database.backend=='mysql':
            import MySQLdb as baza
            self.baza=baza.connect(host=config.database.host, user=config.database.user, passwd=config.database.password, charset="utf8")
        self.kursor=self.baza.cursor()
        self.setup()
    def setup(self):
        if config.database.backend=='mysql':
            self.kursor.execute("set names utf8;")
            try:
                self.kursor.execute(u'use {0};'.format(config.database.database))
            except:
                self.kursor.execute(u'create database {0} CHARACTER SET utf8 COLLATE utf8_general_ci'.format(config.database.database))
                self.kursor.execute(u'use {0};'.format(config.database.database))
        self.kursor.execute(u'create table if not exists beatmaps(approved int, approved_date date , last_update date , artist text , beatmap_id text, beatmapset_id text, bpm int, creator text, star_diff real, cs real, oa real, ar real, hp real, hit_lenght int, source text, genre_id text, language_id text, title text , total_lenght int, diff_name text, file_hash text, mode text, tags text, favourite_count int, play_count int, pass_count int, max_combo int, max_gained_score int, min_gained_score int, avg_gained_score real, ampl_gained_score real , max_gained_combo int , min_gained_combo int , avg_gained_combo real , ampl_gained_combo real , avg_perfect real , top100count int );')
        self.kursor.execute(u'create table if not exists plays( beatmap_id text , score int , username text , count_300 int , count_100 int , count_50 int , count_miss int , max_combo int , count_katu int , count_geki int , perfect int , enabled_mods int , user_id text , date date , rank text , pp real );')

    def close(self):
        self.kursor.close()
        self.baza.commit()
        self.baza.close()
    def commit(self):
        self.baza.commit()
        
    def worker(self):
        #threading workaround
        if config.database.backend=='sqlite3':
            self.dbInit()
            
            
        self.main.log.msg('0','Db: Thread started.')
        
        
        while self.main.working:
            a=self.main.process.dbQueue.get()
            if not self.beatmapExists(a[0][4]):
                self.addBeatmap(a[0],False)
            else:
                self.deletePlays(a[0][4],False)
                self.deleteBeatmap(a[0][4],False)
                self.addBeatmap(a[0],False)
            for b in a[1]:
                self.addPlay(a[0][4], b,False)
            self.commit()
            
        
    def start(self):
        self.main.log.msg('0','Db: Starting thread.')
        a=threading.Thread(target=self.worker,args=[])
        self.main.threads.append(a)
        a.start()
    def getType(self,a):
        return str(type(a)).split("'")[1].split("'")[0]
    
    def addBeatmap(self, beatmap, commit=True):
        zapytanie=u"""insert into beatmaps(approved, approved_date, last_update, artist  , beatmap_id  , beatmapset_id  , bpm  , creator  , star_diff  , cs  , oa  , ar  , hp  , hit_lenght  , source  , genre_id  , language_id  , title  , total_lenght  , diff_name  , file_hash  , mode  , tags  ,favourite_count  , play_count  , pass_count  , max_combo  , max_gained_score  , min_gained_score  , avg_gained_score  , ampl_gained_score  , max_gained_combo  , min_gained_combo  , avg_gained_combo  , ampl_gained_combo  , avg_perfect , top100count  ) values({approved},"{approved_date}","{last_update}","{artist}","{beatmap_id}","{beatmapset_id}",{bpm},"{creator}",{star_diff},{cs},{oa},{ar},{hp},{hit_lenght},"{source}","{genre_id}","{language_id}","{title}",{total_lenght},"{diff_name}","{file_hash}","{mode}","{tags}",{favourite_count},{play_count},{pass_count},{max_combo},{max_gained_combo},{min_gained_score},{avg_gained_score},{ampl_gained_score},{max_gained_combo},{min_gained_combo},{avg_gained_combo},{ampl_gained_combo},{avg_perfect},{top100count});""".format(approved=beatmap[0] ,approved_date=beatmap[1] ,last_update=beatmap[2] ,artist=beatmap[3] ,beatmap_id=beatmap[4] ,beatmapset_id=beatmap[5] ,bpm=beatmap[6] ,creator=beatmap[7] ,star_diff=beatmap[8] ,cs=beatmap[9] ,oa=beatmap[10] ,ar=beatmap[11] ,hp=beatmap[12] ,hit_lenght=beatmap[13] ,source=beatmap[14] ,genre_id=beatmap[15] ,language_id=beatmap[16] ,title=beatmap[17] ,total_lenght=beatmap[18] ,diff_name=beatmap[19] ,file_hash=beatmap[20] ,mode=beatmap[21] ,tags=beatmap[22] ,favourite_count=beatmap[23] ,play_count=beatmap[24] ,pass_count=beatmap[25] ,max_combo=beatmap[26] ,max_gained_score=beatmap[27] ,min_gained_score=beatmap[28] ,avg_gained_score=beatmap[29] ,ampl_gained_score=beatmap[30] ,max_gained_combo=beatmap[31] ,min_gained_combo=beatmap[32] ,avg_gained_combo=beatmap[33] ,ampl_gained_combo=beatmap[34] ,avg_perfect=beatmap[35] ,top100count=beatmap[36])
        self.kursor.execute(zapytanie.encode('utf-8'))
        if commit:
            self.commit()
    def beatmapExists(self,beatmap_id):
        zapytanie=u"""select * from beatmaps where beatmap_id="{0}";""".format(beatmap_id)
        self.kursor.execute(zapytanie)
        g=[]
        for a in self.kursor:
            g.append(a)
        w=0
        for a in g:
            for b in a:
                if beatmap_id == b:
                    w+=1
        if w>0:
            print 'duplikat'
            return True
        else:
            return False
    
    def deleteBeatmap(self,beatmap_id, commit=True):
        zapytanie=u"""delete from beatmaps where beatmap_id={0}""".format(beatmap_id)
        self.kursor.execute(zapytanie)
        if commit:
            self.commit()
    
    
    
    def deletePlays(self,beatmap_id,commit=True):
        zapytanie=u"""delete from plays where beatmap_id={0}""".format(beatmap_id)
        self.kursor.execute(zapytanie)
        if commit:
            self.commit()
        
    def addPlay(self, beatmap_id,play,commit=True):
        pla=play
        play=varcheck.Varcheck(pla)
        zapytanie=u"""insert into plays( beatmap_id  , score  , username  , count_300  , count_100  , count_50  , count_miss  , max_combo  , count_katu  , count_geki  , perfect  , enabled_mods  , user_id  , date , rank  , pp) values("{beatmap_id}",{score},"{username}",{count_300},{count_100},{count_50},{count_miss},{max_combo},{count_katu},{count_geki},{perfect},{enabled_mods},"{user_id}","{date}","{rank}",{pp});""".format(beatmap_id=beatmap_id,score=play[0],username=play[1],count_300=play[2],count_100=play[3],count_50=play[4],count_miss=play[5],max_combo=play[6],count_katu=play[7],count_geki=play[8],perfect=play[9],enabled_mods=play[10],user_id=play[11],date=play[12],rank=play[13],pp=play[14])
        self.kursor.execute(zapytanie)
        if commit:
            self.commit()
                
import re
import Queue
import threading
import config
import requests
import time 

class Parser:
    def __init__(self,main):
        self.main=main
        self.idQueue=Queue.Queue()
    def getBeatmapsDetails(self):
        #[approved, approved_date, last_update, artist, beatmap_id, beatmapset_id, bpm, creator, star_diff, cs, oa, ar, hp, lenght, source, genre_id, language_id, title, total_lenght, diff_name, file_hash, game_mode, tags, favourite_count, play_count, pass_count, max-combo]
        w=requests.get("https://osu.ppy.sh//api/get_beatmaps?k={key}".format(key=config.osuapi.key))
        i=[]
        a=w.json()
        for c in a:    
            i.append(c['beatmap_id'])
        return i
       
    def worker(self):
        self.main.log.msg('0','Parser: Thread started.')
        while self.main.working:
            a=self.getBeatmapsDetails()
            self.idQueue.put(a)
            time.sleep(60*30)
    def start(self):
        self.main.log.msg('0','Parser: Starting thread.')
        a=threading.Thread(target=self.worker,args=[])
        self.main.threads.append(a)
        a.start()
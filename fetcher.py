import re
import Queue
import threading
import config
import requests
import varcheck
import time
class Fetcher:  
    def __init__(self,main):
        self.main=main
        self.processQueue=Queue.Queue()
    def getBeatmapDetails(self,beatmapid):
        #[approved, approved_date, last_update, artist, beatmap_id, beatmapset_id, bpm, creator, star_diff, cs, oa, ar, hp, lenght, source, genre_id, language_id, title, total_lenght, diff_name, file_hash, game_mode, tags, favourite_count, play_count, pass_count, max-combo]
        w=requests.get(u"https://osu.ppy.sh//api/get_beatmaps?k={key}&b={beatmap_id}".format(key=config.osuapi.key,beatmap_id=beatmapid))
        
        b=w.json()[0]
        a=varcheck.Varcheck(b)
        return [a['approved'],a['approved_date'],a['last_update'],a['artist'],a['beatmap_id'],a['beatmapset_id'],a['bpm'],a['creator'],a['difficultyrating'],a['diff_size'],a['diff_overall'],a['diff_approach'],a['diff_drain'],a['hit_length'],a['source'],a['genre_id'],a['language_id'],a['title'],a['total_length'],a['version'],a['file_md5'],a['mode'],a['tags'],a['favourite_count'],a['playcount'],a['passcount'],a['max_combo']]
    def getBeatmapPlays(self,beatmapid):
        #[beatmap_id,score, username, count_300, count_100, count_50, count_miss, max_combo, count_katu, count_geki, perfect, enabled_mods, user_id, date, rank_grade, pp]
        w=requests.get("https://osu.ppy.sh//api/get_scores?k={key}&b={beatmap_id}&limit=100".format(key=config.osuapi.key,beatmap_id=beatmapid))
        b=w.json()
        wyn=[]
        for a in b:
            wyn.append([a['score'],a['username'],a['count300'],a['count100'],a['count50'],a['countmiss'],a['maxcombo'],a['countkatu'],a['countgeki'],a['perfect'],a['enabled_mods'],a['user_id'],a['date'],a['rank'],a['pp']])
        return wyn
    
    
    
    def getBeatmapsDetails(self):
        #[approved, approved_date, last_update, artist, beatmap_id, beatmapset_id, bpm, creator, star_diff, cs, oa, ar, hp, lenght, source, genre_id, language_id, title, total_lenght, diff_name, file_hash, game_mode, tags, favourite_count, play_count, pass_count, max-combo]
        w=requests.get("https://osu.ppy.sh//api/get_beatmaps?k={key}&since={since}".format(key=config.osuapi.key,since=config.beatmaps.since))
        i=[]
        a=w.json()
        for c in a:    
            i.append(unicode(c[u'beatmap_id']))
        return i
    
        
    def worker(self):
        self.main.log.msg('0','Fetcher: Thread started.')
        while self.main.working:
            
            a=self.getBeatmapsDetails()
            for b in a:
                details=self.getBeatmapDetails(b)
                plays=self.getBeatmapPlays(b)
                self.processQueue.put([details,plays])
            time.sleep(60)
    def start(self):
        self.main.log.msg('0','Fetcher: Starting thread.')
        a=threading.Thread(target=self.worker,args=[])
        self.main.threads.append(a)
        a.start()
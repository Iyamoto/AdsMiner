# AdsMiner: Get Ads Networks from grab.py log files

import os
import re
from urllib.parse import urlparse
import adsminer
    
stats = {}
cookies_dir = ''
cookies_file = 'cookies.txt'
low_limit=0 # ?????
total = 0
cookies_path = os.path.join(cookies_dir, cookies_file)
if os.path.isfile(cookies_path) == True:
    text = adsminer.file2text(cookies_path)
        
##        for url_id in url_ids:
##            for href in url_id[5]:
##                domain = adsminer.getDomainfromUrl(href)
##                if len(domain)>1:
##                    stats[domain] = stats.get(domain,0)+1
##                    total+=1
                        
print('Total Links found: ',  total)
if total>0:
    list_stats = []
    for k,v in stats.items():
        if v>low_limit:
            percent = int(100*v/total)
            list_stats.append((k,v,percent))
        
    sorted_stats = sorted(list_stats, key=adsminer.getIndex1,reverse=True)
    for items in sorted_stats:
        try:
            print(items[0], items[1], str(items[2])+'%')
        except:
            continue
            



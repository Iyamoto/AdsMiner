# AdsMiner: Get Ads Networks from grab.py log files

import os
from urllib.parse import urlparse
import adsminer
    
stats = {}
json_dir = 'json'
low_limit=5 # ?????
total = 0
for file in os.listdir(json_dir):
    if file.endswith('.txt'):
        print('Reading json file: ',file)
        json_path = os.path.join(json_dir, file)
        if os.path.isfile(json_path) == True:
            url_ids = adsminer.readJson(json_path)
            for url_id in url_ids:
                for href in url_id[2]:
                    domain = adsminer.getDomainfromUrl(href)
                    if len(domain)>1:
                        stats[domain] = stats.get(domain,0)+1
                        total+=1
print('Total Links found: ',  total)                        
list_stats = []
for k,v in stats.items():
    if v>low_limit:
        percent = int(100*v/total)
        list_stats.append((k,v,percent))
    
sorted_stats = sorted(list_stats, key=adsminer.getIndex1,reverse=True)
for items in sorted_stats:
    print(items[0], items[1], str(items[2])+'%')
            



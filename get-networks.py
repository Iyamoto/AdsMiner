# AdsMiner: Get Ads Networks from grab.py log.txt

import os
from urllib.parse import urlparse
import adsminer
      
stats = {}
logs_dir = 'logs'
low_limit=5
for file in os.listdir(logs_dir):
    if file.endswith('.txt'):
        print('Reading log file: ',file)
        log_path = os.path.join(logs_dir, file)
        if os.path.isfile(log_path) == True:
            lines = adsminer.file2list(log_path)
            for line in lines:
                if line.find('href: ')>=0:
                    domain = adsminer.getDomainfromUrl(line.split()[1])
                    if len(domain)>1:
                        stats[domain] = stats.get(domain,0)+1
list_stats = []
for k,v in stats.items():
    if v>low_limit:
        list_stats.append((k,v))
    
sorted_stats = sorted(list_stats, key=adsminer.getIndex1,reverse=True)
for items in sorted_stats:
    print(items[0], items[1])
            



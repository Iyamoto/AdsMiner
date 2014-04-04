# AdsMiner: Get Ads Networks from grab.py log.txt

import os.path
from urllib.parse import urlparse
import adsminer

log_path = 'log.txt'
stats = {}

low_limit=5

if os.path.isfile(log_path) == True:
    lines = adsminer.file2list(log_path)
    for line in lines:
        if line.find('href: ')>=0:
            domain = adsminer.getDomainfromUrl(line.split()[1])
            stats[domain] = stats.get(domain,0)+1
list_stats = []
for k,v in stats.items():
    if v>low_limit:
        list_stats.append((k,v))
    
sorted_stats = sorted(list_stats, key=adsminer.getIndex1,reverse=True)
print(sorted_stats)            
            



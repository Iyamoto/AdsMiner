# AdsMiner: Get Ads Networks from grab.py log.txt

import os.path
from urllib.parse import urlparse
import adsminer
import configparser

config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False
    
log_file = os.path.join('logs', config['GRABBER']['Urls'])
stats = {}

low_limit=5

if os.path.isfile(log_file) == True:
    lines = adsminer.file2list(log_file)
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
            



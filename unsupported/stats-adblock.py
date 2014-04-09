# Compare found ad domains with domains from adblock list

import os
import re
from urllib.parse import urlparse
import adsminer
    
stats = {}
json_dir = 'json'
lists_dir = 'info'
limit = 0
ad_domains = []
domains_counters = {}
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
                        domains_counters[domain] = domains_counters.get(domain,0)+1
                        ad_domains.append(domain)

ad_domains = adsminer.uniqList(ad_domains)
print('Domains in lists found: '+ str(len(ad_domains)))

domains_from_adblock = []
for file in os.listdir(lists_dir):
    if file.endswith('advblock.txt'):
        print('Reading url list file: ',file)
        list_path = os.path.join(lists_dir, file)
        if os.path.isfile(list_path) == True:
            urls = adsminer.file2list(list_path)
            if len(urls)>0:
                for url in urls:
                    if url[0]=='|' and url[1]=='|':
                        needle = re.search(r'([^\/]+)\/', url[2:])
                        try:
                            if needle.group(1).find('.')!=-1:
                                domains_from_adblock.append(needle.group(1))
                        except:
                            continue
                    
domains_from_adblock = adsminer.uniqList(domains_from_adblock)
print('Domains in adblock list found: '+ str(len(domains_from_adblock)))            

suspects = []
for ad_domain in ad_domains:
    if ad_domain in domains_from_adblock:
        if domains_counters[ad_domain] > limit:
            suspects.append([ad_domain, domains_counters[ad_domain]])

stats = sorted(suspects, key=adsminer.getIndex1, reverse=True)
for pairs in stats:
    print(pairs[0], pairs[1])

            



# Compare domains from cookies.txt with domains from adblock list

import os
import re
from urllib.parse import urlparse
import adsminer
    
cookies_dir = ''
cookies_file = 'cookies.txt'
lists_dir = 'info'
limit = 5
domains_counters = {}
total = 0
cookies_path = os.path.join(cookies_dir, cookies_file)
if os.path.isfile(cookies_path) == True:
    text = adsminer.file2text(cookies_path)
    matches = re.findall(r'domain=\.([^;]+);', text)
    for domain in matches:
        domains_counters[domain] = domains_counters.get(domain,0)+1
    domains_from_cookies = adsminer.uniqList(matches)
    print('Domains in cookies found: '+ str(len(domains_from_cookies)))

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
for domain_from_cookies in domains_from_cookies:
    if domain_from_cookies in domains_from_adblock:
        if domains_counters[domain_from_cookies] > limit:
            suspects.append([domain_from_cookies, domains_counters[domain_from_cookies]])

stats = sorted(suspects, key=adsminer.getIndex1, reverse=True)
for pairs in stats:
    print(pairs[0], pairs[1])

            



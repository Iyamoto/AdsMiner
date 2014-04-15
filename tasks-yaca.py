# Tasks creator for grab2.py
# A Paginator extraction and links accumulation
# Parses urls from YaCa
# Give a key or a category url
# Assign a task name
# Puts a task file(urls list) with the given name to the tasks dir

import configparser
import hashlib
import os.path
from urllib.parse import quote_plus
from urllib.parse import urlparse
import re
import adsminer

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

# Init
tasksdir = 'tasks'
infodir = 'info'
listsdir = 'lists'
if not os.path.exists(tasksdir):
    os.makedirs(tasksdir)
datadir = config['GRABBER']['DataDir']
if not os.path.exists(datadir):
    os.makedirs(datadir)
run = config['GRABBER']['Run']

category_path = os.path.join(infodir, 'women.txt')
category_raw = adsminer.file2list(category_path)
category_data = {}
for line in category_raw:
    if line[0]=='#' or len(line.strip())==0:
        continue
    items = line.strip().split(';')
    category_data[items[0]] = items[1]


##key = 'рецепты'
##urlkey = quote_plus(key)
##starturl = 'http://yaca.yandex.ru/yca/cat/?text='
##url = starturl+urlkey

for name, url in category_data.items():
    print(name,url)
    list_path = os.path.join(listsdir, name+'.txt')
    if os.path.isfile(list_path) == True:
        print('Already exists')
        continue

    task_name = name
    pagi_list_path = os.path.join(tasksdir, task_name+'.txt')
    isLogFile = adsminer.initLog(pagi_list_path)

    baseurl = urlparse(url).netloc
    scheme = urlparse(url).scheme

    while True:
        url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
        path = os.path.join(datadir, url_id + '.html')

        html = adsminer.url2htmlW(run, url, path)
        # Get links
        matches = re.findall(r'<a[^>]+>.+</a>', html)  
        for match in matches:
            if match.find('result__name')>0:
                tmp = re.search(r'href="([^"]+)"',match)
                link = tmp.group(1)
                adsminer.writeLog(pagi_list_path,link+'\n',isLogFile)
        # Find next
        match = re.findall(r'<a[^>]+>следующая</a>', html)
        if len(match)==1:
            next = re.search(r'href="([^"]+)"',match[0])
            url = scheme+'://'+baseurl+next.group(1)
            print(url)        
        else:
            break

    print('Done')

    

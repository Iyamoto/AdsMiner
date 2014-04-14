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
if not os.path.exists(tasksdir):
    os.makedirs(tasksdir)
datadir = config['GRABBER']['DataDir']
if not os.path.exists(datadir):
    os.makedirs(datadir)
run = config['GRABBER']['Run']

##key = 'рецепты'
##urlkey = quote_plus(key)
##starturl = 'http://yaca.yandex.ru/yca/cat/?text='
##url = starturl+urlkey
url = 'http://yaca.yandex.ru/yca/cat/Rest/Hobby/Needlework/'

task_name = 'needlework'

pagi_list_path = os.path.join(tasksdir, task_name+'.txt')
isLogFile = adsminer.initLog(pagi_list_path)

baseurl = urlparse(url).netloc
scheme = urlparse(url).scheme

print(baseurl)

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

    

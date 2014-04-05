# A Paginator extraction and links accumulation

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
##urlsfile = config['GRABBER']['Urls']
datadir = config['GRABBER']['DataDir']
run = config['GRABBER']['Run']

##lists_dir = os.path.dirname(urlsfile)
pagi_list_path = os.path.join('tasks', 'pagi.txt')
isLogFile = adsminer.initLog(pagi_list_path)

key = 'рецепты'
urlkey = quote_plus(key)
starturl = 'http://yaca.yandex.ru/yca/cat/?text='
url = starturl+urlkey
url = 'http://yaca.yandex.ru/yca/cat/Private_Life/Family/Parents/'

baseurl = urlparse(url).netloc
scheme = urlparse(url).scheme

print(baseurl)

while True:
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = os.path.join(datadir, url_id + '.html')

    html = adsminer.url2html(run, url, path)
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

    

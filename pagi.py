# A Paginator extraction

import configparser
import hashlib
import os.path
from urllib.parse import quote_plus
import adsminer

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

# Init
urlsfile = config['GRABBER']['Urls']
datadir = config['GRABBER']['DataDir']
run = config['GRABBER']['Run']

lists_dir = os.path.dirname(urlsfile)
pagi_list_path = os.path.join(lists_dir, 'pagi.txt')

key = 'гороскоп'
url = quote_plus('http://yaca.yandex.ru/yca/cat/?text='+key)
print(url)
assert False


url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
path = os.path.join(datadir, url_id + '.html')

if os.path.isfile(path) == False:
    code = adsminer.url2file(run, url, path)
    assert code==True
try:
    text = adsminer.file2text(path)
except:
    print('Cant read file '+path)
    assert False
    

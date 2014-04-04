# AdsMiner:Grabber
# TODO http://www.myjane.ru/articles/rubric/?id=54 =?

import configparser
import hashlib
import os.path
import adsminer

# Test Harness
test_data = {}
test_data['http://gotovim-doma.ru/']=9
test_data['http://horo.tochka.net/']=2 #????
test_data['http://www.edimdoma.ru/retsepty']=4
test_data['http://www.mycharm.ru/']=4
test_data['http://onbeauty.ru/']=6
test_data['http://yeswoman.ru/']=11
test_data['http://www.astrocentr.ru/']=8
test_data['http://astroscope.ru/']=13
test_data['http://www.sonniki.net.ru/']=4

def test_parseBlocks(url,num):
    test_data[url] = test_data.get(url, 0)
    msg = 'Testing: '+url+' Should be: ' + str(test_data[url]) + ' Got: ' + str(num)
    print(msg)
    diff = abs(num - test_data[url])
    return diff

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
block_complexity = int(config['GRABBER']['BlockComplexity'])
log_file = config['GRABBER']['LogFile']
maxBlockSize = int(config['GRABBER']['MaxBlockSize'])
minBlockSize = int(config['GRABBER']['MinBlockSize'])
maxLinks = int(config['GRABBER']['MaxLinks'])

# TODO add multi lists support

urls = test_data.keys()
if len(urls)==0:
    print('No urls found')
    assert False

total_diff = 0

for url in urls:
    try:
        url = adsminer.clearUrl(url)
    except:
        continue
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = datadir + url_id + '.html'

    #print(url, path)
    if os.path.isfile(path) == False:
        code = adsminer.url2file(run, url, path)
        if code==False:
            print('Cant get url: '+url)
            continue        
    try:
        text = adsminer.file2text(path)
    except:
        print('Cant read file '+path)
        continue
    
    # TODO add tidy html?
    ads = adsminer.parseBlocks(text, url, block_complexity, minBlockSize, maxBlockSize, maxLinks)
    assert type(ads)==dict
    ads_num = len(ads.keys())
    
    # Test Harness
    diff = test_parseBlocks(url,ads_num)
    total_diff += diff

    del(ads)
    #break

print('Total diff: '+str(total_diff))

# AdsMiner: Grabber optimizer
# TODO http://www.myjane.ru/articles/rubric/?id=54 =?

import configparser
import hashlib
import os.path
import adsminer
from datetime import datetime

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
##    msg = 'Testing: '+url+' Should be: ' + str(test_data[url]) + ' Got: ' + str(num)
##    print(msg)
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

# For maxLinks
##maxLinks = 8 
##min_opt, max_opt, step_opt = 0,12,1

# For block_complexity
##block_complexity = 0
#min_opt, max_opt, step_opt = 0,4,1

# For minBlockSize
##minBlockSize = 70
#min_opt, max_opt, step_opt = 10,100,5

# For maxBlockSize
##maxBlockSize = 70
min_opt, max_opt, step_opt = 150,300,10

# TODO add multi lists support

urls = test_data.keys()
if len(urls)==0:
    print('No urls found')
    assert False

opt_data = []
text_buckets = {}
startTime = datetime.now()

for test_param in range(min_opt, max_opt, step_opt):    
    #maxLinks = test_param
    #block_complexity = test_param
    #minBlockSize = test_param
    maxBlockSize = test_param
    total_diff = 0

    for url in urls:
        try:
            url = adsminer.clearUrl(url)
        except:
            continue
        url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
        path = datadir + url_id + '.html'

        # Trading memory for file IO
        # Need less file IO?
        if url not in text_buckets.keys():
            text_buckets[url] = adsminer.url2html(run, url, path)
        text = text_buckets.get(url)
        # Need less memory usage?
        #text = adsminer.url2html(run, url, path) # Should I keep em in memory? Yes
        
        # TODO add tidy html?
        ads = adsminer.parseBlocks(text, url, block_complexity, minBlockSize, maxBlockSize, maxLinks)
        ads_num = len(ads.keys())
        
        # Test Harness
        diff = test_parseBlocks(url,ads_num)
        total_diff += diff

        del(ads)
        #break

    print('Param: '+ str(test_param) +' Total diff: '+str(total_diff))
    opt_data.append([test_param, total_diff])

sorted_data = sorted(opt_data, key=adsminer.getIndex1)
print('Best param: '+ str(sorted_data[0][0]))
print('Optimization time: ',datetime.now()-startTime)

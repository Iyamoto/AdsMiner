# AdsMiner:Grabber

import configparser
import hashlib
import os.path
import adsminer

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

# Init
urlsdir = 'lists'
logsdir = 'logs'
jsondir = 'json'
if not os.path.exists(logsdir):
    os.makedirs(logsdir)
if not os.path.exists(jsondir):
    os.makedirs(jsondir)

urlsfile = os.path.join(urlsdir, config['GRABBER']['Urls'])
jsonfile = os.path.join(jsondir, config['GRABBER']['Urls'])
datadir = config['GRABBER']['DataDir']
if not os.path.exists(datadir):
    os.makedirs(datadir)
run = config['GRABBER']['Run']
run1 = config['GRABBER']['Run1']
block_complexity = int(config['GRABBER']['BlockComplexity'])
log_file = os.path.join(logsdir, config['GRABBER']['Urls'])
maxBlockSize = int(config['GRABBER']['MaxBlockSize'])
minBlockSize = int(config['GRABBER']['MinBlockSize'])
maxLinks = int(config['GRABBER']['MaxLinks'])
Timeout = int(config['GRABBER']['Timeout'])

urls = adsminer.file2list(urlsfile)
if len(urls)==0:
    print('No urls found')
    assert False

to_json = []

for url in urls:
    try:
        url = adsminer.clearUrl(url)
    except:
        continue
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = os.path.join(datadir, url_id + '.html')

    print(url, path)
    text = adsminer.url2html(run, url, path, Timeout)
    
    ads = adsminer.parseBlocks(text, url, block_complexity, minBlockSize, maxBlockSize, maxLinks)
    try:
        ads_num = len(ads.keys())
    except:
        del(ads)
        continue
    
    if ads_num>0:
        for id in ads.keys():
            target_urls = []
            # Accumulating json data
            json_block = adsminer.Block2List(url, id, ads[id])
            for target_url in json_block[2]:
                print(target_url)
                output = adsminer.url2url(run1, target_url, url)
                target_urls.append(output.strip())
                print(output)
            json_block.append(target_urls)

            #to_json.append(json_block)                
    
    del(ads)
    break

# Writing json data to file
##adsminer.writeJson(jsonfile, to_json)

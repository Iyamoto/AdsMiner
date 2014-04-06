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

isLogFile = adsminer.initLog(log_file,'Grabber started\n')

urls = adsminer.file2list(urlsfile)
if len(urls)==0:
    print('No urls found')
    assert False

total_blocks = 0
to_json = []

for url in urls:
    try:
        url = adsminer.clearUrl(url)
    except:
        continue
    adsminer.writeLog(log_file, url+'\n', isLogFile)
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
    total_blocks +=ads_num
      
    adsminer.writeLog(log_file, 'Find ads: '+str(ads_num)+'\n', isLogFile)
    
    if ads_num>0:
        for id in ads.keys():
            if isLogFile:
                # Comment next 2 lines if you dont need logs
                out = adsminer.getBlock(id,ads)
                adsminer.writeLog(log_file, out, isLogFile)
            
            # Accumulating json data
            target_urls = []
            json_block = adsminer.Block2List(url, id, ads[id])
            for target_url in json_block[2]:
                adsminer.writeLog(log_file, 'Redirecting: '+target_url+'\n', isLogFile)
                output = adsminer.url2url(run1, target_url, url)
                try:
                    target_urls.append(output.strip())
                except:
                    continue
                adsminer.writeLog(log_file, 'Landed: '+output+'\n', isLogFile)
            json_block.append(target_urls)
            to_json.append(json_block)                
    
    del(ads)
    #break

# Writing json data to file
adsminer.writeJson(jsonfile, to_json)

##from_json = adsminer.readJson(jsonfile)   
##print(from_json)

adsminer.writeLog(log_file, 'Total blocks found: '+str(total_blocks)+'\n', isLogFile)
adsminer.writeLog(log_file, 'Done\n', isLogFile)

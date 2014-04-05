# AdsMiner:Grabber2.0

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
procdir = 'proc'
logsdir = 'logs'
tasksdir = 'tasks'
if not os.path.exists(logsdir):
    os.makedirs(logsdir)
if not os.path.exists(urlsdir):
    os.makedirs(urlsdir)
if not os.path.exists(procdir):
    os.makedirs(procdir)    

#urlsfile = os.path.join('tasks', config['GRABBER']['Urls'])
 
datadir = config['GRABBER']['DataDir']
run = config['GRABBER']['Run']
block_complexity = int(config['GRABBER']['BlockComplexity'])
log_file = os.path.join(logsdir, config['GRABBER']['Urls'])
maxBlockSize = int(config['GRABBER']['MaxBlockSize'])
minBlockSize = int(config['GRABBER']['MinBlockSize'])
maxLinks = int(config['GRABBER']['MaxLinks'])

isLogFile = adsminer.initLog(log_file,'Grabber started\n')

# Looking for tasks
for file in os.listdir(tasksdir):
    if file.endswith('.txt'):
        print('Reading tasks file: ',file)
        tasks_path = os.path.join(tasksdir, file)
        proc_path = os.path.join(procdir, file)
        os.rename(tasks_path, proc_path) # Moving the task to proc dir

assert False

# TODO add multi lists support
urlsfile = proc_path
urls = adsminer.file2list(urlsfile)
if len(urls)==0:
    print('No urls found')
    assert False

total_blocks = 0

for url in urls:
    try:
        url = adsminer.clearUrl(url)
    except:
        continue
    adsminer.writeLog(log_file, url+'\n', isLogFile)
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = os.path.join(datadir, url_id + '.html')

    print(url, path)
    text = adsminer.url2html(run, url, path)
    
    # TODO add tidy html?
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
                out = adsminer.getBlock(id,ads)
                adsminer.writeLog(log_file, out, isLogFile)

    del(ads)
    #break

adsminer.writeLog(log_file, 'Total blocks found: '+str(total_blocks)+'\n', isLogFile)
adsminer.writeLog(log_file, 'Done\n', isLogFile)

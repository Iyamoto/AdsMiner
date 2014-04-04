# AdsMiner: Get Ads Networks from grab.py log.txt

import os.path
import adsminer

log_path = 'log.txt'

if os.path.isfile(log_path) == True:
    lines = adsminer.file2list(log_path)
    print(lines[0])



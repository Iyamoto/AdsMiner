# AdsMiner: Gets ref links from db src urls

import os
import adsminer
import configparser
import sys
from sqlalchemy import *
from urllib.parse import urlparse

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print(row)

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

driver = config['SQL']['driver']
host = config['SQL']['host']
user = config['SQL']['user']
password = config['SQL']['pass']
database = config['SQL']['db']
encode = config['SQL']['encode']

if encode == 'True':
    def encoding(val):
        return val.encode('utf-8')
else:
    def encoding(val):
        return val

try:
    lim = int(sys.argv[1])
except:
    lim = 20   
        
#Connect to db
db = create_engine(driver+'://'+user+':'+password+'@'+host+'/'+database)
db.echo = False
metadata = MetaData(db)
metadata.reflect()

addomains_table = Table('addomains', metadata, autoload=True)
landings_table = Table('landings', metadata, autoload=True)

filters = ('ref','partner','id')
blacklist = ('yandex.ru','begun.ru','adriver.ru','adfox.ru')
reflinks = []

for filter in filters:
    filter = '%'+filter+'%'
    s = text("""SELECT src_url FROM landings WHERE src_url LIKE :x""")
    rows = db.execute(s,x=filter).fetchall()
    for row in rows:
         reflinks.append(row[0])

reflinks = sorted(adsminer.uniqList(reflinks))
for reflink in reflinks:
    blacklisted = False
    query = urlparse(reflink).query.lower()
    base = urlparse(reflink).netloc.lower()
    if len(query)==0:
        continue
    if query.find('=')!=-1:
        for domain in blacklist:
            if base.find(domain)!=-1:
                blacklisted = True
                continue
        if not blacklisted:
            for filter in filters:
                if query.find(filter)!=-1:
                    print(reflink)
                    break

       

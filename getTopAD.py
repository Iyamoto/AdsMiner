# AdsMiner: Gets top ads domains from db
##SELECT addomains.id, addomains.domain, count( ad_domain_id )
##FROM landings
##INNER JOIN addomains ON landings.ad_domain_id = addomains.id
##GROUP BY ad_domain_id
##ORDER BY count( ad_domain_id ) DESC
##LIMIT 0 , 30

import os
import adsminer
from urllib.parse import urlparse
import configparser
from sqlalchemy import *

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
        
#Connect to db
db = create_engine(driver+'://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)

addomains_table = Table('addomains', metadata, autoload=True)

s = addomains_table.select(users.c.id == 1)
run(s)


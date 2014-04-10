# AdsMiner: Gets top ads domains from db
##SELECT addomains.id, addomains.domain, count( ad_domain_id )
##FROM landings
##INNER JOIN addomains ON landings.ad_domain_id = addomains.id
##GROUP BY ad_domain_id
##ORDER BY count( ad_domain_id ) DESC
##LIMIT 20

import os
import adsminer
import configparser
import sys
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

s = select([addomains_table.c.id, addomains_table.c.domain, \
func.count(landings_table.c.ad_domain_id)], \
from_obj=[addomains_table.join(landings_table,\
landings_table.c.ad_domain_id == addomains_table.c.id)]).\
group_by(landings_table.c.ad_domain_id).\
order_by(func.count(landings_table.c.ad_domain_id).desc()).\
limit(lim)

run(s)


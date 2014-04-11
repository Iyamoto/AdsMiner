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

infodir = 'info'
adnets_file = os.path.join(infodir, 'adnets.txt')
adnets = sorted(adsminer.uniqList(adsminer.file2list(adnets_file)))

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

print('id, domain, counter')
rows = s.execute()
for row in rows:
    print(row)

print()
print('New domains:')
for row in rows:
    for domain in adnets:
        if row[1].find(domain)!=-1:
            print(row[1])

            


# AdsMiner: Gets info about ad domain id from db
##select * from urls where id in
##(SELECT url_id FROM landings WHERE ad_domain_id = 1)
##select * from ads where id in
##(SELECT ad_id FROM landings WHERE ad_domain_id = 1)

import os
import sys
import adsminer
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
db = create_engine(driver+'://'+user+':'+password+'@'+host+'/'+database+'?charset=utf8')
db.echo = False
metadata = MetaData(db)
metadata.reflect()

##addomains_table = Table('addomains', metadata, autoload=True)
##landings_table = Table('landings', metadata, autoload=True)
##urls_table = Table('urls', metadata, autoload=True)

id = int(sys.argv[1])
s = text("""select * from urls where id in
(SELECT url_id FROM landings WHERE ad_domain_id = :x)""")
rows = db.execute(s,x=id).fetchall()
for row in rows:
     print(row[3])

s = text("""select * from ads where id in
(SELECT ad_id FROM landings WHERE ad_domain_id = :x)""")
rows = db.execute(s,x=id).fetchall()
for row in rows:
     print(row[2])





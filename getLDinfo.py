# AdsMiner: Gets landing domain info from db

import os
import adsminer
from urllib.parse import urlparse
import configparser
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
        
#Connect to db
db = create_engine(driver+'://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)


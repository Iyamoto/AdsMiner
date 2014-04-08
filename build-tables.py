# AdsMiner: Builds sql tables
# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.ResultProxy

import configparser
from sqlalchemy import *

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

host = config['MYSQL']['host']
user = config['MYSQL']['user']
password = config['MYSQL']['pass']
database = config['MYSQL']['db']


#Connect to db
#engine = create_engine('postgresql://'+user+':'+password+'@'+host+'/'+database)
db = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)

# Build tables
# Categories
##categories_table = Table('categories', metadata,
##    Column('id', Integer, primary_key=True),
##    Column('name', String(40)),
##)
##categories_table.create()
##ins = categories_table.insert()
##ins.execute(name='women')

# Sites
##sites_table = Table('sites', metadata,
##    Column('id', Integer, primary_key=True),
##    Column('domain', String(80)),
##)
##sites_table.create()

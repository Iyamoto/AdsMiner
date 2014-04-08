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
#db = create_engine('postgresql://'+user+':'+password+'@'+host+'/'+database)
db = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)

# Build tables
# 1.Categories (category_id, name)
categories_table = Table('categories', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(40)),
)
categories_table.create()
ins = categories_table.insert()
ins.execute(name='women')

# 2.Sites (site_id, domain)
sites_table = Table('sites', metadata,
    Column('id', Integer, primary_key=True),
    Column('domain', String(80)),
)
sites_table.create()

# 3.Urls (url_id, category_id, site_id, url)
urls_table = Table('urls', metadata,
    Column('id', Integer, primary_key=True),
    Column('category_id', Integer),
    Column('site_id', Integer),                   
    Column('url', String(255)),
)
urls_table.create()

# 4.Ads (ad_id, url_id, text, hash)
ads_table = Table('ads', metadata,
    Column('id', Integer, primary_key=True),
    Column('url_id', Integer),
    Column('text', Text),                   
    Column('hash', String(255)),
)
ads_table.create()

# 5.Landings (land_id, ad_id, url_id, src_url, land_url, time)
landings_table = Table('landings', metadata,
    Column('id', Integer, primary_key=True),
    Column('ad_id', Integer),
    Column('url_id', Integer),
    Column('src_url', String(255)),                       
    Column('land_url', String(255)),                   
    Column('time', String(255)),
)
landings_table.create()

# 6.Landdomains(land_id, domain)
landdomains_table = Table('landdomains', metadata,
    Column('id', Integer, primary_key=True),
    Column('domain', String(80)),
)
landdomains_table.create()

# 7.Images (img_id, ad_id, img_url)
images_table = Table('images', metadata,
    Column('id', Integer, primary_key=True),
    Column('ad_id', Integer),                
    Column('img_url', String(255)),
)
images_table.create()



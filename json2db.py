# AdsMiner: Adblocks from json to mysql
# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.ResultProxy

import os
import adsminer
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

# Get all sites
sites_table = Table('sites', metadata, autoload=True)
sel = sites_table.select()
sites_ins = sites_table.insert()
rs = sel.execute()
rows = rs.fetchall()

sites = {}
urls = {}

for row in rows:
    sites[row[1]] = row[0] # sites[domain]=id

urls_table = Table('urls', metadata, autoload=True)
urls_ins = urls_table.insert()
    
json_dir = 'json'
Category = 1

total = 0
for file in os.listdir(json_dir):
    if file.endswith('.txt'):
        print('Reading json file: ',file)
        json_path = os.path.join(json_dir, file)
        if os.path.isfile(json_path) == True:
            data = adsminer.readJson(json_path)
            for block in data:
##                try:
                # Forming adblock object
                ab = adsminer.adblock(block[0],block[1])
                for img in block[3]:
                    ab.addImgUrl(img)
                i=0
                for link in block[2]:
                    ab.addLink(link, block[5][i])
                    i+=1
                ab.addText(block[4])
                # Inserting adblock data int to db
                # 2.Sites (site_id, domain)
                # Check if domain is already in db
                if ab.getSrcDomain() not in sites.keys():
                    # Insert into the db.sites
                    rp = sites_ins.execute(domain=ab.getSrcDomain()) #returns ResultProxy
                    sites[ab.getSrcDomain()] = rp.lastrowid
                    total+=1
                # 3.Urls (url_id, category_id, site_id, url)
                # category_id = Category
                # site_id = sites[ab.getSrcDomain()]
                # url = ab.getSrcUrl
                rp = urls_ins.execute(category_id=Category, site_id = sites[ab.getSrcDomain()], url = ab.getSrcUrl)
                urls[ab.getSrcUrl] = rp.lastrowid
                break
                    
##                except:
##                    print('Cant get block')
##                    continue

print('Total domains inserted: ',  total)

          



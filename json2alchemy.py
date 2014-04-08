# AdsMiner: Adblocks from json to mysql

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
#engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
db = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)

# Get all sites
sites_table = Table('sites', metadata, autoload=True)
sel = sites_table.select()
ins = sites_table.insert()
rs = sel.execute()
rows = rs.fetchall()

sites = {}
for row in rows:
    sites[row[1]] = row[0] # sites[domain]=id
print(sites)

    
json_dir = 'json'

total = 0
for file in os.listdir(json_dir):
    if file.endswith('.txt'):
        print('Reading json file: ',file)
        json_path = os.path.join(json_dir, file)
        if os.path.isfile(json_path) == True:
            data = adsminer.readJson(json_path)
            for block in data:
##                try:
                ab = adsminer.adblock(block[0],block[1])
                for img in block[3]:
                    ab.addImgUrl(img)
                i=0
                for link in block[2]:
                    ab.addLink(link, block[5][i])
                    i+=1
                ab.addText(block[4])
                #Check if domain is already in the db
                if ab.getSrcDomain() not in sites.keys():
                    #Insert into the db
                    r = ins.execute(domain=ab.getSrcDomain())
                    print(help(r))
                
                break
                total+=1
##                except:
##                    print('Cant get block')
##                    continue

print('Total Links found: ',  total)

          



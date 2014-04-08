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

db.echo = True  # We want to see the SQL we're creating
metadata = MetaData(db)
#metadata = BoundMetaData(db)

sites = Table('sites', metadata, autoload=True)
s = sites.select()
rs = s.execute()
row = rs.fetchone()
print(row)

##conn = adsmysql.init_mysqldb()
##write2db = adsmysql.write2mysql
##
##sql = 'SELECT * FROM sites'
##data = adsmysql.execute_mysqldb(conn, sql)
##print(data)
##    
##json_dir = 'json'
##
##total = 0
##for file in os.listdir(json_dir):
##    if file.endswith('.txt'):
##        print('Reading json file: ',file)
##        json_path = os.path.join(json_dir, file)
##        if os.path.isfile(json_path) == True:
##            data = adsminer.readJson(json_path)
##            for block in data:
####                try:
##                ab = adsminer.adblock(block[0],block[1])
##                for img in block[3]:
##                    ab.addImgUrl(img)
##                i=0
##                for link in block[2]:
##                    ab.addLink(link, block[5][i])
##                    i+=1
##                ab.addText(block[4])
##                #print(ab.getSrcDomain())
##                row = []
##                row.append(('domain',ab.getSrcDomain()))
##                write2db(conn, 'sites', row)
##                break
##                total+=1
####                except:
####                    print('Cant get block')
####                    continue
##
##print('Total Links found: ',  total)
##
##
##adsmysql.kill_mysqldb(conn)
##
##            



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

sites = {}
urls = {}

#Connect to db
#db = create_engine('postgresql://'+user+':'+password+'@'+host+'/'+database)
db = create_engine('mysql+pymysql://'+user+':'+password+'@'+host+'/'+database)
db.echo = False  # We want to see the SQL we're creating
metadata = MetaData(db)

# Get all sites from db
sites_table = Table('sites', metadata, autoload=True)
sites_ins = sites_table.insert()
sel = sites_table.select()
rs = sel.execute()
rows = rs.fetchall()
for row in rows:
    sites[row[1]] = row[0] # sites[domain]=id

# Get all urls from db
urls_table = Table('urls', metadata, autoload=True)
urls_ins = urls_table.insert()
sel = urls_table.select()
rs = sel.execute()
rows = rs.fetchall()
for row in rows:
    urls[row[3]] = row[0] # urls[url]=id

# Inits ads table
ads_table = Table('ads', metadata, autoload=True)
ads_ins = ads_table.insert()

# Inits landings table
landings_table = Table('landings', metadata, autoload=True)
landings_ins = landings_table.insert()

# Inits images table
images_table = Table('images', metadata, autoload=True)
images_ins = landings_table.insert()
    
json_dir = 'json'
Category = 1

total_sites = 0
total_urls = 0
total_ads = 0
total_landings = 0
total_images = 0
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
                    total_sites+=1
                    
                # 3.Urls (url_id, category_id, site_id, url)
                # category_id = Category
                # site_id = sites[ab.getSrcDomain()]
                if ab.getSrcUrl() not in urls.keys():
                    url = ab.getSrcUrl().encode('utf-8')
                    rp = urls_ins.execute(category_id=Category, site_id = sites[ab.getSrcDomain()], url = url)
                    urls[ab.getSrcUrl()] = rp.lastrowid
                    total_urls+=1

                # 4.Ads (ad_id, url_id, text, hash)
                url_id = urls[ab.getSrcUrl()]
                text = ab.getText().encode('utf-8')
                hash = ab.getHash()
                rp = ads_ins.execute(url_id=url_id, text = text, hash = hash)
                ad_id = rp.lastrowid
                total_ads+=1
                #break

                # 5.Landings (land_id, ad_id, url_id, src_url, land_url, time)
                url_id = urls[ab.getSrcUrl()]
                time = ''
                links = ab.getLinks()
                for k,v in links.items():
                    src_url = k.encode('utf-8')
                    land_url = v.encode('utf-8')
                    rp = landings_ins.execute(ad_id=ad_id, url_id=url_id, src_url=src_url, land_url=land_url, time=time)
                    total_landings+=1

                #6.(land_id, landing_domain)


                #7.Images (img_id, ad_id, img_url)
                img_links = ab.ImgUrls()
                for img_link in img_links:
                    img_url = img_link.encode('utf-8')
                    rp = landings_ins.execute(ad_id=ad_id, img_url=img_url)
                    total_images+=1
                                      
##                except:
##                    print('Cant get block')
##                    continue

print('Total sites inserted: ',  total_sites)
print('Total urls inserted: ',  total_urls)
print('Total ads inserted: ',  total_ads)
print('Total landings inserted: ',  total_landings)
print('Total images inserted: ',  total_images)

          



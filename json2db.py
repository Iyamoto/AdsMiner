# AdsMiner: Adblocks from json to mysql
# http://docs.sqlalchemy.org/en/rel_0_9/core/connections.html#sqlalchemy.engine.ResultProxy

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
        
sites = {}
urls = {}
landdomains = {}

#Connect to db
db = create_engine(driver+'://'+user+':'+password+'@'+host+'/'+database)
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

# Get all land domains from db
landdomains_table = Table('landdomains', metadata, autoload=True)
landdomains_ins = landdomains_table.insert()
sel = landdomains_table.select()
rs = sel.execute()
rows = rs.fetchall()
for row in rows:
    landdomains[row[1]] = row[0] # landdomains[domain]=id

# Inits images table
images_table = Table('images', metadata, autoload=True)
images_ins = images_table.insert()
    
json_dir = 'json'
Category = 1

total_sites = 0
total_urls = 0
total_ads = 0
total_landings = 0
total_landdomains = 0
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
                if ab.getSrcDomain() not in sites.keys():
                    # Insert into the db.sites
                    rp = sites_ins.execute(domain=ab.getSrcDomain()) #returns ResultProxy
                    sites[ab.getSrcDomain()] = rp.inserted_primary_key[0]
                    total_sites+=1
                    
                # 3.Urls (url_id, category_id, site_id, url)
                if ab.getSrcUrl() not in urls.keys():
                    url = encoding(ab.getSrcUrl())
                    rp = urls_ins.execute(category_id=Category, site_id = sites[ab.getSrcDomain()], url = url)
                    urls[ab.getSrcUrl()] = rp.inserted_primary_key[0]
                    total_urls+=1

                #6.LandDomains (landdomain_id, domain)
                links = ab.getLinks()                    
                for k,v in links.items():
                    land_domain = urlparse(v).netloc.lower()
                    if land_domain not in landdomains.keys():
                        if len(land_domain)>0:
                            rp = landdomains_ins.execute(domain=land_domain)
                            landdomains[land_domain] = rp.inserted_primary_key[0]
                            total_landdomains+=1                    

                # 4.Ads (ad_id, url_id, text, hash)
                url_id = urls[ab.getSrcUrl()]
                text =  encoding(ab.getText())
                hash = ab.getHash()
                rp = ads_ins.execute(url_id=url_id, text = text, hash = hash)
                ad_id = rp.inserted_primary_key[0]
                total_ads+=1

                # 5.Landings (land_id, ad_id, url_id, src_url, land_url, time)
                url_id = urls[ab.getSrcUrl()]
                
                time = ''
                links = ab.getLinks()
                for k,v in links.items():
                    src_url =  encoding(k)
                    land_url =  encoding(v)
                    land_domain = urlparse(v).netloc.lower()
                    land_domain_id = landdomains[land_domain]
                    rp = landings_ins.execute(ad_id=ad_id, url_id=url_id, src_url=src_url, land_url=land_url, land_domain_id=land_domain_id)
                    total_landings+=1

                #7.Images (img_id, ad_id, img_url)
                for img_link in ab.getImgUrls():
                    img_url =  encoding(img_link)
                    rp = images_ins.execute(ad_id=ad_id, img_url=img_url)
                    total_images+=1
                                      
##                except:
##                    print('Cant get block')
##                    continue

print('Total sites inserted: ',  total_sites)
print('Total urls inserted: ',  total_urls)
print('Total ads inserted: ',  total_ads)
print('Total landings inserted: ',  total_landings)
print('Total land domains inserted: ',  total_landdomains)
print('Total images inserted: ',  total_images)

          



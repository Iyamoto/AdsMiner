# AdsMiner: Adblocks from json to mysql

import os
from urllib.parse import urlparse
import adsminer
import adsmysql

conn = adsmysql.init_mysqldb()
write2db = adsmysql.write2mysql

sql = 'SELECT * FROM sites'
data = adsmysql.execute_mysqldb(conn, sql)
print(data)
    
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
                #print(ab.getSrcDomain())
                row = []
                row.append(('domain',ab.getSrcDomain()))
                write2db(conn, 'sites', row)
                break
                total+=1
##                except:
##                    print('Cant get block')
##                    continue

print('Total Links found: ',  total)


adsmysql.kill_mysqldb(conn)

            



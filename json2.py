# AdsMiner: Get target domain stats

import os
from urllib.parse import urlparse
import adsminer
    
json_dir = 'json'

total = 0
for file in os.listdir(json_dir):
    if file.endswith('.txt'):
        print('Reading json file: ',file)
        json_path = os.path.join(json_dir, file)
        if os.path.isfile(json_path) == True:
            data = adsminer.readJson(json_path)
            for block in data:
                #try:
                ab = adsminer.adblock(block[0],block[1])
                for img in block[3]:
                    ab.addImgUrl(img)
                i=0
                for link in block[2]:
                    #print('src', i, link)
                    ab.addLink(link, block[5][i])
                    i+=1
                ab.addText(block[4])
                #for land in block[5]:
                    #print('land',land)  
                print(ab, ab.getLinks())
##                except:
##                    print('Cant get block')
##                    continue
print('Total Links found: ',  total)

            



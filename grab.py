# AdsMiner:Grabber
# TODO http://www.myjane.ru/articles/rubric/?id=54 =?

import subprocess
import configparser
import hashlib
import os.path
from urllib.parse import urlparse
from lxml import html
import codecs

def url2file(run, url, html, png=''):
    """PhantomJS wrapper
    url - http://name.tld
    html - where to save page code (html)
    png - where to save rendered page (image)"""
    cmd = run+' '+url+' '+html
    code = subprocess.call(cmd, shell=True)
    # TODO  check return code
    return code

def file2text(path):
    """Reads utf-8 file from path"""    
    path = str(path)
    f = codecs.open(path, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    return text

def file2list(path):
    """Reads utf-8 file from path"""    
    path = str(path)
    f = codecs.open(path, 'r', encoding='utf-8')
    # TODO if bad file?
    text = f.read()
    f.close()
    return text

def showBlocks(id, items):
    print('Start of:',id)
    for child in items[id].getchildren():
        #print(child.attrib)
        if child.tag=='a':
            if child.attrib.has_key('href'):
                print(child.attrib['href'])
            if child.attrib.has_key('title'):
                print(child.attrib['title'])
        if child.text!=None:
            print(child.text.strip())
        if child.tag=='img':
            print(child.attrib['src'])
    print('End of:',id)
    print()
    return None

def saveBlocks(id, items):
    out = 'Start of:'+str(id)+'\n'
    for child in items[id].getchildren():
        if child.tag=='a':
            if child.attrib.has_key('href'):
                out = out + child.attrib['href'] +'\n'
            if child.attrib.has_key('title'):
                out = out + child.attrib['title'] +'\n'
        if child.text!=None:
            out = out + child.text.strip()+'\n'
        if child.tag=='img':
            out = out + child.text.strip()+'\n'
    out = out + 'End of:' +str(id) +'\n'
    return out

def getAdBlocks(text, url=''):
    assert type(text)==str
    if len(url)>0:
        BaseUrl = urlparse(url).netloc
        tmp = BaseUrl.split('.')
        BaseUrl = tmp[-2]+'.'+tmp[-1]
    tree = html.document_fromstring(text)
    # TODO return code?
    data = {}
    items = {}
    id=0
    for element in tree.body.iter():
        items[id] = element
        pool = ()
        hasLink = False
        hasText = False
        LinkCounter=0
        for child in element.getchildren():
            if len(element.getchildren())>2:# Filter by amount of tags
                pool += (child.tag,)
                if child.tag == 'a':# Filter by tag (a href)
                    if child.attrib.has_key('href'):
                        if child.attrib['href'].find('http://')!=-1 and child.attrib['href'].find(BaseUrl)==-1:
                            hasLink = True
                        LinkCounter+=1
        if hasLink and LinkCounter==1:
            AdText=''
            for text in element.itertext():
                AdText += text.strip()
            if len(AdText)>0:
                data[id] = data.get(id,(element.tag,)) + pool
                id+=1
    return data, items

def file2list(file):
    lines = []
    f = open(file, 'rU')
    #TODO file check?
    for line in f:
        if len(line)>0:
            lines.append(line.strip())
    f.close()
    return lines

config = configparser.ConfigParser()
config.read('miner.conf')

urlsfile = config['DEFAULT']['Urls']
datadir = config['DEFAULT']['DataDir']
run = config['DEFAULT']['Run']

urls = file2list(urlsfile)

for url in urls:
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = datadir + url_id + '.html'

    print(url, path)
    if os.path.isfile(path) == False:
        code = url2file(run, url, path)    
    # TODO if bad return code?
    text = file2text(path)
    # TODO if bad return code?

    ads, blocks = getAdBlocks(text, url)
    print('Find ads:',len(ads))
    
    #for k,v in data.items(): print(k,v)

    f = codecs.open('log.txt', 'w', encoding='utf-8')

    for id in ads.keys():
        #showBlocks(id,blocks)
        out = saveBlocks(id,blocks)
        f.write(out)

    f.close()

    del(ads)
    del(blocks)
    #break


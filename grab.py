# AdsMiner:Grabber
# TODO http://www.myjane.ru/articles/rubric/?id=54 =?

import subprocess
import configparser
import hashlib
import os.path
from urllib.parse import urlparse
from lxml import html
import codecs

def url2file(run, url, html):
    """PhantomJS wrapper
    url - http://name.tld
    html - where to save page code (html)"""
    cmd = run+' '+url+' '+html
    try:
        code = subprocess.call(cmd, shell=True)
    except:
        print('Cant execute: '+cmd)
        return False
    return code

def file2text(path):
    """Reads utf-8 file from path"""
    try:
        f = codecs.open(path, 'r', encoding='utf-8')
    except:
        print('Cant read file: '+path)
        return ''
    text = f.read()
    f.close()
    return text

def file2list(path):
    """Reads utf-8 file from path
    Returns a list of lines"""
    lines = []
    try:
        f = open(path, 'rU')
    except:
        print('Cant read file: '+path)
        return lines
    for line in f:
        if len(line)>0:
            lines.append(line.strip())
    f.close()
    return lines

def showBlocks(id, items):
    """ Block print """
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
    """ Form human readable block """
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
            out = out + child.attrib['src']+'\n'
    out = out + 'End of:' +str(id) +'\n'
    return out

def getAdBlocks(text, url=''):
    """ Get ad (tiser) blocks from html
    A tiser is a block with 1 outer link, text and inner tag complexity
    text is a html code of the page
    url is a url of the page, needed for outer links detection"""
    assert type(text)==str
    if len(url)>0:
        BaseUrl = urlparse(url).netloc
        tmp = BaseUrl.split('.')
        BaseUrl = tmp[-2]+'.'+tmp[-1]
    try:
        tree = html.document_fromstring(text)
    except:
        print('Cant render html')
        return None # ????
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
            # Filter by amount of tags (block complexity)
            if len(element.getchildren())>2:
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

# Read config
config = configparser.ConfigParser()
try:
    config.read('miner.conf')
except:
    print('Cant read config file')
    assert False

urlsfile = config['DEFAULT']['Urls']
datadir = config['DEFAULT']['DataDir']
run = config['DEFAULT']['Run']

urls = file2list(urlsfile)
if len(urls)==0:
    print('No urls found')
    assert False

for url in urls:
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = datadir + url_id + '.html'

    print(url, path)
    if os.path.isfile(path) == False:
        code = url2file(run, url, path)
        if code==False:
            print('Cant get url: url')
            continue      
    try:
        text = file2text(path)
    except:
        print('Cant read file '+path)
        continue

    ads, blocks = getAdBlocks(text, url)
    print('Find ads:',len(ads))
    
    #for k,v in data.items(): print(k,v)
    
    if len(ads)>0:
        try:
            f = codecs.open('log.txt', 'a', encoding='utf-8')
        except:
            print('Cant open log file')
            continue
        for id in ads.keys():
            #showBlocks(id,blocks)
            out = saveBlocks(id,blocks)
            f.write(out)
        f.close()

    del(ads)
    del(blocks)
    #break


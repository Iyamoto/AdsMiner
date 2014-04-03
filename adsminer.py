# Functions for AdsMiner

import subprocess
from urllib.parse import urlparse
from lxml import html
import codecs
import re

def url2file(run, url, html):
    """PhantomJS wrapper
    url - http://name.tld
    html - where to save page code (html)"""
    cmd = run+' '+url+' '+html
    try:
        subprocess.call(cmd, shell=True)
    except:
        print('Cant execute: '+cmd)
        return False
    return True

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

def initLog(log_file):
    """ Log file init """
    try:
        f = codecs.open(log_file, 'w', encoding='utf-8')
    except:
        print('Cant open log file: '+log_file)
        return False
    out = 'Grabber started\n'
    # TODO add date and time
    f.write(out)
    f.close()
    return True

def writeLog(log_file, msg, isLogFile=True):
    """ Log file init """
    if isLogFile==True:
        assert type(msg)==str
        try:
            f = codecs.open(log_file, 'a', encoding='utf-8')
        except:
            print('Cant open log file: '+log_file)
            return False
        f.write(msg)
        f.close()
        return True
    else:
        return False

def showBlock(id, items):
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

def getBlock(id, items):
    """ Form human readable block """
    tags=''
    textSize = 0
    out = '=====Start of:'+str(id)+'\n'
    for child in items[id].getchildren():
        tags = tags + str(child.tag) + ' '
        if child.tag=='a':
            if child.attrib.has_key('href'):
                out = out + 'href: '+ child.attrib['href'] +'\n'
            if child.attrib.has_key('title'):
                out = out + 'title: '+ child.attrib['title'] +'\n'
                textLen = len(child.attrib['title'])
                textSize += textLen              
        if child.tag=='img':
            out = out + 'img src: ' +child.attrib['src']+'\n'
        if str(type(child))!='<class \'lxml.html.HtmlComment\'>':
            textLen = len(child.text_content().strip())
            if textLen>0:
                textSize += textLen
                out = out + str(child.tag) +' text: '+child.text_content().strip() + '\n'
            
    out = out + 'Text size: ' +str(textSize)+'\n'            
    out = out + 'Tags structure: ' +tags+'\n'           
    out = out + '=====End of:' +str(id) +'\n\n'
    return out

def parseBlocks(text, url='', block_complexity=2, minBlockSize=10, maxBlockSize=500, maxLinks=1):
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
        aTitles = ''
        LinkCounter=0
        for child in element.getchildren():
            # Filter html comments
            if str(type(child))=='<class \'lxml.html.HtmlComment\'>':
                continue
            # Filter by amount of tags (block complexity)
            if len(element.getchildren())>block_complexity:
                pool += (child.tag,)
                if child.tag == 'a':# Filter by tag (a href)
                    if child.attrib.has_key('href'):
                        if child.attrib['href'].find('http://')!=-1 and child.attrib['href'].find(BaseUrl)==-1:
                            hasLink = True
                        else:
                            hasLink = False
                        LinkCounter+=1
                    if child.attrib.has_key('title'):
                        aTitles = aTitles + child.attrib['title'].strip() + '\n'
        if hasLink and LinkCounter<=maxLinks:
            AdText=aTitles.strip()
            AdText+=element.text_content().strip()   
            AdSize = len(AdText)
            # print(AdSize)
            # Filter blocks without text and large blocks
            if AdSize>=minBlockSize and AdSize<=maxBlockSize:
                # How to filter counters? Block size?          
                # How to get rid of small blocks with only one link? No way
                # Lets try to parse out http* and check text size - bad idea

##                httpes = re.findall(r'http:[^:]+',AdText)
##                print('httpes',httpes, AdText, AdSize)

                # Finaly, block is good
                data[id] = data.get(id,(element.tag,)) + pool
                id+=1
    return data, items

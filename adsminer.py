# Functions for AdsMiner

import subprocess
from urllib.parse import urlparse
from lxml import html
import codecs
import re
import os.path

def clearUrl(url):
    """ Checking is string is an url """
    assert type(url)==str
    url = url.strip()
    url = url.strip('\'" ')
    assert url[0]!='#'
    (scheme, netloc, path, params, query, fragment) = urlparse(url)
    if len(scheme)>0 and len(netloc)>0 and netloc.find('.')!=-1:
        return url
    print('Got a bad url: ', url)
    assert False
    return None
    

def url2file(run, url, path):
    """PhantomJS wrapper
    url - http://name.tld
    path - where to save page code (html)"""
    cmd = run+' "'+url+'" '+path
    try:
        subprocess.call(cmd, shell=True)
    except:
        print('Cant execute: '+cmd)
        return False
    return True

def url2html(run, url, path):
    if os.path.isfile(path) == False:
        code = url2file(run, url, path)
        assert code==True
    try:
        html = file2text(path)
    except:
        print('Cant read file: '+path)
        assert False
    return html

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
        f = codecs.open(path, 'r', encoding='utf-8')
        #f = open(path, 'rU')
    except:
        print('Cant read file: '+path)
        return lines
    for line in f:
        if len(line)>0:
            lines.append(line.strip())
    f.close()
    return lines

def initLog(log_file, out = ''):
    """ Log file init """
    try:
        f = codecs.open(log_file, 'w', encoding='utf-8')
    except:
        print('Cant open log file: '+log_file)
        return False
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

def getIndex1(my_items):
    return my_items[1]

def getIndex2(my_items):
    return my_items[2]

def get_test_data(path):
    if os.path.isfile(path) == True:
        test_data = {}
        f = open(path, 'rU')
        for line in f:
            if line[0]!='#':
                items = line.split()
                if len(items)==2:
                    test_data[items[1]] = int(items[0])
        f.close()
        return test_data
    else:
        print('File not found: ',path)
        assert False

def showBlock(id, items):
    """ Block print
    No more in use
    Delete? """
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
    out = '=====Start of:'+str(id)+'\n'
    for child in items[id].iterdescendants():
        tags = tags + str(child.tag) + ' '
        if child.tag=='a':
            if child.attrib.has_key('href'):
                out = out + 'href: '+ child.attrib['href'] +'\n'            
        if child.tag=='img' and child.attrib.has_key('src'):
            out = out + 'img src: ' +child.attrib['src']+'\n'
    main_text = items[id].text_content().strip()
    textSize = len(main_text)
    out = out + 'Main text: ' +main_text+'\n'                            
    out = out + 'Text size: ' +str(textSize)+'\n'            
    out = out + 'Tags structure: ' +tags+'\n'           
    out = out + '=====End of:' +str(id) +'\n\n'
    return out

def getDomainfromUrl(url):
    tld = ('com','net','org','ucoz','narod')
    BaseUrl = urlparse(url).netloc
    BaseUrl = BaseUrl.lower()
    tmp = BaseUrl.split('.')
    if len(tmp)>=2:
        if len(tmp[-2])>2:
            if tmp[-2] not in tld:
                BaseUrl = tmp[-2]+'.'+tmp[-1]
    return BaseUrl

def parseBlocks(text, url='', block_complexity=2, minBlockSize=10, maxBlockSize=500, maxLinks=1):
    """ Get ad (tiser) blocks from html
    A tiser is a block with:
    Outer links less then maxLinks,
    Inner links is zero,
    Text size is between minBlockSize and maxBlockSize,
    Inner tag complexity is more then block_complexity,
    Params:
    text is a html code of the page
    url is a url of the page, needed for outer links detection"""
    assert type(text)==str
    if len(url)>0:
        BaseUrl = getDomainfromUrl(url)
    try:
        tree = html.document_fromstring(text)
    except:
        print('Cant render html')
        return None # ????
    items = {}
    id=0
    SkipBlocks = 0
    try:
        for element in tree.body.iter():
            if SkipBlocks>0:
                SkipBlocks-=1
                continue
            pool = ()
            hasLink = False
            LinkCounter=0
            InnerLinkCounter = 0
            Complexity = 0

            for child in element.iterdescendants():
                Complexity+=1
                # Filter html comments
                if str(type(child))=='<class \'lxml.html.HtmlComment\'>':
                    continue
                pool += (child.tag,)
                if child.tag == 'a':# Filter by tag (a href)
                    if child.attrib.has_key('href'):
                        if child.attrib['href'].find('http://')!=-1 and child.attrib['href'].lower().find(BaseUrl)==-1:
                            hasLink = True
                            LinkCounter+=1
                        else:
                            hasLink = False
                            InnerLinkCounter+=1
                            
            # Filter by Links and amount of tags (block complexity)                
            if hasLink and LinkCounter<=maxLinks and InnerLinkCounter==0 and Complexity>block_complexity:
                textSize = len(element.text_content().strip())                        
                # Filter blocks without text and large blocks
                if textSize>=minBlockSize and textSize<=maxBlockSize:
                    # How to filter counters? Block size?          
                    # How to get rid of small blocks with only one link? No way

                    # Finaly, block is good
                    items[id] = element
                    id+=1
                    SkipBlocks = len(pool)-1 # Skip checking for inner blocks, they are already in the ad block
    except:
        print('Bad html')
    return items

# Functions for AdsMiner

import subprocess
from urllib.parse import urlparse
from lxml import html
import codecs
import re
import os.path
import json
import hashlib
#from tidylib import tidy_document
#import chardet

class adblock(object):
    #Ad block (tiser) class
    def __init__(self, url='', id=0):
        """Create an AdBlock"""
        self.SrcUrl = clearUrl(url)
        self.SrcDomain = urlparse(self.SrcUrl).netloc.lower()
        self.Id = int(id)
        self.ImgUrls = []
        self.ImgCounter = 0
        self.Links = {}
        self.LinkCounter = 0
        self.Text = ''
        self.Hash = ''
        self.TextLen = 0

    def addImgUrl(self, e):
        """ Adds img url to AdBlock"""
        self.ImgUrls.append(e) # Should I check the url?
        self.ImgCounter+=1
        return

    def getImgUrls(self):
        """ Returns list of img urls"""
        return self.ImgUrls

    def addLink(self, redirect, landing):
        """ Adds redirect-landing pair urls to AdBlock"""
        self.Links[redirect]=landing
        self.LinkCounter+=1
        return

    def getText(self):
        """ Returns text of AdBlock"""
        return self.Text

    def getHash(self):
        """ Returns hash of AdBlock text"""
        return self.Hash

    def getTextLen(self):
        """ Returns length of the AdBlock text"""
        return self.TextLen

    def addText(self, text):
        """ Adds text to AdBlock"""
        self.Text = text#.encode('utf-8')
        self.Hash = hashlib.md5(self.Text).hexdigest()
        self.TextLen = len(self.Text)
        return

    def getLinks(self):
        """ Returns dict of ad urls pairs"""
        return self.Links

    def getId(self):
        """ Returns AdBlock ID"""
        return self.Id

    def getSrcUrl(self):
        """ Returns AdBlock Src Url"""
        return self.SrcUrl

    def getSrcDomain(self):
        """ Returns AdBlock Src Domain name"""
        return self.SrcDomain

    def ImgsNum(self):
        """ Returns number of img urls"""
        return self.ImgCounter

    def LinksNum(self):
        """ Returns number of ad urls pairs"""
        return self.LinkCounter

    def __str__(self):
        """Returns a string representation of AdBlock"""
        output = 'SrcUrl: '+self.getSrcUrl()+'\n'
        output+='ID: '+str(self.getId())+'\n'
        output+='Images: '+str(self.ImgsNum())+'\n'
        output+='Links: '+str(self.LinksNum())+'\n'
        output+='Text: '+str(self.getText())+'\n'
        return output

def uniqList(lst):
    assert type(lst)==list
    uniq = list(set(lst))
    return uniq

def readJson(jsonpath):
    with open(jsonpath, 'r') as fp:
        from_json = json.load(fp)    
    fp.close()
    return from_json

def writeJson(jsonpath, to_json):
    with open(jsonpath, 'w') as fp:
        json.dump(to_json, fp)
    fp.close()
    return

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
    

def url2file(run, url, path, timeout=5000):
    """PhantomJS wrapper
    url - http://name.tld
    path - where to save page code (html)"""
    cmd = run+' "'+url+'" '+path+' '+str(timeout)
    try:
        subprocess.call(cmd, shell=True)
    except:
        print('Cant execute: '+cmd)
        return False
    return True

def url2html(run, url, path, timeout=5000):
    if os.path.isfile(path) == False:
        code = url2file(run, url, path, timeout)
        assert code==True
    try:
        html = file2text(path)
        #html, errors = tidy_document(html, options={'hide-comments':1, 'new-inline-tags':'yatag'})
        #print(errors)
    except:
        print('Cant read file: '+path)
        assert False
    return html

def url2url(run, url, ref='http://yandex.ru', timeout=5000):
    """PhantomJS wrapper
    url - http://name.tld"""
    cmd = run+' "'+url+'" "'+ref+'" '+str(timeout)
    try:
        output=subprocess.check_output(cmd, shell=True)
    except:
        print('Cant execute: '+cmd)
        return ''
    try:
        s = output.decode('utf-8')
        s = re.search(r'URL###: (.+)',s)
        out = s.group(1)
    except:
        print('Redirect not found')
        out = ''
    return out

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

##def file2textU(path):
##    """Reads file from path
##    Detects encoding
##    Returns utf-8 text"""
##    try:
##        f = open(path, 'rb')
##    except:
##        print('Cant read file: '+path)
##        return ''
##    rawdata = f.read()
##    result = chardet.detect(rawdata)
##    charenc = result['encoding']
##    f.close()
##    text = rawdata.decode(charenc)
##    return text

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

def Block2List(url, id, item):
    """ Convert an ad block to a list
    [url, id, [href1, hrefN], [imgsrc1, imgsrcN], text]"""
    hrefs = []
    imgsrcs = []
    for child in item.iterdescendants():
        if child.tag=='a' and child.attrib.has_key('href'):
            hrefs.append(child.attrib['href'])
        if child.tag=='img' and child.attrib.has_key('src'):
            imgsrcs.append(child.attrib['src'])
    text = item.text_content().strip()
    hrefs = uniqList(hrefs)
    imgsrcs = uniqList(imgsrcs)
    out_list = [url, id, hrefs, imgsrcs, text]
    return out_list
    

def getBlock(id, items):
    """ Form human readable block """
    tags=''
    out = '=====Start of:'+str(id)+'\n'
    for child in items[id].iterdescendants():
        tags = tags + str(child.tag) + ' '
        if child.tag=='a' and child.attrib.has_key('href'):
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
    tld = ('com','net','org','ucoz','narod','livejournal','blogspot')
    BaseUrl = urlparse(url).netloc
    BaseUrl = BaseUrl.lower()
    tmp = BaseUrl.split('.')
    if len(tmp)>=2:
        if len(tmp[-2])>2:
            if tmp[-2] not in tld:
                BaseUrl = tmp[-2]+'.'+tmp[-1]
    return BaseUrl

def parseBlocks(text, url='', block_complexity=2, minBlockSize=10, maxBlockSize=500, maxLinks=1, maxDomains=1):
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
            DomainsList = []

            for child in element.iterdescendants():
                Complexity+=1
                # Filter html comments
                if str(type(child))=='<class \'lxml.html.HtmlComment\'>':
                    continue
                pool += (child.tag,)
                if child.tag == 'a':# Filter by tag (a href)      
                    if child.attrib.has_key('href'):
                        if child.attrib['href'].find('http://')==0 and child.attrib['href'].lower().find(BaseUrl)==-1:
                        #if child.attrib['href'].find('http://')!=-1 and child.attrib['href'].lower().find(BaseUrl)==-1:
                            hasLink = True
                            LinkCounter+=1
                            DomainsList.append(urlparse(child.attrib['href'].lower()).netloc)
                        else:
                            hasLink = False
                            InnerLinkCounter+=1                 

                            
            # Filter by Links and amount of tags (block complexity)
            if hasLink and LinkCounter<=maxLinks and InnerLinkCounter==0:
                if Complexity>block_complexity:
                    DomainsList = uniqList(DomainsList)
                    if len(DomainsList)<=maxDomains:
                        #print(pool)
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

# AdsMiner:Grabber
# TODO http://www.myjane.ru/articles/rubric/?id=54 =?
def url2file(url, html, png=''):
    """PhantomJS wrapper
    url - http://name.tld
    html - where to save page code (html)
    png - where to save rendered page (image)"""
    import subprocess
    code = subprocess.call(['save.cmd', url, html, png])
    # TODO  check return code
    return code

def file2text(path):
    """Reads utf-8 file from path"""    
    path = str(path)
    import codecs
    f = codecs.open(path, 'r', encoding='utf-8')
    text = f.read()
    f.close()
    return text

def file2list(path):
    """Reads utf-8 file from path"""    
    path = str(path)
    import codecs
    f = codecs.open(path, 'r', encoding='utf-8')
    # TODO if bad file?
    text = f.read()
    f.close()
    return text

def rebuild(id, items):
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
            print('Img found')
            print(child.attrib)
            assert False
            #if child.attrib.has_key('href'):
             #   print(child.attrib['href'])            
    #items[id].text_content()
    print('End of:',id)
    print()
    return None

def getAdBlocks(text, url=''):
    assert type(text)==str
    from urllib.parse import urlparse
    from lxml import html
    if len(url)>0:
        BaseUrl = urlparse(url).netloc
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

urls = 'lists\\women.txt'
datadir = 'F:\\tmp\\py\\'

import hashlib
import os.path
f = open(urls, 'rU')
for line in f:
    url = line.strip()
    if len(url)==0: continue
    url_id = hashlib.md5(url.encode('utf-8')).hexdigest()    
    path = datadir + url_id + '.html'

    print(url, path)
    if os.path.isfile(path) == False:
        code = url2file(url, path)
    # TODO if bad return code?
    text = file2text(path)
    # TODO if bad return code?

    ads, blocks = getAdBlocks(text, url)
    print('Find ads:',len(ads))
    
    #for k,v in data.items(): print(k,v)

    for id in ads.keys():
        rebuild(id,blocks)

    del(ads)
    del(blocks)
    #break
f.close()

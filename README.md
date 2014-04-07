AdsMiner
========
<p>Ad Blocks data miner</p>
<p>Based on Python 3 and Phantom.JS</p>

INSTALL
=======
<ul>
<li>aptitude install python3-lxml</li>
<li>aptitude install curl</li>
<li>aptitude install python-mysqldb</li>
<li>#pip-3.2 install pytidylib6</li>
<li>#pip-3.2 install chardet</li>
<li>pip-3.2 install requests</li>
<li>cp miner.conf.OS miner.conf</li>
</ul>

TODO
====

add graber to cron
add bot master to cron

add blacklist support for grab.parser

replace urllib with requests?

grab2 json save every N blocks?

blacklist rambler counter

Grab direct
http://direct.yandex.ru/search?text=%27%D0%B3%D0%BE%D1%80%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%27&ref-page=118826

IDEAS
=====

INFO
====

<h2>Grabber output structure</h2>
0 url
1 block_id
2 links[]
3 img_links[]
4 block_text
5 target_urls[]

<h2>Bot Master functions</h2>
 manage cache
 get tasks
 clear cookies.txt?
 zip and send results

<h2>Tables</h2>
1.Categories (category_id, name)
2.Sites (site_id, domain)
3.Urls (url_id, category_id, site_id, url)
4.Ads (ad_id, url_id, text, time)
5.Landings (land_id, ad_id, url_id, src_url, land_url, time)
6.(land_id, landing_domain)
7.Images (img_id, ad_id, img_url)





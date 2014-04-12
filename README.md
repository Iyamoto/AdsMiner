AdsMiner
========
<p>Ad Blocks data miner</p>
<p>Based on Python 3 and Phantom.JS</p>

INSTALL
=======
<ul>
<li>aptitude install python3-lxml</li>
<li>#aptitude install curl</li>
<li>pip-3.2 install PyMySQL</li>
<li>pip-3.2 install sqlalchemy</li>
<li>#pip-3.2 install pytidylib6</li>
<li>#pip-3.2 install chardet</li>
<li>pip-3.2 install requests</li>
<li>cp miner.conf.OS miner.conf</li>
</ul>

TODO
====
grab.js - fix stuck on bad pages - if any

gather blacklist, adnets and partners
	fill db
	run getTopAd.py 30
	check domains
	analyze (run getAdIdinfo.py ad_domain_id)
	fill info/blacklist, adnets and partners

add graber to cron
add bot master to cron

Get yandex landing domain from ad text?

Grab direct with out redirects
http://direct.yandex.ru/search?text=%27%D0%B3%D0%BE%D1%80%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%27&ref-page=118826

IDEAS
=====

INFO
====

<h2>Grabber output structure</h2>
AdBlock elements:
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
<ol>
<li>1.Categories (category_id, name)</li>
<li>2.Sites (site_id, domain)</li>
<li>3.Urls (url_id, category_id, site_id, url)</li>
<li>4.Ads (ad_id, url_id, text, hash)</li>
<li>5.Landings (land_id, ad_id, url_id, src_url, land_url, land_domain_id, ad_domain_id)</li>
<li>6.LandDomains (land_domain_id, landing_domain)</li>
<li>7.Images (img_id, ad_id, img_url)</li>
<li>8.AdDomains (ad_domain_id, ad_domain)</li>
</ol>





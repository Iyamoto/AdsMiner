AdsMiner
========
<p>Ad Blocks data miner</p>
<p>Based on Phantom.JS</p>

INSTALL
=======
<ul>
<li>aptitude install python-tidylib python3-lxml</li>
<li>pip-3.2 install pytidylib6</li>
<li>pip-3.2 install chardet</li>
<li>cp miner.conf.OS miner.conf</li>
</ul>

TODO
====
how to improve save.js?
resourceTimeout to config 

add graber to cron
clear cache daily (server)

blacklist rambler counter

gzip json? no need

Grab direct
http://direct.yandex.ru/search?text=%27%D0%B3%D0%BE%D1%80%D0%BE%D1%81%D0%BA%D0%BE%D0%BF%27&ref-page=118826

add pytidylib to grabber

Grabber output structure
url
block_id
links[]
img_links[]
block_text

master
 manage cache
 get tasks

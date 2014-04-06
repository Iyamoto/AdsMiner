AdsMiner
========
<p>Ad Blocks data miner</p>
<p>Based on Python 3 and Phantom.JS</p>

INSTALL
=======
<ul>
<li>aptitude install python3-lxml</li>
<li>aptitude install curl</li>
<li>#pip-3.2 install pytidylib6</li>
<li>#pip-3.2 install chardet</li>
<li>pip-3.2 install requests</li>
<li>cp miner.conf.OS miner.conf</li>
</ul>

TODO
====

add graber to cron
add bot master to cron

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
url
block_id
links[]
img_links[]
block_text
target_urls[]

<h2>Bot Master functions</h2>
 manage cache
 get tasks
 clear cookies.txt?
 zip and send results

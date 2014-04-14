rem grab html from urls list with phantom.js
set params=--cookies-file=cookies.txt --disk-cache=false --proxy-type=none
set outdir=F:\tmp\py\
set timeout=3000
set threads=1

D:\tools\phantomjs-1.9.7-windows\phantomjs.exe %params% grab.js %1 %outdir% %timeout% %threads%
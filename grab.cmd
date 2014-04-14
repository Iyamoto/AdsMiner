rem grab html from urls list with phantom.js
set params=--cookies-file=cookies.txt --disk-cache=false --proxy-type=none
set outdir=F:\tmp\py\
set timeout=5000
set threads=2

D:\tools\phantomjs-1.9.7-windows\phantomjs.exe %params% grab.js %1 %outdir% %timeout% %threads%
@echo off
rem get redirected url
set params=--cookies-file=cookies.txt --disk-cache=true --proxy-type=none
D:\tools\phantomjs-1.9.7-windows\phantomjs.exe %params% redir.js %1 %2 %3
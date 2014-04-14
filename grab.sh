#!/bin/bash
#grab html from urls list with phantom.js
phantom='/usr/local/phantomjs/bin/phantomjs'
param='--cookies-file=cookies.txt --disk-cache=false --proxy-type=none'
outdir='/tmp/phantom/'
timeout='3000'
threads='1'
echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6
$phantom $param grab.js $1 $outdir $timeout $threads > /dev/null 2>&1
echo 0 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 0 > /proc/sys/net/ipv6/conf/default/disable_ipv6
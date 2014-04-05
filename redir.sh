#!/bin/bash
phantom='/usr/local/phantomjs/bin/phantomjs'
param='--cookies-file=cookies.txt --disk-cache=true --proxy-type=none'
echo 1 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 1 > /proc/sys/net/ipv6/conf/default/disable_ipv6
$phantom $param redir.js $1 $2 $3
echo 0 > /proc/sys/net/ipv6/conf/all/disable_ipv6
echo 0 > /proc/sys/net/ipv6/conf/default/disable_ipv6
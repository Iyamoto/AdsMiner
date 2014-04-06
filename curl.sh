#!/bin/bash
# cat  tasks/targets.wget |xargs -n1 -i bash -k curl.sh  {}

echo $1
curl -s -i -A 'Mozilla/5.0 (Windows NT 5.1; rv:27.0) Gecko/20100101 Firefox/27.0' -L $1  |grep "200 OK" -B 100 | tac |grep -m 1 -i "Location: http"; 
if [ $? -ne "0" ]
then
 echo "No redirect found"
fi

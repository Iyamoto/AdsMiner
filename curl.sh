#!/bin/bash
# cat list_test |xargs -n1 -i bash -k curl.sh  {}

echo $1
curl -s -i -A 'Mozilla/4.0' -L $1  |grep "200 OK" -B 100 | tac |grep -m 1 -i "Location: http"

#!/bin/bash

for i in *; do
    if [ "${i:0:4}" = "taxi" ];then
        echo "Готовим файл  $i"
        awk '{gsub(/ UTC,/,",")}1' $i > temp.txt && mv temp.txt $i
        tail -n3 $i
    fi
done

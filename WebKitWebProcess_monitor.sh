#!/bin/bash

while [ 1 ]

do

    pid=$(ps -eaf | /bin/grep WebKitWebProcess | grep -v $0 | /bin/grep -v grep | awk '{print $2}')

    #echo "pid=${pid}"

    # CPU%,MEM%
    cpu_mem=$(/bin/top -b -n 2 -d 1 -p $pid | tail -1 | awk '{print $9,$10}' | tr ' ' ',')

    timestamp=$(date +"%Y-%m-%d %T")

    echo "date,cpu,mem=$timestamp,$cpu_mem"

    echo "$timestamp,$cpu_mem" >> ~/WebKitWeb.log

    sleep 60

done

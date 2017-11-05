#!/bin/sh
ps up `cat mydaemon.pid ` >/dev/null && echo "Program Running" || python /home/kyligence/SHREPA/Lianjia_Collection_Main_2017.py log

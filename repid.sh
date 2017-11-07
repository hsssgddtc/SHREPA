#!/bin/bash

for i in 0 1 2 3 4 5 6 7 8 9 10 11 12
do
base_path="/home/kyligence/SHREPA_"
pid_path=$base_path$i"/mydaemon.pid"
kill `cat $base_path$i"/mydaemon.pid"`
rm $pid_path
done

#!/bin/bash
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12
do
base_path="/home/kyligence/SHREPA_"
code_path=$base_path$i
rm -rf $code_path
git clone "https://github.com/hsssgddtc/SHREPA.git" $code_path --depth 1
done
exit 0

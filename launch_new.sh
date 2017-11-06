#!/bin/bash  
 
cur_path="$PWD"
now=$(date +"%Y%m%d")
output_path=$cur_path"/logs/cron_"$now".output"
date >> $output_path

funcCreatePath(){
pid_path=$cur_path"/mydaemon.pid"
code_path=$cur_path"/Lianjia_Collection_Main_2017.py"
log_path=$cur_path"/"
if [ $1 = 1 ]
then district=上海周边,崇明,金山,静安,黄浦,奉贤,闸北
elif [ $1 = 2 ]
then district=虹口
elif [ $1 = 3 ]
then district=长宁
elif [ $1 = 4 ]
then district=青浦
elif [ $1 = 5 ]
then district=嘉定
elif [ $1 = 6 ]
then district=徐汇
elif [ $1 = 7 ]
then district=松江
elif [ $1 = 8 ]
then district=普陀
elif [ $1 = 9 ]
then district=杨浦
elif [ $1 = 10 ]
then district=宝山
elif [ $1 = 11 ]
then district=闵行
elif [ $1 = 12 ]
then district=浦东
fi
ps up `cat $cur_path"/mydaemon.pid"` >/dev/null && echo "Program Running" || `python $code_path log incre $district` >> $output_path 2>&1
#echo $district
}
num=`echo $cur_path | sed 's/[^0-9]//g'`
funcCreatePath $num

#!/bin/bash  

cur_path=`pwd`"/SHREPA_"$1 

funcCreatePath(){
pid_path=$cur_path"/mydaemon.pid"

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

if [ $1 = 0 ]
then ps up `cat $cur_path"/mydaemon.pid"` >/dev/null 2>&1 && echo "Program Running" || `python $cur_path"/Lianjia_Refresh_Main_2017.py" log refresh`
else
ps up `cat $cur_path"/mydaemon.pid"` >/dev/null 2>&1 && echo "Program Running" || `python $cur_path"/Lianjia_Collection_Main_2017.py" log $district`
fi
}
num=`echo $cur_path | sed 's/[^0-9]//g'`
funcCreatePath $num

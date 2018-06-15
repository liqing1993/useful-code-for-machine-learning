#!/bin/bash

[[ $# -eq 0 ]] && echo "$0 caffemodel resize_scale" && exit 0
set -x
deploy=$1
model=$2
resize_scale=$3

d=`pwd`
current_dir=`basename $d`
iter=`echo $model |awk -F '.' '{print $1}' |awk -F '_' '{print $NF}'`
save_dir=ssd_${current_dir}_iter_$iter
#anno_path=/home/caiyang/workspace/ssd/data/hyy_data/benchmark/wide/image_anno_set/benchmark_wide_1000
anno_path=/home/user/data/detection/libraf/benchmark/wide/image_anno_set/benchmark_wide_1000

../../../build/tools/ssd_predict $deploy $model $anno_path 0.01 $save_dir
echo "begin roc task"
python ~/data/detection_code/ssd/lib/tools/roc.py --anno_file=$anno_path --save_dir=$save_dir --resized_height=$resize_scale --anno_key=person_upper --ious=0.4 --scale_ranges="(8,1000)"  --show

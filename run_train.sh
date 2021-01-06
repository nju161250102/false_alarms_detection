#! /bin/bash
case $1 in
"method")
python3 ./python/TrainScript.py "/home/qmy/Data/MethodFeature/" "/home/qmy/Data/label.csv" "/home/qmy/Data/MethodFeature.csv" 10 "All"
;;
"slice_1")
python3 ./python/TrainScript.py "/home/qmy/Data/SliceFeature/" "/home/qmy/Data/slice_label1.csv" "/home/qmy/Data/SliceFeature_$2.csv" 10 $2
;;
"slice_2")
python3 ./python/TrainScript.py "/home/qmy/Data/SliceFeature/" "/home/qmy/Data/slice_label2.csv" "/home/qmy/Data/SliceFeature_$2.csv" 10 $2
;;
"category")
python3 ./python/TrainScript.py "/home/qmy/Data/MethodFeature/" "/home/qmy/Data/label.csv" "/home/qmy/Data/CategoryResult" 10 "Category"
;;
*)
echo "参数1"
echo "method: 方法体"
echo "slice_1: 人工标记前的切片结果"
echo "slice_2: 人工标记后的切片结果"
esac

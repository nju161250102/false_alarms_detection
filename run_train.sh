#! /bin/bash
case $1 in
"method")
python3 ./python/TrainScript.py "/home/qmy/Data/MethodFeature/" "/home/qmy/Data/label.csv" "/home/qmy/Data/MethodFeature.csv" 10 "All"
;;
"slice")
python3 ./python/TrainScript.py "/home/qmy/Data/SliceFeature/" "/home/qmy/Data/slice_label.csv" "/home/qmy/Data/SliceFeature_$2.csv" 10 $2
;;
*)
echo "error!"
esac

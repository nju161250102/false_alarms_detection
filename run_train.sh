#! /bin/bash
case $1 in
"method")
python3 ./python/TrainScript.py "/home/qmy/Data/MethodFeature/" "/home/qmy/Data/label.csv" "/home/qmy/Data/MethodFeature.csv" 5
;;
"slice")
python3 ./python/TrainScript.py "/home/qmy/Data/SliceFeature/" "/home/qmy/Data/slice_label.csv" "/home/qmy/Data/SliceFeature.csv" 5
;;
*)
echo "error!"
esac

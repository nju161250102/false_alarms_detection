#! /bin/bash
case $1 in
"method")
python3 ./python/TrainScript.py "/home/qmy/Data/MethodFeature" "/home/qmy/Data/label.csv"
;;
"slice")
python3 ./python/TrainScript.py "/home/qmy/Data/SliceFeature" "/home/qmy/Data/slice_label.csv"
;;
*)
echo "error!"
esac

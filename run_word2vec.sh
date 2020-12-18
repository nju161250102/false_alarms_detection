#! /bin/bash
function clean_dir() {
    if [ -d $1 ];then
        rm -rf $1
    fi
    mkdir $1
}

function transform() {
    data_dir=$1
    for word in word_ans word_aps word_ext ast type
    do
        for num in 16 32 64
        do
            echo "${word}_v_${num}"
            clean_dir "${data_dir}/${word}_v_${num}"
            python3 ./python/WordEmbedding.py "${data_dir}/${word}" "${data_dir}/${word}_v_${num}" $num
        done
    done
}

if [ $# -gt 0 ]
then
    transform "/home/qmy/Data/$1"
else
    transform "/home/qmy/Data/MethodFeature"
    transform "/home/qmy/Data/SliceFeature"
fi
